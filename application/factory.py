"""
Application Layer - Factory Pattern
Implementación del patrón Factory Method
Aplicando OCP y DIP
"""
from typing import Dict, Any, Optional
import logging

from domain.interfaces import ProveedorAbstracto
from domain.entities import ProvisioningResult, VMStatus
from infrastructure.providers import AWS, Azure, Google, OnPremise

logger = logging.getLogger(__name__)


class VMProviderFactory:
    """
    Creator Concreto: Factory que crea proveedores según el tipo solicitado
    
    Aplicando:
    - Factory Method Pattern: Centraliza la creación de objetos
    - OCP: Fácil agregar nuevos proveedores sin modificar esta clase
    - DIP: Retorna abstracciones (ProveedorAbstracto) no implementaciones
    - SRP: Solo se encarga de crear proveedores
    """
    
    # Registro de proveedores disponibles (facilita extensibilidad)
    _providers = {
        'aws': AWS,
        'azure': Azure,
        'google': Google,
        'gcp': Google,  # Alias
        'onpremise': OnPremise,
        'on-premise': OnPremise  # Alias
    }
    
    @classmethod
    def register_provider(cls, name: str, provider_class):
        """
        Permite registrar nuevos proveedores dinámicamente
        Mejora la extensibilidad (OCP)
        """
        cls._providers[name.lower()] = provider_class
        logger.info(f"Proveedor registrado: {name}")
    
    @classmethod
    def create_provider(cls, provider_type: str, config: Dict[str, Any]) -> Optional[ProveedorAbstracto]:
        """
        Factory Method: Crea el proveedor apropiado según el tipo
        
        Args:
            provider_type: Tipo de proveedor (aws, azure, google, onpremise)
            config: Configuración específica del proveedor
            
        Returns:
            Instancia del proveedor o None si no existe
        """
        provider_type = provider_type.lower().strip()
        
        provider_class = cls._providers.get(provider_type)
        
        if provider_class is None:
            logger.error(f"Proveedor no soportado: {provider_type}")
            return None
        
        try:
            # Extraer parámetros comunes
            field_type = config.get('type', 'default')
            method_type = config.get('method', 'default')
            
            # Crear instancia del proveedor
            provider = provider_class(field_type, method_type)
            
            logger.info(f"Proveedor creado exitosamente: {provider_type}")
            return provider
            
        except Exception as e:
            logger.error(f"Error creando proveedor {provider_type}: {str(e)}")
            return None
    
    @classmethod
    def get_available_providers(cls) -> list:
        """Retorna lista de proveedores disponibles"""
        return list(cls._providers.keys())


class VMProvisioningService:
    """
    Application Service: Servicio de aprovisionamiento de VMs
    
    Aplicando:
    - SRP: Solo se encarga de orquestar el aprovisionamiento
    - DIP: Depende de abstracciones (ProveedorAbstracto)
    - ISP: Interfaz específica para aprovisionamiento
    """
    
    def __init__(self):
        self.factory = VMProviderFactory()
    
    def provision_vm(self, provider_type: str, config: Dict[str, Any]) -> ProvisioningResult:
        """
        Aprovisiona una VM usando el proveedor especificado
        
        Args:
            provider_type: Tipo de proveedor (aws, azure, google, onpremise)
            config: Configuración de la VM a crear
            
        Returns:
            ProvisioningResult con el resultado de la operación
        """
        try:
            # Validar proveedor
            if not provider_type:
                return ProvisioningResult(
                    success=False,
                    message="Error: Tipo de proveedor no especificado",
                    error_detail="El parámetro 'provider' es requerido"
                )
            
            # Crear proveedor usando Factory
            provider = self.factory.create_provider(provider_type, config)
            
            if provider is None:
                available = self.factory.get_available_providers()
                return ProvisioningResult(
                    success=False,
                    message=f"Proveedor '{provider_type}' no soportado",
                    error_detail=f"Proveedores disponibles: {', '.join(available)}",
                    provider=provider_type
                )
            
            # Verificar estado del proveedor
            if not provider.estado():
                return ProvisioningResult(
                    success=False,
                    message="Proveedor no disponible",
                    error_detail=f"El proveedor {provider_type} no está disponible en este momento",
                    provider=provider_type
                )
            
            # Aprovisionar VM (RNF4 - Logging sin información sensible)
            logger.info(f"Iniciando aprovisionamiento en {provider_type}")
            
            vm = provider.provisionar()
            
            # Validar creación
            if vm and vm.status == VMStatus.RUNNING:
                logger.info(f"VM aprovisionada exitosamente - ID: {vm.vmId}")
                
                return ProvisioningResult(
                    success=True,
                    vm_id=vm.vmId,
                    message=f"VM creada exitosamente en {provider_type}",
                    provider=provider_type
                )
            else:
                return ProvisioningResult(
                    success=False,
                    message="Error al crear la VM",
                    error_detail="La VM no pudo ser iniciada correctamente",
                    provider=provider_type
                )
                
        except Exception as e:
            logger.error(f"Error en aprovisionamiento: {str(e)}", exc_info=True)
            return ProvisioningResult(
                success=False,
                message="Error interno en el aprovisionamiento",
                error_detail=str(e),
                provider=provider_type
            )
    
    def get_supported_providers(self) -> list:
        """Retorna lista de proveedores soportados"""
        return self.factory.get_available_providers()