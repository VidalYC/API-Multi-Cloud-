import uuid
from datetime import datetime
from typing import Dict, Any
import logging

from domain.interfaces import ProveedorAbstracto
from domain.entities import MachineVirtual, VMStatus, Network, StorageDisk

logger = logging.getLogger(__name__)


class Google(ProveedorAbstracto):
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.machine_type = self.config.get('type', 'n1-standard-1')
        self.zone = self.config.get('zone', 'us-central1-a')
    
    def crear_vm(self) -> MachineVirtual:
        vm_id = f"gcp-{uuid.uuid4()}"
        logger.info(f"Creando VM en Google Cloud - ID: {vm_id}, Tipo: {self.machine_type}, Zona: {self.zone}")
        
        vcpu_ram_map = {
            'f1-micro': (1, 0.6),
            'n1-standard-1': (1, 3.75),
            'n1-standard-2': (2, 7.5),
            'e2-standard-2': (2, 8)
        }
        vcpus, memoryGB = vcpu_ram_map.get(self.machine_type, (1, 4))
        
        vm = MachineVirtual(
            vmId=vm_id,
            name=f"gcp-{self.machine_type}-{self.zone}-{vm_id[:4]}",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="google",
            vcpus=int(vcpus),
            memoryGB=int(memoryGB),
            memoryOptimization=False,
            diskOptimization=False,
            keyPairName=self.config.get('keyPairName'),
            instance_type=self.machine_type
        )
        return vm

    def crear_network(self) -> Network:
        net_name = self.config.get('networkName', 'default-net')
        logger.info(f"Creando Red en GCP - Nombre: {net_name}")
        
        return Network(
            networkId=net_name,
            name=net_name,
            cidr_block="10.2.0.0/16",
            provider="google",
            region=self.zone,  # ✅ OBLIGATORIO
            firewallRules=self.config.get('firewallRules'),
            publicIP=self.config.get('publicIP')
        )

    def crear_disk(self) -> StorageDisk:
        disk_name = f"disk-{uuid.uuid4().hex[:8]}"
        size_gb = self.config.get('sizeGB', 10)
        disk_type = self.config.get('diskType', 'pd-standard')
        logger.info(f"Creando Disco en GCP - Nombre: {disk_name}, Tamaño: {size_gb}GB, Tipo: {disk_type}")
        
        return StorageDisk(
            diskId=disk_name,
            name=disk_name,
            size_gb=size_gb,
            disk_type=disk_type,
            provider="google",
            region=self.zone,  # ✅ OBLIGATORIO
            iops=self.config.get('iops')
        )