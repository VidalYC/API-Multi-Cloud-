"""
OnPremise VM Builder - Concrete Builder para On-Premise
Implementa construcción paso a paso de VMs On-Premise
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
import logging

from domain.builder import VMBuilder
from domain.entities import MachineVirtual, VMInstanceType, VMStatus, Network, StorageDisk

logger = logging.getLogger(__name__)


class OnPremiseVMBuilder(VMBuilder):
    """Builder concreto para OnPremise con parámetros del PDF (Página 4)"""

    def __init__(self):
        super().__init__()
        self._config = {
            'provider': 'on-premise',
            'datacenter': 'datacenter-1',
            'flavor': 'onprem-std1',
            'vcpus': 2,
            'memoryGB': 4,
            'disk': 50,
            'vlan_id': 100,
            'storage_pool': 'default_pool',
            'raid_level': 5,
            'memoryOptimization': False,
            'diskOptimization': False,
            'keyPairName': None,
            'firewallRules': None,
            'publicIP': None,
            'iops': None
        }

    def reset(self) -> 'OnPremiseVMBuilder':
        self.__init__()
        return self

    def set_basic_config(self, name: str, vm_type: str) -> 'OnPremiseVMBuilder':
        self._config['name'] = name
        self._config['vm_type'] = vm_type

        if vm_type == 'standard':
            self._config['flavor'] = 'onprem-std1'
            self._config['memoryOptimization'] = False
            self._config['diskOptimization'] = False
        elif vm_type == 'memory-optimized':
            self._config['flavor'] = 'onprem-mem1'
            self._config['memoryOptimization'] = True
            self._config['diskOptimization'] = False
        elif vm_type == 'disk-optimized':
            self._config['flavor'] = 'onprem-cpu1'
            self._config['memoryOptimization'] = False
            self._config['diskOptimization'] = True
        else:
            self._config['flavor'] = vm_type

        specs = VMInstanceType.get_specs('onpremise', self._config['flavor'])
        if specs:
            self._config['vcpus'] = specs['vcpus']
            self._config['memoryGB'] = specs['memoryGB']

        logger.info(f"OnPremise Builder: Config - {name}, Flavor: {self._config['flavor']}")
        return self

    def set_instance_type(self, instance_type: str) -> 'OnPremiseVMBuilder':
        self._config['flavor'] = instance_type
        specs = VMInstanceType.get_specs('onpremise', instance_type)
        if specs:
            self._config['vcpus'] = specs['vcpus']
            self._config['memoryGB'] = specs['memoryGB']
        return self

    def set_compute_resources(self, cpu: Optional[int] = None,
                              ram: Optional[int] = None) -> 'OnPremiseVMBuilder':
        if cpu is not None:
            self._config['vcpus'] = cpu
        if ram is not None:
            self._config['memoryGB'] = ram
        return self

    def set_storage(self, size_gb: int, disk_type: Optional[str] = None,
                    iops: Optional[int] = None) -> 'OnPremiseVMBuilder':
        self._config['disk'] = size_gb
        raid_mapping = {
            'ssd': 10,
            'standard': 5,
            'performance': 0,
            'redundant': 6
        }
        if disk_type:
            self._config['raid_level'] = raid_mapping.get(disk_type, 5)
            self._config['disk_type'] = disk_type
        if iops is not None:
            self._config['iops'] = iops
        return self

    def set_network(self, network_id: Optional[str] = None,
                    cidr: Optional[str] = None,
                    firewall_rules: Optional[list] = None,
                    public_ip: Optional[bool] = None) -> 'OnPremiseVMBuilder':
        if network_id:
            try:
                self._config['vlan_id'] = int(network_id) if network_id.isdigit() else 100
            except:
                self._config['vlan_id'] = 100
        self._config['cidr_block'] = cidr or '192.168.1.0/24'
        if firewall_rules is not None:
            self._config['firewallRules'] = firewall_rules
        if public_ip is not None:
            self._config['publicIP'] = public_ip
        return self

    def set_location(self, location: str) -> 'OnPremiseVMBuilder':
        self._config['datacenter'] = location
        return self

    def set_advanced_options(self, options: Dict[str, Any]) -> 'OnPremiseVMBuilder':
        if 'memoryOptimization' in options:
            self._config['memoryOptimization'] = options['memoryOptimization']
        if 'diskOptimization' in options:
            self._config['diskOptimization'] = options['diskOptimization']
        if 'keyPairName' in options:
            self._config['keyPairName'] = options['keyPairName']
        self._config.update(options)
        return self

    def build(self) -> MachineVirtual:
        datacenter = self._config.get('datacenter', 'datacenter-1')
        vlan_id = self._config.get('vlan_id', 100)

        network = Network(
            networkId=f"vlan-{vlan_id}",
            name=f"prod-net-{vlan_id}",
            cidr_block=self._config.get('cidr_block', '192.168.1.0/24'),
            provider='on-premise',
            region=datacenter,
            firewallRules=self._config.get('firewallRules'),
            publicIP=self._config.get('publicIP')
        )

        storage_pool = self._config.get('storage_pool', 'default_pool')
        raid_level = self._config.get('raid_level', 5)
        
        disk = StorageDisk(
            diskId=f"disk-{storage_pool}-{uuid.uuid4().hex[:4]}",
            name=f"storage-for-{storage_pool}",
            size_gb=self._config.get('disk', 50),
            disk_type=f"RAID-{raid_level}",
            provider='on-premise',
            region=datacenter,
            iops=self._config.get('iops')
        )

        if network.region != disk.region:
            raise ValueError(f"Error de coherencia: Network={network.region}, Disk={disk.region}")

        vm_id = f"onprem-{uuid.uuid4()}"

        vm = MachineVirtual(
            vmId=vm_id,
            name=self._config.get('name', f"onprem-vm-{vm_id[:4]}"),
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider='on-premise',
            vcpus=self._config.get('vcpus', 2),
            memoryGB=self._config.get('memoryGB', 4),
            network=network,
            disks=[disk],
            memoryOptimization=self._config.get('memoryOptimization'),
            diskOptimization=self._config.get('diskOptimization'),
            keyPairName=self._config.get('keyPairName'),
            instance_type=self._config.get('flavor')
        )

        logger.info(f"OnPremise Builder: VM construida - {vm_id}")
        return vm