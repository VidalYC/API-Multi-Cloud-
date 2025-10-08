import uuid
from datetime import datetime
from typing import Optional, Dict, Any
import logging

from domain.builder import VMBuilder
from domain.entities import MachineVirtual, VMStatus, Network, StorageDisk, VMInstanceType

logger = logging.getLogger(__name__)


class AzureVMBuilder(VMBuilder):
    """
    Builder concreto para Azure con parámetros del PDF (Página 3)
    """
    
    def __init__(self):
        super().__init__()
        self._config = {
            'provider': 'azure',
            'location': 'eastus',
            'resource_group': 'default-rg',
            'size': 'D2s_v3',  # Default: Standard VM
            'vcpus': 2,
            'memoryGB': 8,
            'disk_sku': 'Standard_LRS',
            'size_gb': 50,
            'memoryOptimization': False,
            'diskOptimization': False,
            'keyPairName': None,
            'firewallRules': None,
            'publicIP': None,
            'iops': None
        }

    def reset(self) -> 'AzureVMBuilder':
        self.__init__()
        return self

    def set_basic_config(self, name: str, vm_type: str) -> 'AzureVMBuilder':
        """
        Configura el tipo de VM según el PDF (Página 3)
        """
        self._config['name'] = name
        self._config['vm_type'] = vm_type
        
        # Mapeo de tipos de VM según PDF
        if vm_type == 'standard':
            self._config['size'] = 'D2s_v3'  # Standard / General Purpose
            self._config['memoryOptimization'] = False
            self._config['diskOptimization'] = False
        elif vm_type == 'memory-optimized':
            self._config['size'] = 'E2s_v3'  # Memory-Optimized
            self._config['memoryOptimization'] = True
            self._config['diskOptimization'] = False
        elif vm_type == 'disk-optimized':
            self._config['size'] = 'F2s_v2'  # Compute-Optimized
            self._config['memoryOptimization'] = False
            self._config['diskOptimization'] = True
        else:
            self._config['size'] = vm_type
        
        # Obtener especificaciones automáticas
        specs = VMInstanceType.get_specs('azure', self._config['size'])
        if specs:
            self._config['vcpus'] = specs['vcpus']
            self._config['memoryGB'] = specs['memoryGB']
        
        logger.info(f"Azure Builder: Configuración básica - Nombre: {name}, Tipo: {vm_type}, Size: {self._config['size']}")
        return self

    def set_instance_type(self, instance_type: str) -> 'AzureVMBuilder':
        """
        Configura un size específico de Azure
        Ejemplo: D2s_v3, E4s_v3, F8s_v2
        """
        self._config['size'] = instance_type
        
        specs = VMInstanceType.get_specs('azure', instance_type)
        if specs:
            self._config['vcpus'] = specs['vcpus']
            self._config['memoryGB'] = specs['memoryGB']
            logger.info(f"Azure Builder: Size configurado - {instance_type} ({specs['vcpus']} vCPUs, {specs['memoryGB']} GB RAM)")
        else:
            logger.warning(f"Azure Builder: Size '{instance_type}' no reconocido")
        
        return self

    def set_compute_resources(self, cpu: Optional[int] = None, ram: Optional[int] = None) -> 'AzureVMBuilder':
        """Configura recursos de cómputo"""
        if cpu is not None:
            self._config['vcpus'] = cpu
        if ram is not None:
            self._config['memoryGB'] = ram
        
        logger.info(f"Azure Builder: Recursos - CPU: {self._config['vcpus']}, RAM: {self._config['memoryGB']}GB")
        return self

    def set_storage(self, size_gb: int, disk_type: Optional[str] = None,
                    iops: Optional[int] = None) -> 'AzureVMBuilder':
        """Configura almacenamiento con IOPS opcional del PDF"""
        self._config['size_gb'] = size_gb
        
        disk_mapping = {
            'ssd': 'Premium_LRS',
            'standard': 'Standard_LRS',
            'ultra': 'UltraSSD_LRS'
        }
        self._config['disk_sku'] = disk_mapping.get(disk_type, 'Standard_LRS') if disk_type else 'Standard_LRS'
        
        if iops is not None:
            self._config['iops'] = iops
        
        logger.info(f"Azure Builder: Almacenamiento - {size_gb}GB, SKU: {self._config['disk_sku']}, IOPS: {iops}")
        return self

    def set_network(self, network_id: Optional[str] = None, cidr: Optional[str] = None,
                    firewall_rules: Optional[list] = None, public_ip: Optional[bool] = None) -> 'AzureVMBuilder':
        """Configura red con parámetros del PDF"""
        self._config['vnet_name'] = network_id or f"vnet-{self._config['resource_group']}"
        self._config['cidr_block'] = cidr or '10.1.0.0/16'
        
        if firewall_rules is not None:
            self._config['firewallRules'] = firewall_rules
        if public_ip is not None:
            self._config['publicIP'] = public_ip
        
        logger.info(f"Azure Builder: Red - VNet: {self._config['vnet_name']}")
        return self

    def set_location(self, location: str) -> 'AzureVMBuilder':
        """Configura la ubicación/región"""
        self._config['location'] = location
        logger.info(f"Azure Builder: Ubicación - {location}")
        return self

    def set_advanced_options(self, options: Dict[str, Any]) -> 'AzureVMBuilder':
        """Configura opciones avanzadas del PDF"""
        if 'memoryOptimization' in options:
            self._config['memoryOptimization'] = options['memoryOptimization']
        if 'diskOptimization' in options:
            self._config['diskOptimization'] = options['diskOptimization']
        if 'keyPairName' in options:
            self._config['keyPairName'] = options['keyPairName']
        if 'resource_group' in options:
            self._config['resource_group'] = options['resource_group']
        if 'optimized' in options:
            self._config['accelerated_networking'] = options['optimized']
        if 'monitoring' in options:
            self._config['boot_diagnostics'] = options['monitoring']
        
        self._config.update(options)
        logger.info("Azure Builder: Opciones avanzadas configuradas")
        return self

    def build(self) -> MachineVirtual:
        """Construye la VM con validación de región"""
        location = self._config.get('location', 'eastus')
        
        # Network con región obligatoria
        network = Network(
            networkId=self._config.get('vnet_name', f"vnet-{self._config['resource_group']}"),
            name=self._config.get('vnet_name', 'default-vnet'),
            cidr_block=self._config.get('cidr_block', '10.1.0.0/16'),
            provider='azure',
            region=location,  # ✅ OBLIGATORIO
            firewallRules=self._config.get('firewallRules'),
            publicIP=self._config.get('publicIP')
        )
        
        # Disk con región obligatoria
        disk = StorageDisk(
            diskId=f"disk-{uuid.uuid4().hex[:8]}",
            name=f"azure-disk-{self._config.get('disk_sku', 'Standard_LRS')}",
            size_gb=self._config.get('size_gb', 50),
            disk_type=self._config.get('disk_sku', 'Standard_LRS'),
            provider='azure',
            region=location,  # ✅ OBLIGATORIO
            iops=self._config.get('iops')
        )
        
        # ✅ VALIDACIÓN DE REGIÓN
        if network.region != disk.region:
            raise ValueError(f"Error de coherencia de región: Network={network.region}, Disk={disk.region}")
        
        vm_id = f"azure-{uuid.uuid4()}"
        
        vm = MachineVirtual(
            vmId=vm_id,
            name=self._config.get('name', f"azure-vm-{vm_id[:4]}"),
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider='azure',
            vcpus=self._config.get('vcpus', 2),
            memoryGB=self._config.get('memoryGB', 8),
            network=network,
            disks=[disk],
            memoryOptimization=self._config.get('memoryOptimization'),
            diskOptimization=self._config.get('diskOptimization'),
            keyPairName=self._config.get('keyPairName'),
            instance_type=self._config.get('size')
        )
        
        logger.info(f"Azure Builder: VM construida - ID: {vm_id}, Size: {vm.instance_type}, vCPUs: {vm.vcpus}, RAM: {vm.memoryGB}GB")
        return vm