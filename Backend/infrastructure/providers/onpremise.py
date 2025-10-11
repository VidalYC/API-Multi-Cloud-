import uuid
from datetime import datetime
from typing import Dict, Any
import logging

from domain.interfaces import ProveedorAbstracto
from domain.entities import MachineVirtual, VMStatus, Network, StorageDisk

logger = logging.getLogger(__name__)


class OnPremise(ProveedorAbstracto):
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.cpu = self.config.get('cpu', 2)
        self.ram = self.config.get('ram', 4)
        self.disk = self.config.get('disk', 50)
        self.datacenter = self.config.get('datacenter', 'datacenter-1')
    
    def crear_vm(self) -> MachineVirtual:
        vm_id = f"onprem-{uuid.uuid4()}"
        logger.info(f"Creando VM On-Premise - ID: {vm_id}, CPU: {self.cpu}, RAM: {self.ram}GB, Disco: {self.disk}GB")
        
        vm = MachineVirtual(
            vmId=vm_id,
            name=f"onprem-vm-{self.cpu}c-{self.ram}gb-{vm_id[:4]}",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="on-premise",
            vcpus=self.cpu,
            memoryGB=self.ram,
            memoryOptimization=False,
            diskOptimization=False,
            keyPairName=self.config.get('keyPairName'),
            instance_type=f"custom-{self.cpu}cpu-{self.ram}gb"
        )
        return vm

    def crear_network(self) -> Network:
        vlan_id = self.config.get('vlanId', 100)
        logger.info(f"Configurando Red On-Premise - VLAN ID: {vlan_id}")
        
        return Network(
            networkId=f"vlan-{vlan_id}",
            name=f"prod-net-{vlan_id}",
            cidr_block="192.168.1.0/24",
            provider="on-premise",
            region=self.datacenter,  # ✅ OBLIGATORIO
            firewallRules=self.config.get('firewallRules'),
            publicIP=self.config.get('publicIP')
        )

    def crear_disk(self) -> StorageDisk:
        pool_name = self.config.get('storagePool', 'default_pool')
        size_gb = self.config.get('disk', 100)
        raid_level = self.config.get('raidLevel', 5)
        logger.info(f"Asignando Disco On-Premise - Pool: {pool_name}, Tamaño: {size_gb}GB, RAID: {raid_level}")
        
        return StorageDisk(
            diskId=f"disk-{pool_name}-{uuid.uuid4().hex[:4]}",
            name=f"storage-for-{pool_name}",
            size_gb=size_gb,
            disk_type=f"RAID-{raid_level}",
            provider="on-premise",
            region=self.datacenter,  # ✅ OBLIGATORIO
            iops=self.config.get('iops')
        )