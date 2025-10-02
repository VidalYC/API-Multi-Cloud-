import uuid
from datetime import datetime
from typing import Dict, Any
import logging

from domain.interfaces import ProveedorAbstracto
from domain.entities import MachineVirtual, VMStatus, Network, StorageDisk

logger = logging.getLogger(__name__)


class Azure(ProveedorAbstracto):
    """
    Concrete Factory: Implementación para Azure.
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.size = self.config.get('type', 'Standard_B1s')
        self.resource_group = self.config.get('resource_group', 'default-rg')
    
    def crear_vm(self) -> MachineVirtual:
        """Factory Method implementado para Azure"""
        vm_id = f"azure-{uuid.uuid4()}"
        
        logger.info(f"Creando VM en Azure - ID: {vm_id}, Tamaño: {self.size}, Grupo: {self.resource_group}")
        
        vm = MachineVirtual(
            vmId=vm_id,
            name=f"azure-{self.size}-{vm_id[:4]}",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="azure"
        )
        
        return vm

    def crear_network(self) -> Network:
        """Crea un recurso de red para Azure."""
        vnet_name = self.config.get('virtualNetwork', f"vnet-{self.resource_group}")
        logger.info(f"Creando Red en Azure - VNet: {vnet_name}")
        return Network(
            networkId=vnet_name,
            name=vnet_name,
            cidr_block="10.1.0.0/16",
            provider="azure"
        )

    def crear_disk(self) -> StorageDisk:
        """Crea un recurso de disco para Azure."""
        disk_name = f"disk-{uuid.uuid4().hex[:8]}"
        size_gb = self.config.get('sizeGB', 30)
        disk_sku = self.config.get('diskSku', 'Standard_LRS')
        logger.info(f"Creando Disco en Azure - Nombre: {disk_name}, Tamaño: {size_gb}GB, SKU: {disk_sku}")
        return StorageDisk(
            diskId=disk_name,
            name=disk_name,
            size_gb=size_gb,
            disk_type=disk_sku,
            provider="azure"
        )