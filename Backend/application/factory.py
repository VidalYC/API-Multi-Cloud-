from typing import Dict, Any, Optional, Type
import logging

from pydantic import ValidationError
from application.schemas import get_validator_for
from domain.interfaces import ProveedorAbstracto
from domain.entities import ProvisioningResult, VMStatus, MachineVirtual
from domain.builder import VMBuilder, VMDirector
from infrastructure.providers import AWS, Azure, Google, OnPremise  # Esta importación sigue funcionando gracias al __init__.py
from infrastructure.builders import AWSVMBuilder, AzureVMBuilder, GoogleVMBuilder, OnPremiseVMBuilder

logger = logging.getLogger(__name__)


class VMProviderFactory:
    
    
    
    _providers = {
        'aws': AWS,
        'azure': Azure,
        'google': Google,
        'gcp': Google, 
        'onpremise': OnPremise  
    }
    
    @classmethod
    def register_provider(cls, name: str, provider_class):
        
        cls._providers[name.lower()] = provider_class
        logger.info(f"Proveedor registrado: {name}")
    
    @classmethod
    def create_provider(cls, provider_type: str, config: Dict[str, Any]) -> Optional[ProveedorAbstracto]:
        
        provider_type = provider_type.lower().strip()
        
        provider_class = cls._providers.get(provider_type)
        
        if provider_class is None:
            logger.error(f"Proveedor no soportado: {provider_type}")
            return None
        
        try:
            
            provider = provider_class(config)
            
            logger.info(f"Proveedor creado exitosamente: {provider_type}")
            return provider
            
        except Exception as e:
            logger.error(f"Error creando proveedor {provider_type}: {str(e)}")
            return None
    
    @classmethod
    def get_available_providers(cls) -> list:
        
        return list(cls._providers.keys())


