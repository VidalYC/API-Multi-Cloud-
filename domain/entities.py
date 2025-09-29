from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class VMStatus(Enum):
    """Estados posibles de una máquina virtual"""
    PENDING = "pending"
    CREATING = "creating"
    RUNNING = "running"
    ERROR = "error"
    STOPPED = "stopped"


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
    
    def is_active(self) -> bool:
        """Verifica si la VM está activa"""
        return self.status == VMStatus.RUNNING
    
    def get_id(self) -> str:
        """Retorna el ID de la VM"""
        return self.vmId


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
    
    def to_dict(self):
        """Convierte el resultado a diccionario para serialización"""
        return {
            "success": self.success,
            "vm_id": self.vm_id,
            "message": self.message,
            "error_detail": self.error_detail,
            "provider": self.provider
        }