"""
Application Layer - Factory Pattern
Implementación del patrón Factory Method
Aplicando OCP y DIP
"""
from typing import Dict, Any, Optional, Type
import logging

from pydantic import ValidationError
from application.schemas import get_validator_for
from domain.interfaces import ProveedorAbstracto
from domain.entities import ProvisioningResult, VMStatus
from infrastructure.providers import AWS, Azure, Google, OnPremise  # Esta importación sigue funcionando gracias al __init__.py

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
            # Crear instancia del proveedor
            provider = provider_class(config)
            
            logger.info(f"Proveedor creado exitosamente: {provider_type}")
            return provider
            
        except Exception as e:
            logger.error(f"Error creando proveedor {provider_type}: {str(e)}")
            return None
    
    @classmethod
    def get_available_providers(cls) -> list:
        """Retorna lista de proveedores disponibles"""
        return list(cls._providers.keys())


class ProviderOrchestrator:
    """
    Clase auxiliar para validar y obtener un proveedor.
    Refinamiento de SRP: Su única responsabilidad es la validación y preparación del proveedor.
    """
    def __init__(self, factory: VMProviderFactory):
        self.factory = factory

    def get_validated_provider(self, provider_type: str, config: Dict[str, Any]) -> tuple[Optional[ProveedorAbstracto], Optional[ProvisioningResult]]:
        """
        Valida la solicitud y devuelve el proveedor o un resultado de error.
        """
        if not provider_type:
            error_result = ProvisioningResult(
                success=False,
                message="Error: Tipo de proveedor no especificado",
                error_detail="El parámetro 'provider' es requerido"
            )
            return None, error_result

        # 1. Validar el `config` usando el esquema de Pydantic correspondiente
        validator = get_validator_for(provider_type)
        if validator:
            try:
                # Pydantic parsea, valida y asigna valores por defecto
                validated_config = validator.model_validate(config)
                # Usamos la configuración validada y enriquecida para la creación
                config = validated_config.model_dump()
            except ValidationError as e:
                # Si la validación falla, Pydantic genera un error detallado
                error_result = ProvisioningResult(
                    success=False,
                    message="Error de validación de parámetros",
                    error_detail=e.json(),  # Devolvemos los detalles del error en formato JSON
                    provider=provider_type
                )
                return None, error_result

        provider = self.factory.create_provider(provider_type, config)

        if provider is None:
            available = self.factory.get_available_providers()
            error_result = ProvisioningResult(
                success=False,
                message=f"Proveedor '{provider_type}' no soportado",
                error_detail=f"Proveedores disponibles: {', '.join(available)}",
                provider=provider_type
            )
            return None, error_result

        if not provider.estado():
            error_result = ProvisioningResult(
                success=False,
                message="Proveedor no disponible",
                error_detail=f"El proveedor {provider_type} no está disponible en este momento",
                provider=provider_type
            )
            return None, error_result

        # Si todo es correcto, devuelve el proveedor y ningún error.
        return provider, None


class VMProvisioningService:
    """
    Application Service: Servicio de aprovisionamiento de VMs
    
    Aplicando:
    - SRP: Solo se encarga de orquestar el aprovisionamiento
    - DIP: Depende de abstracciones (ProveedorAbstracto)
    - ISP: Interfaz específica para aprovisionamiento
    """
    
    def __init__(self):
        factory = VMProviderFactory()
        self.orchestrator = ProviderOrchestrator(factory)

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
            # 1. Delegar validación y obtención del proveedor
            provider, error_result = self.orchestrator.get_validated_provider(provider_type, config)

            # Si hubo un error de validación, retornarlo inmediatamente
            if error_result:
                return error_result

            # Ayuda al analizador estático a entender que `provider` no puede ser None en este punto.
            assert provider is not None

            # Aprovisionar VM (RNF4 - Logging sin información sensible)
            logger.info(f"Iniciando aprovisionamiento en {provider_type} con proveedor validado.")
            
            vm = provider.provisionar()
            
            # Validar creación
            if vm and vm.status == VMStatus.RUNNING:
                logger.info(f"VM aprovisionada exitosamente - ID: {vm.vmId}")
                
                return ProvisioningResult(
                    success=True,
                    vm_id=vm.vmId,
                    message=f"VM creada exitosamente en {provider_type}",
                    provider=provider_type,
                    vm_details=vm.to_dict()  # Añadir detalles de la VM
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
        return self.orchestrator.factory.get_available_providers()