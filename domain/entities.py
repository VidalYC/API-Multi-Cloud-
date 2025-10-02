from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List


class VMStatus(Enum):
    """Estados posibles de una máquina virtual"""
    PENDING = "pending"
    CREATING = "creating"
    RUNNING = "running"
    ERROR = "error"
    STOPPED = "stopped"


@dataclass
class Network:
    """Entidad que representa un recurso de Red."""
    networkId: str
    name: str
    cidr_block: str
    provider: str

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class StorageDisk:
    """Entidad que representa un recurso de Disco de Almacenamiento."""
    diskId: str
    name: str
    size_gb: int
    disk_type: str
    provider: str

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__


@dataclass
class MachineVirtual:
    """
    Entidad principal que representa una Máquina Virtual
    Aplicando SRP: Solo contiene datos y lógica de negocio básica
    """
    vmId: str
    name: str
    status: VMStatus
    createdAt: datetime
    provider: str
    network: Optional[Network] = None
    disks: Optional[List[StorageDisk]] = None
    
    def is_active(self) -> bool:
        """Verifica si la VM está activa"""
        return self.status == VMStatus.RUNNING
    
    def get_id(self) -> str:
        """Retorna el ID de la VM"""
        return self.vmId
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte la entidad a un diccionario para serialización"""
        return {
            "vmId": self.vmId,
            "name": self.name,
            "status": self.status.value,
            "createdAt": self.createdAt.isoformat(),
            "provider": self.provider,
            "network": self.network.to_dict() if self.network else None,
            "disks": [d.to_dict() for d in self.disks] if self.disks else []
        }


@dataclass
class ProvisioningResult:
    """
    Value Object que representa el resultado de un aprovisionamiento
    """
    success: bool
    vm_id: Optional[str] = None
    message: str = ""
    error_detail: Optional[str] = None
    provider: str = ""
    vm_details: Optional[Dict[str, Any]] = None
    
    def to_dict(self):
        """Convierte el resultado a diccionario para serialización"""
        return {
            "success": self.success,
            "vm_id": self.vm_id,
            "message": self.message,
            "error_detail": self.error_detail,
            "provider": self.provider,
            "vm_details": self.vm_details
        }