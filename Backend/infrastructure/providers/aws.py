import uuid
from datetime import datetime
from typing import Dict, Any
import logging

from domain.interfaces import ProveedorAbstracto
from domain.entities import MachineVirtual, VMStatus, Network, StorageDisk

logger = logging.getLogger(__name__)


class AWS(ProveedorAbstracto):
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.instance_type = self.config.get('type', 't2.micro')
        self.region = self.config.get('region', 'us-east-1')
    
    def crear_vm(self) -> MachineVirtual:
        vm_id = f"aws-{uuid.uuid4()}"
        logger.info(f"Creando VM en AWS - ID: {vm_id}, Tipo: {self.instance_type}, Región: {self.region}")
        
        # Valores por defecto de vCPU y memoria según instance type
        vcpu_ram_map = {
            't2.micro': (1, 1),
            't2.small': (1, 2),
            't2.medium': (2, 4),
            't3.medium': (2, 4),
            'm5.large': (2, 8),
            'm5.xlarge': (4, 16)
        }
        vcpus, memoryGB = vcpu_ram_map.get(self.instance_type, (2, 4))
        
        vm = MachineVirtual(
            vmId=vm_id,
            name=f"aws-{self.instance_type}-{self.region}-{vm_id[:4]}",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="aws",
            vcpus=vcpus,  # ✅ Parámetro obligatorio del PDF
            memoryGB=memoryGB,  # ✅ Parámetro obligatorio del PDF
            memoryOptimization=False,  # ✅ Parámetro opcional del PDF
            diskOptimization=False,  # ✅ Parámetro opcional del PDF
            keyPairName=self.config.get('keyPairName'),  # ✅ Parámetro opcional del PDF
            instance_type=self.instance_type
        )
        return vm

    def crear_network(self) -> Network:
        vpc_id = self.config.get('vpcId', f"vpc-{uuid.uuid4().hex[:8]}")
        logger.info(f"Creando Red en AWS - VPC ID: {vpc_id}")
        
        return Network(
            networkId=vpc_id,
            name=f"aws-net-{self.region}",
            cidr_block="10.0.0.0/16",
            provider="aws",
            region=self.region,  # ✅ OBLIGATORIO según PDF página 2
            firewallRules=self.config.get('firewallRules'),  # ✅ OPCIONAL según PDF
            publicIP=self.config.get('publicIP')  # ✅ OPCIONAL según PDF
        )

    def crear_disk(self) -> StorageDisk:
        disk_id = f"vol-{uuid.uuid4().hex[:12]}"
        size_gb = self.config.get('sizeGB', 20)
        volume_type = self.config.get('volumeType', 'gp2')
        logger.info(f"Creando Disco en AWS - ID: {disk_id}, Tamaño: {size_gb}GB, Tipo: {volume_type}")
        
        return StorageDisk(
            diskId=disk_id,
            name=f"aws-disk-{volume_type}",
            size_gb=size_gb,
            disk_type=volume_type,
            provider="aws",
            region=self.region,  # ✅ OBLIGATORIO según PDF página 2
            iops=self.config.get('iops')  # ✅ OPCIONAL según PDF
        )