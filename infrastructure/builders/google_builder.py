import uuid
from datetime import datetime
from typing import Optional, Dict, Any
import logging

from domain.builder import VMBuilder
from domain.entities import MachineVirtual, VMStatus, Network, StorageDisk, VMInstanceType

logger = logging.getLogger(__name__)


class GoogleVMBuilder(VMBuilder):
    """Builder concreto para Google Cloud con parámetros del PDF (Página 3)"""
    
    def __init__(self):
        super().__init__()
        self._config = {
            'provider': 'google',
            'zone': 'us-central1-a',
            'machine_type': 'e2-standard-2',
            'vcpus': 2,
            'memoryGB': 8,
            'disk_type': 'pd-standard',
            'size_gb': 50,
            'memoryOptimization': False,
            'diskOptimization': False,
            'keyPairName': None,
            'firewallRules': None,
            'publicIP': None,
            'iops': None
        }

    def reset(self) -> 'GoogleVMBuilder':
        self.__init__()
        return self

    def set_basic_config(self, name: str, vm_type: str) -> 'GoogleVMBuilder':
        self._config['name'] = name
        self._config['vm_type'] = vm_type
        
        if vm_type == 'standard':
            self._config['machine_type'] = 'e2-standard-2'
            self._config['memoryOptimization'] = False
            self._config['diskOptimization'] = False
        elif vm_type == 'memory-optimized':
            self._config['machine_type'] = 'n2-highmem-2'
            self._config['memoryOptimization'] = True
            self._config['diskOptimization'] = False
        elif vm_type == 'disk-optimized':
            self._config['machine_type'] = 'n2-highcpu-2'
            self._config['memoryOptimization'] = False
            self._config['diskOptimization'] = True
        else:
            self._config['machine_type'] = vm_type
        
        specs = VMInstanceType.get_specs('google', self._config['machine_type'])
        if specs:
            self._config['vcpus'] = specs['vcpus']
            self._config['memoryGB'] = specs['memoryGB']
        
        logger.info(f"Google Builder: Config - {name}, Type: {vm_type}, Machine: {self._config['machine_type']}")
        return self

    def set_instance_type(self, instance_type: str) -> 'GoogleVMBuilder':
        self._config['machine_type'] = instance_type
        specs = VMInstanceType.get_specs('google', instance_type)
        if specs:
            self._config['vcpus'] = specs['vcpus']
            self._config['memoryGB'] = specs['memoryGB']
        return self

    def set_compute_resources(self, cpu: Optional[int] = None, ram: Optional[int] = None) -> 'GoogleVMBuilder':
        if cpu is not None:
            self._config['vcpus'] = cpu
        if ram is not None:
            self._config['memoryGB'] = ram
        return self

    def set_storage(self, size_gb: int, disk_type: Optional[str] = None,
                    iops: Optional[int] = None) -> 'GoogleVMBuilder':
        self._config['size_gb'] = size_gb
        disk_mapping = {
            'ssd': 'pd-ssd',
            'standard': 'pd-standard',
            'balanced': 'pd-balanced'
        }
        self._config['disk_type'] = disk_mapping.get(disk_type, 'pd-standard') if disk_type else 'pd-standard'
        if iops is not None:
            self._config['iops'] = iops
        return self

    def set_network(self, network_id: Optional[str] = None, cidr: Optional[str] = None,
                    firewall_rules: Optional[list] = None, public_ip: Optional[bool] = None) -> 'GoogleVMBuilder':
        self._config['network_name'] = network_id or 'default-net'
        self._config['cidr_block'] = cidr or '10.2.0.0/16'
        if firewall_rules is not None:
            self._config['firewallRules'] = firewall_rules
        if public_ip is not None:
            self._config['publicIP'] = public_ip
        return self

    def set_location(self, location: str) -> 'GoogleVMBuilder':
        self._config['zone'] = location
        return self

    def set_advanced_options(self, options: Dict[str, Any]) -> 'GoogleVMBuilder':
        if 'memoryOptimization' in options:
            self._config['memoryOptimization'] = options['memoryOptimization']
        if 'diskOptimization' in options:
            self._config['diskOptimization'] = options['diskOptimization']
        if 'keyPairName' in options:
            self._config['keyPairName'] = options['keyPairName']
        self._config.update(options)
        return self

    def build(self) -> MachineVirtual:
        zone = self._config.get('zone', 'us-central1-a')
        
        network = Network(
            networkId=self._config.get('network_name', 'default-net'),
            name=self._config.get('network_name', 'default-net'),
            cidr_block=self._config.get('cidr_block', '10.2.0.0/16'),
            provider='google',
            region=zone,
            firewallRules=self._config.get('firewallRules'),
            publicIP=self._config.get('publicIP')
        )
        
        disk = StorageDisk(
            diskId=f"disk-{uuid.uuid4().hex[:8]}",
            name=f"gcp-disk-{self._config.get('disk_type', 'pd-standard')}",
            size_gb=self._config.get('size_gb', 50),
            disk_type=self._config.get('disk_type', 'pd-standard'),
            provider='google',
            region=zone,
            iops=self._config.get('iops')
        )
        
        if network.region != disk.region:
            raise ValueError(f"Error de coherencia: Network={network.region}, Disk={disk.region}")
        
        vm_id = f"gcp-{uuid.uuid4()}"
        
        vm = MachineVirtual(
            vmId=vm_id,
            name=self._config.get('name', f"gcp-vm-{vm_id[:4]}"),
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider='google',
            vcpus=self._config.get('vcpus', 2),
            memoryGB=self._config.get('memoryGB', 8),
            network=network,
            disks=[disk],
            memoryOptimization=self._config.get('memoryOptimization'),
            diskOptimization=self._config.get('diskOptimization'),
            keyPairName=self._config.get('keyPairName'),
            instance_type=self._config.get('machine_type')
        )
        
        logger.info(f"Google Builder: VM construida - {vm_id}")
        return vm