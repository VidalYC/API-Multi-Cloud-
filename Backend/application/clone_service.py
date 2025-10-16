"""
Application Layer - Clone Service
Servicio para clonar VMs usando el patrón Prototype.
Orquesta la lógica de negocio para clonación de máquinas virtuales.
"""
from typing import Optional, Dict, Any
from domain.entities import MachineVirtual, ProvisioningResult
from domain.prototype_registry import VMPrototypeRegistry
import logging

logger = logging.getLogger(__name__)


class VMCloneService:
    """
    Servicio de clonación de VMs usando el patrón Prototype.

    Aplicando SRP: Responsabilidad única de orquestrar clonación de VMs.
    Aplicando DIP: Depende de abstracciones (MachineVirtual, VMPrototypeRegistry).
    """

    def __init__(self):
        self.registry = VMPrototypeRegistry()

    def clone_from_prototype(
        self,
        prototype_name: str,
        new_vm_name: str,
        customizations: Optional[Dict[str, Any]] = None
    ) -> ProvisioningResult:
        """
        Clona una VM desde un prototipo del registro.

        Args:
            prototype_name: Nombre del prototipo a clonar
            new_vm_name: Nombre para la nueva VM
            customizations: Personalizaciones opcionales (vcpus, memoryGB, region, etc.)

        Returns:
            ProvisioningResult con el resultado de la clonación
        """
        try:
            logger.info(f"Clonando VM desde prototipo: {prototype_name}")

            # Verificar que el prototipo existe
            if not self.registry.prototype_exists(prototype_name):
                available_prototypes = [p['name'] for p in self.registry.list_prototypes()]
                return ProvisioningResult(
                    success=False,
                    message=f"Prototipo '{prototype_name}' no encontrado",
                    error_detail=f"Prototipos disponibles: {', '.join(available_prototypes)}"
                )

            # Preparar customizaciones
            custom_params = customizations or {}

            # Clonar el prototipo
            cloned_vm = self.registry.clone_prototype(
                name=prototype_name,
                new_name=new_vm_name,
                **custom_params
            )

            if not cloned_vm:
                return ProvisioningResult(
                    success=False,
                    message="Error al clonar el prototipo",
                    error_detail="No se pudo crear la VM clonada"
                )

            # Validar consistencia de región (RNF1)
            if cloned_vm.network and cloned_vm.disks:
                network_region = cloned_vm.network.region
                for disk in cloned_vm.disks:
                    if disk.region != network_region:
                        return ProvisioningResult(
                            success=False,
                            message="Error de consistencia de región",
                            error_detail=f"La región del disco ({disk.region}) no coincide con la región de la red ({network_region})"
                        )

            logger.info(f"VM clonada exitosamente: {cloned_vm.vmId}")

            return ProvisioningResult(
                success=True,
                vm_id=cloned_vm.vmId,
                message=f"VM '{new_vm_name}' clonada exitosamente desde '{prototype_name}'",
                provider=cloned_vm.provider,
                vm_details=cloned_vm.to_dict()
            )

        except Exception as e:
            logger.error(f"Error al clonar VM desde prototipo: {str(e)}")
            return ProvisioningResult(
                success=False,
                message="Error al clonar VM",
                error_detail=str(e)
            )

    def clone_existing_vm(
        self,
        source_vm: MachineVirtual,
        new_vm_name: str,
        customizations: Optional[Dict[str, Any]] = None
    ) -> ProvisioningResult:
        """
        Clona una VM existente (no necesariamente un prototipo del registro).

        Args:
            source_vm: VM fuente a clonar
            new_vm_name: Nombre para la nueva VM
            customizations: Personalizaciones opcionales

        Returns:
            ProvisioningResult con el resultado de la clonación
        """
        try:
            logger.info(f"Clonando VM existente: {source_vm.vmId}")

            # Preparar customizaciones
            custom_params = customizations or {}

            # Clonar la VM
            cloned_vm = source_vm.clone(new_name=new_vm_name, **custom_params)

            # Validar consistencia de región (RNF1)
            if cloned_vm.network and cloned_vm.disks:
                network_region = cloned_vm.network.region
                for disk in cloned_vm.disks:
                    if disk.region != network_region:
                        return ProvisioningResult(
                            success=False,
                            message="Error de consistencia de región",
                            error_detail=f"La región del disco ({disk.region}) no coincide con la región de la red ({network_region})"
                        )

            logger.info(f"VM clonada exitosamente: {cloned_vm.vmId}")

            return ProvisioningResult(
                success=True,
                vm_id=cloned_vm.vmId,
                message=f"VM '{new_vm_name}' clonada exitosamente",
                provider=cloned_vm.provider,
                vm_details=cloned_vm.to_dict()
            )

        except Exception as e:
            logger.error(f"Error al clonar VM existente: {str(e)}")
            return ProvisioningResult(
                success=False,
                message="Error al clonar VM",
                error_detail=str(e)
            )

    def list_available_prototypes(self) -> Dict[str, Any]:
        """
        Lista todos los prototipos disponibles en el registro.

        Returns:
            Diccionario con la lista de prototipos y sus detalles
        """
        try:
            prototypes = self.registry.list_prototypes()
            return {
                "success": True,
                "count": len(prototypes),
                "prototypes": prototypes
            }
        except Exception as e:
            logger.error(f"Error al listar prototipos: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "prototypes": []
            }

    def get_prototype_details(self, prototype_name: str) -> Dict[str, Any]:
        """
        Obtiene los detalles completos de un prototipo específico.

        Args:
            prototype_name: Nombre del prototipo

        Returns:
            Diccionario con los detalles del prototipo
        """
        try:
            prototype = self.registry.get_prototype(prototype_name)
            if not prototype:
                return {
                    "success": False,
                    "error": f"Prototipo '{prototype_name}' no encontrado"
                }

            return {
                "success": True,
                "prototype": prototype.to_dict()
            }
        except Exception as e:
            logger.error(f"Error al obtener detalles del prototipo: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    def register_custom_prototype(
        self,
        name: str,
        vm: MachineVirtual
    ) -> Dict[str, Any]:
        """
        Registra una VM como prototipo personalizado en el registro.

        Args:
            name: Nombre identificador del prototipo
            vm: Instancia de MachineVirtual a registrar

        Returns:
            Diccionario con el resultado de la operación
        """
        try:
            # Verificar si ya existe
            if self.registry.prototype_exists(name):
                return {
                    "success": False,
                    "message": f"Ya existe un prototipo con el nombre '{name}'"
                }

            # Registrar el prototipo
            self.registry.register_prototype(name, vm)

            logger.info(f"Prototipo personalizado registrado: {name}")

            return {
                "success": True,
                "message": f"Prototipo '{name}' registrado exitosamente"
            }

        except Exception as e:
            logger.error(f"Error al registrar prototipo personalizado: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
