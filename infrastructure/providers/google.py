import uuid
from datetime import datetime
from typing import Dict, Any
import logging

from domain.interfaces import ProveedorAbstracto
from domain.entities import MachineVirtual, VMStatus, Network, StorageDisk

logger = logging.getLogger(__name__)


class Google(ProveedorAbstracto):
    """
    Concrete Factory: Implementación para Google Cloud.
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.config = config
        self.machine_type = self.config.get('type', 'n1-standard-1')
        self.zone = self.config.get('zone', 'us-central1-a')
    
    def crear_vm(self) -> MachineVirtual:
        """Factory Method implementado para GCP"""
        vm_id = f"gcp-{uuid.uuid4()}"
        
        logger.info(f"Creando VM en Google Cloud - ID: {vm_id}, Tipo: {self.machine_type}, Zona: {self.zone}")
        
        vm = MachineVirtual(
            vmId=vm_id,
            name=f"gcp-{self.machine_type}-{self.zone}-{vm_id[:4]}",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="google"
        )
        
        return vm

    def crear_network(self) -> Network:
        """Crea un recurso de red para Google Cloud."""
        net_name = self.config.get('networkName', 'default-net')
        logger.info(f"Creando Red en GCP - Nombre: {net_name}")
        return Network(
            networkId=net_name,
            name=net_name,
            cidr_block="10.2.0.0/16",
            provider="google"
        )

    def crear_disk(self) -> StorageDisk:
        """Crea un recurso de disco para Google Cloud."""
        disk_name = f"disk-{uuid.uuid4().hex[:8]}"
        size_gb = self.config.get('sizeGB', 10)
        disk_type = self.config.get('diskType', 'pd-standard')
        logger.info(f"Creando Disco en GCP - Nombre: {disk_name}, Tamaño: {size_gb}GB, Tipo: {disk_type}")
        return StorageDisk(
            diskId=disk_name,
            name=disk_name,
            size_gb=size_gb,
            disk_type=disk_type,
            provider="google"
        )