import uuid
from datetime import datetime
from typing import Dict, Any
import logging

from domain.interfaces import ProveedorAbstracto
from domain.entities import MachineVirtual, VMStatus, Network, StorageDisk

logger = logging.getLogger(__name__)


class AWS(ProveedorAbstracto):
    """
    Concrete Factory: Implementación para AWS. Crea una familia de productos AWS.
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        # Extraer configuración específica de AWS, con valores por defecto
        self.config = config
        self.instance_type = self.config.get('type', 't2.micro')
        self.region = self.config.get('region', 'us-east-1')
    
    def crear_vm(self) -> MachineVirtual:
        """Factory Method implementado para AWS"""
        vm_id = f"aws-{uuid.uuid4()}"
        
        logger.info(f"Creando VM en AWS - ID: {vm_id}, Tipo: {self.instance_type}, Región: {self.region}")
        
        # Simulación de creación en AWS
        vm = MachineVirtual(
            vmId=vm_id,
            name=f"aws-{self.instance_type}-{self.region}-{vm_id[:4]}",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="aws"
        )
        
        return vm

    def crear_network(self) -> Network:
        """Crea un recurso de red para AWS."""
        vpc_id = self.config.get('vpcId', f"vpc-{uuid.uuid4().hex[:8]}")
        logger.info(f"Creando Red en AWS - VPC ID: {vpc_id}")
        return Network(
            networkId=vpc_id,
            name=f"aws-net-{self.region}",
            cidr_block="10.0.0.0/16",
            provider="aws"
        )

    def crear_disk(self) -> StorageDisk:
        """Crea un recurso de disco para AWS."""
        disk_id = f"vol-{uuid.uuid4().hex[:12]}"
        size_gb = self.config.get('sizeGB', 20)
        volume_type = self.config.get('volumeType', 'gp2')
        logger.info(f"Creando Disco en AWS - ID: {disk_id}, Tamaño: {size_gb}GB, Tipo: {volume_type}")
        return StorageDisk(
            diskId=disk_id,
            name=f"aws-disk-{volume_type}",
            size_gb=size_gb,
            disk_type=volume_type,
            provider="aws"
        )