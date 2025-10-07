"""
OnPremise VM Builder - Concrete Builder para On-Premise
Implementa construcción paso a paso de VMs On-Premise
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
import logging

from domain.builder import VMBuilder
from domain.entities import MachineVirtual, VMStatus, Network, StorageDisk

logger = logging.getLogger(__name__)


class OnPremiseVMBuilder(VMBuilder):
    """
    Concrete Builder: Implementa construcción de VMs para On-Premise
    """

    def __init__(self):
        super().__init__()
        self._config = {
            'provider': 'on-premise',
            'cpu': 2,
            'ram': 4,
            'disk': 50,
            'vlan_id': 100,
            'storage_pool': 'default_pool',
            'raid_level': 5
        }

    def reset(self) -> 'OnPremiseVMBuilder':
        """Reinicia el builder"""
        self.__init__()
        return self

    def set_basic_config(self, name: str, vm_type: str) -> 'OnPremiseVMBuilder':
        """Configura parámetros básicos On-Premise"""
        self._config['name'] = name
        self._config['vm_type'] = vm_type

        # Configuración base según tipo
        type_configs = {
            'minimal': {'cpu': 1, 'ram': 1, 'disk': 20},
            'standard': {'cpu': 2, 'ram': 4, 'disk': 50},
            'high-performance': {'cpu': 8, 'ram': 32, 'disk': 500},
            'custom': {'cpu': 2, 'ram': 4, 'disk': 50}
        }

        config = type_configs.get(vm_type, type_configs['custom'])
        self._config.update(config)

        logger.info(f"OnPremise Builder: Configuración básica - Nombre: {name}, Tipo: {vm_type}")

        return self

    def set_compute_resources(self, cpu: Optional[int] = None,
                             ram: Optional[int] = None) -> 'OnPremiseVMBuilder':
        """Configura recursos de cómputo"""
        if cpu is not None:
            self._config['cpu'] = cpu
        if ram is not None:
            self._config['ram'] = ram

        logger.info(f"OnPremise Builder: Recursos de cómputo - CPU: {self._config['cpu']}, RAM: {self._config['ram']}GB")

        return self

    def set_storage(self, size_gb: int, disk_type: Optional[str] = None) -> 'OnPremiseVMBuilder':
        """Configura almacenamiento local"""
        self._config['disk'] = size_gb

        # Configurar RAID según tipo de disco
        raid_mapping = {
            'ssd': 10,
            'standard': 5,
            'performance': 0,
            'redundant': 6
        }

        if disk_type:
            self._config['raid_level'] = raid_mapping.get(disk_type, 5)
            self._config['disk_type'] = disk_type

        logger.info(f"OnPremise Builder: Almacenamiento - {size_gb}GB, RAID: {self._config['raid_level']}")

        return self

    def set_network(self, network_id: Optional[str] = None,
                   cidr: Optional[str] = None) -> 'OnPremiseVMBuilder':
        """Configura VLAN y red"""
        if network_id:
            try:
                self._config['vlan_id'] = int(network_id) if network_id.isdigit() else 100
            except:
                self._config['vlan_id'] = 100

        self._config['cidr_block'] = cidr or '192.168.1.0/24'
        logger.info(f"OnPremise Builder: Red - VLAN ID: {self._config['vlan_id']}")

        return self

    def set_location(self, location: str) -> 'OnPremiseVMBuilder':
        """Configura datacenter/rack"""
        self._config['datacenter'] = location
        logger.info(f"OnPremise Builder: Ubicación - Datacenter: {location}")

        return self

    def set_advanced_options(self, options: Dict[str, Any]) -> 'OnPremiseVMBuilder':
        """Configura opciones avanzadas On-Premise"""
        if 'storage_pool' in options:
            self._config['storage_pool'] = options['storage_pool']

        if 'raid_level' in options:
            self._config['raid_level'] = options['raid_level']

        if 'hypervisor' in options:
            self._config['hypervisor'] = options['hypervisor']

        if 'high_availability' in options:
            self._config['ha_enabled'] = options['high_availability']

        self._config.update(options)
        logger.info(f"OnPremise Builder: Opciones avanzadas configuradas")

        return self

    def build(self) -> MachineVirtual:
        """Construye la VM On-Premise con toda la configuración"""
        vm_id = f"onprem-{uuid.uuid4()}"

        # Crear Network
        vlan_id = self._config.get('vlan_id', 100)
        network = Network(
            networkId=f"vlan-{vlan_id}",
            name=f"prod-net-{vlan_id}",
            cidr_block=self._config.get('cidr_block', '192.168.1.0/24'),
            provider='on-premise'
        )

        # Crear Disk
        storage_pool = self._config.get('storage_pool', 'default_pool')
        raid_level = self._config.get('raid_level', 5)
        disk = StorageDisk(
            diskId=f"disk-{storage_pool}-{uuid.uuid4().hex[:4]}",
            name=f"storage-for-{storage_pool}",
            size_gb=self._config.get('disk', 50),
            disk_type=f"RAID-{raid_level}",
            provider='on-premise'
        )

        # Crear VM
        cpu = self._config.get('cpu', 2)
        ram = self._config.get('ram', 4)
        vm = MachineVirtual(
            vmId=vm_id,
            name=self._config.get('name', f"onprem-vm-{cpu}c-{ram}gb-{vm_id[:4]}"),
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider='on-premise',
            network=network,
            disks=[disk]
        )

        logger.info(f"OnPremise Builder: VM construida exitosamente - ID: {vm_id}")

        return vm
