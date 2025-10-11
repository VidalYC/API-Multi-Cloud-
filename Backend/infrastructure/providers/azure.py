import uuid
from datetime import datetime
from typing import Dict, Any
import logging

from domain.interfaces import ProveedorAbstracto
from domain.entities import MachineVirtual, VMStatus, Network, StorageDisk

logger = logging.getLogger(__name__)


class Azure(ProveedorAbstracto):
   
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.size = self.config.get('type', 'Standard_B1s')
        self.resource_group = self.config.get('resource_group', 'default-rg')
        self.location = self.config.get('location', 'eastus')
    
    def crear_vm(self) -> MachineVirtual:
        vm_id = f"azure-{uuid.uuid4()}"
        logger.info(f"Creando VM en Azure - ID: {vm_id}, Tamaño: {self.size}, Grupo: {self.resource_group}")
        
        # Mapeo de vCPU y memoria según size
        vcpu_ram_map = {
            'Standard_B1s': (1, 1),
            'Standard_B2s': (2, 4),
            'D2s_v3': (2, 8),
            'D4s_v3': (4, 16)
        }
        vcpus, memoryGB = vcpu_ram_map.get(self.size, (1, 1))
        
        vm = MachineVirtual(
            vmId=vm_id,
            name=f"azure-{self.size}-{vm_id[:4]}",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="azure",
            vcpus=vcpus,
            memoryGB=memoryGB,
            memoryOptimization=False,
            diskOptimization=False,
            keyPairName=self.config.get('keyPairName'),
            instance_type=self.size
        )
        return vm

    def crear_network(self) -> Network:
        vnet_name = self.config.get('virtualNetwork', f"vnet-{self.resource_group}")
        logger.info(f"Creando Red en Azure - VNet: {vnet_name}")
        
        return Network(
            networkId=vnet_name,
            name=vnet_name,
            cidr_block="10.1.0.0/16",
            provider="azure",
            region=self.location,  # ✅ OBLIGATORIO
            firewallRules=self.config.get('firewallRules'),
            publicIP=self.config.get('publicIP')
        )

    def crear_disk(self) -> StorageDisk:
        disk_name = f"disk-{uuid.uuid4().hex[:8]}"
        size_gb = self.config.get('sizeGB', 30)
        disk_sku = self.config.get('diskSku', 'Standard_LRS')
        logger.info(f"Creando Disco en Azure - Nombre: {disk_name}, Tamaño: {size_gb}GB, SKU: {disk_sku}")
        
        return StorageDisk(
            diskId=disk_name,
            name=disk_name,
            size_gb=size_gb,
            disk_type=disk_sku,
            provider="azure",
            region=self.location,  # ✅ OBLIGATORIO
            iops=self.config.get('iops')
        )