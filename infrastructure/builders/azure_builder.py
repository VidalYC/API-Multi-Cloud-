"""
Azure VM Builder - Concrete Builder para Azure
Implementa construcción paso a paso de VMs en Azure
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
import logging

from domain.builder import VMBuilder
from domain.entities import MachineVirtual, VMStatus, Network, StorageDisk

logger = logging.getLogger(__name__)


class AzureVMBuilder(VMBuilder):
    """
    Concrete Builder: Implementa construcción de VMs para Azure
    """

    def __init__(self):
        super().__init__()
        self._config = {
            'provider': 'azure',
            'resource_group': 'default-rg',
            'size': 'Standard_B1s',
            'disk_sku': 'Standard_LRS',
            'size_gb': 30
        }

    def reset(self) -> 'AzureVMBuilder':
        """Reinicia el builder"""
        self.__init__()
        return self

    def set_basic_config(self, name: str, vm_type: str) -> 'AzureVMBuilder':
        """Configura parámetros básicos de Azure"""
        self._config['name'] = name

        # Mapeo de tipos a VM sizes de Azure
        type_mapping = {
            'minimal': 'Standard_B1s',
            'standard': 'Standard_B2s',
            'high-performance': 'Standard_D8s_v3',
            'custom': 'Standard_B2ms'
        }

        self._config['size'] = type_mapping.get(vm_type, vm_type)
        logger.info(f"Azure Builder: Configuración básica - Nombre: {name}, Tamaño: {self._config['size']}")

        return self

    def set_compute_resources(self, cpu: Optional[int] = None,
                             ram: Optional[int] = None) -> 'AzureVMBuilder':
        """Configura recursos de cómputo"""
        if cpu or ram:
            # Mapeo aproximado de CPU/RAM a VM sizes
            if cpu and ram:
                if cpu <= 1 and ram <= 1:
                    self._config['size'] = 'Standard_B1s'
                elif cpu <= 2 and ram <= 4:
                    self._config['size'] = 'Standard_B2s'
                elif cpu <= 4 and ram <= 16:
                    self._config['size'] = 'Standard_D4s_v3'
                elif cpu <= 8 and ram <= 32:
                    self._config['size'] = 'Standard_D8s_v3'
                else:
                    self._config['size'] = 'Standard_D16s_v3'

            self._config['cpu'] = cpu
            self._config['ram'] = ram
            logger.info(f"Azure Builder: Recursos de cómputo - CPU: {cpu}, RAM: {ram}GB")

        return self

    def set_storage(self, size_gb: int, disk_type: Optional[str] = None) -> 'AzureVMBuilder':
        """Configura managed disks"""
        self._config['size_gb'] = size_gb

        # Mapeo de tipos de disco
        disk_mapping = {
            'ssd': 'Premium_LRS',
            'standard': 'Standard_LRS',
            'ultra': 'UltraSSD_LRS'
        }

        self._config['disk_sku'] = disk_mapping.get(disk_type, 'Standard_LRS') if disk_type else 'Standard_LRS'
        logger.info(f"Azure Builder: Almacenamiento - {size_gb}GB, SKU: {self._config['disk_sku']}")

        return self

    def set_network(self, network_id: Optional[str] = None,
                   cidr: Optional[str] = None) -> 'AzureVMBuilder':
        """Configura VNet y red"""
        self._config['vnet_name'] = network_id or f"vnet-{self._config['resource_group']}"
        self._config['cidr_block'] = cidr or '10.1.0.0/16'
        logger.info(f"Azure Builder: Red - VNet: {self._config['vnet_name']}")

        return self

    def set_location(self, location: str) -> 'AzureVMBuilder':
        """Configura región de Azure"""
        self._config['location'] = location
        logger.info(f"Azure Builder: Ubicación - Región: {location}")

        return self

    def set_advanced_options(self, options: Dict[str, Any]) -> 'AzureVMBuilder':
        """Configura opciones avanzadas de Azure"""
        if 'resource_group' in options:
            self._config['resource_group'] = options['resource_group']

        if 'optimized' in options:
            self._config['accelerated_networking'] = options['optimized']

        if 'monitoring' in options:
            self._config['boot_diagnostics'] = options['monitoring']

        self._config.update(options)
        logger.info(f"Azure Builder: Opciones avanzadas configuradas")

        return self

    def build(self) -> MachineVirtual:
        """Construye la VM de Azure con toda la configuración"""
        vm_id = f"azure-{uuid.uuid4()}"

        # Crear Network
        network = Network(
            networkId=self._config.get('vnet_name', f"vnet-{self._config['resource_group']}"),
            name=self._config.get('vnet_name', 'default-vnet'),
            cidr_block=self._config.get('cidr_block', '10.1.0.0/16'),
            provider='azure'
        )

        # Crear Disk
        disk = StorageDisk(
            diskId=f"disk-{uuid.uuid4().hex[:8]}",
            name=f"azure-disk-{self._config.get('disk_sku', 'Standard_LRS')}",
            size_gb=self._config.get('size_gb', 30),
            disk_type=self._config.get('disk_sku', 'Standard_LRS'),
            provider='azure'
        )

        # Crear VM
        vm = MachineVirtual(
            vmId=vm_id,
            name=self._config.get('name', f"azure-vm-{vm_id[:4]}"),
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider='azure',
            network=network,
            disks=[disk]
        )

        logger.info(f"Azure Builder: VM construida exitosamente - ID: {vm_id}")

        return vm