class ProviderOrchestrator:
    
    def __init__(self, factory: VMProviderFactory):
        self.factory = factory

    def get_validated_provider(self, provider_type: str, config: Dict[str, Any]) -> tuple[Optional[ProveedorAbstracto], Optional[ProvisioningResult]]:
        
        if not provider_type:
            error_result = ProvisioningResult(
                success=False,
                message="Error: Tipo de proveedor no especificado",
                error_detail="El parámetro 'provider' es requerido"
            )
            return None, error_result

       
        validator = get_validator_for(provider_type)
        if validator:
            try:
                
                validated_config = validator.model_validate(config)
                
                config = validated_config.model_dump()
            except ValidationError as e:
                
                error_result = ProvisioningResult(
                    success=False,
                    message="Error de validación de parámetros",
                    error_detail=e.json(),  
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

        
        return provider, None


class VMProvisioningService:
    
    
    def __init__(self):
        factory = VMProviderFactory()
        self.orchestrator = ProviderOrchestrator(factory)

    def provision_vm(self, provider_type: str, config: Dict[str, Any]) -> ProvisioningResult:
       
        try:
            
            provider, error_result = self.orchestrator.get_validated_provider(provider_type, config)

            
            if error_result:
                return error_result

            
            assert provider is not None

            
            logger.info(f"Iniciando aprovisionamiento en {provider_type} con proveedor validado.")
            
            vm = provider.provisionar()
            
            
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
        
        return self.orchestrator.factory.get_available_providers()


class VMBuilderFactory:
    

    
    _builders = {
        'aws': AWSVMBuilder,
        'azure': AzureVMBuilder,
        'google': GoogleVMBuilder,
        'gcp': GoogleVMBuilder,  
        'onpremise': OnPremiseVMBuilder,
        'on-premise': OnPremiseVMBuilder  
    }

    @classmethod
    def create_builder(cls, provider_type: str) -> Optional[VMBuilder]:
        
        provider_type = provider_type.lower().strip()

        builder_class = cls._builders.get(provider_type)

        if builder_class is None:
            logger.error(f"Builder no soportado: {provider_type}")
            return None

        try:
            builder = builder_class()
            logger.info(f"Builder creado exitosamente: {provider_type}")
            return builder
        except Exception as e:
            logger.error(f"Error creando builder {provider_type}: {str(e)}")
            return None

    @classmethod
    def get_available_builders(cls) -> list:
        
        return list(cls._builders.keys())


class VMBuildingService:
    

    def __init__(self):
        self.builder_factory = VMBuilderFactory()

    def build_vm_with_config(self, provider_type: str,
                            build_config: Dict[str, Any]) -> ProvisioningResult:
        
        try:
            
            builder = self.builder_factory.create_builder(provider_type)

            if builder is None:
                available = self.builder_factory.get_available_builders()
                return ProvisioningResult(
                    success=False,
                    message=f"Builder para '{provider_type}' no soportado",
                    error_detail=f"Builders disponibles: {', '.join(available)}",
                    provider=provider_type
                )

           
            builder.reset()

            
            if 'name' in build_config and 'vm_type' in build_config:
                builder.set_basic_config(build_config['name'], build_config['vm_type'])

            
            if 'cpu' in build_config or 'ram' in build_config:
                builder.set_compute_resources(
                    cpu=build_config.get('cpu'),
                    ram=build_config.get('ram')
                )

            
            if 'disk_gb' in build_config:
                builder.set_storage(
                    size_gb=build_config['disk_gb'],
                    disk_type=build_config.get('disk_type')
                )

            
            if 'network_id' in build_config or 'cidr' in build_config:
                builder.set_network(
                    network_id=build_config.get('network_id'),
                    cidr=build_config.get('cidr')
                )

            
            if 'location' in build_config:
                builder.set_location(build_config['location'])

            
            if 'advanced_options' in build_config:
                builder.set_advanced_options(build_config['advanced_options'])

            
            vm = builder.build()

            logger.info(f"VM construida exitosamente con Builder - ID: {vm.vmId}")

            return ProvisioningResult(
                success=True,
                vm_id=vm.vmId,
                message=f"VM construida exitosamente en {provider_type} usando Builder Pattern",
                provider=provider_type,
                vm_details=vm.to_dict()
            )

        except Exception as e:
            logger.error(f"Error en construcción con builder: {str(e)}", exc_info=True)
            return ProvisioningResult(
                success=False,
                message="Error interno en la construcción",
                error_detail=str(e),
                provider=provider_type
            )

    def build_predefined_vm(self, provider_type: str,
                           preset: str,
                           name: str,
                           location: str = "us-east-1") -> ProvisioningResult:
        
        try:
            
            builder = self.builder_factory.create_builder(provider_type)

            if builder is None:
                return ProvisioningResult(
                    success=False,
                    message=f"Builder para '{provider_type}' no soportado",
                    provider=provider_type
                )

            
            director = VMDirector(builder)

            
            if preset == 'minimal':
                vm = director.build_minimal_vm(name)
            elif preset == 'standard':
                vm = director.build_standard_vm(name, location)
            elif preset == 'high-performance':
                vm = director.build_high_performance_vm(name, location)
            else:
                return ProvisioningResult(
                    success=False,
                    message=f"Preset '{preset}' no soportado",
                    error_detail="Presets disponibles: minimal, standard, high-performance",
                    provider=provider_type
                )

            logger.info(f"VM predefinida '{preset}' construida exitosamente - ID: {vm.vmId}")

            return ProvisioningResult(
                success=True,
                vm_id=vm.vmId,
                message=f"VM '{preset}' construida exitosamente en {provider_type}",
                provider=provider_type,
                vm_details=vm.to_dict()
            )

        except Exception as e:
            logger.error(f"Error en construcción predefinida: {str(e)}", exc_info=True)
            return ProvisioningResult(
                success=False,
                message="Error interno en la construcción predefinida",
                error_detail=str(e),
                provider=provider_type
            )
        
    def build_vm_type(self, provider_type: str, vm_type: str,
                      name: str, location: str, size: str = 'medium') -> ProvisioningResult:
        
        try:
            
            builder = self.builder_factory.create_builder(provider_type)

            if builder is None:
                available = self.builder_factory.get_available_builders()
                return ProvisioningResult(
                    success=False,
                    message=f"Builder para '{provider_type}' no soportado",
                    error_detail=f"Builders disponibles: {', '.join(available)}",
                    provider=provider_type
                )

            
            from domain.builder import VMDirector
            director = VMDirector(builder)

            
            if vm_type == 'standard':
                vm = director.build_standard_vm(name, location, size)
                type_description = "Standard VM (General Purpose)"
            elif vm_type == 'memory-optimized':
                vm = director.build_memory_optimized_vm(name, location, size)
                type_description = "VM Optimizada en Memoria (Memory-Optimized)"
            elif vm_type == 'disk-optimized':
                vm = director.build_disk_optimized_vm(name, location, size)
                type_description = "VM Optimizada en Disco (Compute-Optimized)"
            else:
                return ProvisioningResult(
                    success=False,
                    message=f"Tipo de VM '{vm_type}' no soportado",
                    error_detail="Tipos disponibles: standard, memory-optimized, disk-optimized",
                    provider=provider_type
                )

            logger.info(f"VM tipo '{vm_type}' construida exitosamente - ID: {vm.vmId}")
            logger.info(f"Especificaciones: {vm.instance_type} - {vm.vcpus} vCPUs, {vm.memoryGB}GB RAM")
            logger.info(f"Optimizaciones: Memory={vm.memoryOptimization}, Disk={vm.diskOptimization}")

            return ProvisioningResult(
                success=True,
                vm_id=vm.vmId,
                message=f"{type_description} construida exitosamente en {provider_type}",
                provider=provider_type,
                vm_details=vm.to_dict()
            )

        except ValueError as ve:
            
            logger.error(f"Error de validación: {str(ve)}")
            return ProvisioningResult(
                success=False,
                message="Error de validación",
                error_detail=str(ve),
                provider=provider_type
            )
        except Exception as e:
            logger.error(f"Error en construcción de VM tipo '{vm_type}': {str(e)}", exc_info=True)
            return ProvisioningResult(
                success=False,
                message="Error interno en la construcción",
                error_detail=str(e),
                provider=provider_type
            )