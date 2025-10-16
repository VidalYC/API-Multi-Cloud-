from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, Dict, Any, List
import copy
import uuid


class VMStatus(Enum):
    PENDING = "pending"
    CREATING = "creating"
    RUNNING = "running"
    ERROR = "error"
    STOPPED = "stopped"


@dataclass
class Network:
    """
    Network con parámetros del PDF (Página 2):
    - region (obligatorio)
    - firewallRules (opcional)
    - publicIP (opcional)
    """
    networkId: str
    name: str
    cidr_block: str
    provider: str
    region: str  # OBLIGATORIO según PDF
    firewallRules: Optional[List[str]] = None  # OPCIONAL según PDF
    publicIP: Optional[bool] = None  # OPCIONAL según PDF

    def to_dict(self) -> Dict[str, Any]:
        return {
            "networkId": self.networkId,
            "name": self.name,
            "cidr_block": self.cidr_block,
            "provider": self.provider,
            "region": self.region,
            "firewallRules": self.firewallRules,
            "publicIP": self.publicIP
        }

    def clone(self, new_name: Optional[str] = None) -> 'Network':
        """
        Patrón Prototype: Clona la red creando una copia profunda.
        Genera un nuevo networkId único y opcionalmente cambia el nombre.
        """
        cloned = copy.deepcopy(self)
        cloned.networkId = f"{self.provider}-net-{uuid.uuid4().hex[:8]}"
        if new_name:
            cloned.name = new_name
        else:
            cloned.name = f"{self.name}-clone"
        return cloned


@dataclass
class StorageDisk:
    """
    Storage con parámetros del PDF (Página 2):
    - region (obligatorio)
    - iops (opcional)
    """
    diskId: str
    name: str
    size_gb: int
    disk_type: str
    provider: str
    region: str  # OBLIGATORIO según PDF
    iops: Optional[int] = None  # OPCIONAL según PDF

    def to_dict(self) -> Dict[str, Any]:
        return {
            "diskId": self.diskId,
            "name": self.name,
            "size_gb": self.size_gb,
            "disk_type": self.disk_type,
            "provider": self.provider,
            "region": self.region,
            "iops": self.iops
        }

    def clone(self, new_name: Optional[str] = None, new_size: Optional[int] = None) -> 'StorageDisk':
        """
        Patrón Prototype: Clona el disco creando una copia profunda.
        Genera un nuevo diskId único y permite personalizar nombre y tamaño.
        """
        cloned = copy.deepcopy(self)
        cloned.diskId = f"{self.provider}-disk-{uuid.uuid4().hex[:8]}"
        if new_name:
            cloned.name = new_name
        else:
            cloned.name = f"{self.name}-clone"
        if new_size:
            cloned.size_gb = new_size
        return cloned


@dataclass
class MachineVirtual:
    """
    VirtualMachine con parámetros del PDF (Página 2):
    - provider (obligatorio)
    - vcpus (obligatorio)
    - memoryGB (obligatorio)
    - memoryOptimization (opcional)
    - diskOptimization (opcional)
    - keyPairName (opcional)
    """
    vmId: str
    name: str
    status: VMStatus
    createdAt: datetime
    provider: str  # OBLIGATORIO según PDF
    vcpus: int  # OBLIGATORIO según PDF
    memoryGB: int  # OBLIGATORIO según PDF
    network: Optional[Network] = None
    disks: Optional[List[StorageDisk]] = None
    memoryOptimization: Optional[bool] = None  # OPCIONAL según PDF
    diskOptimization: Optional[bool] = None  # OPCIONAL según PDF
    keyPairName: Optional[str] = None  # OPCIONAL según PDF
    instance_type: Optional[str] = None  # Tipo de instancia (t3.medium, D2s_v3, etc.)

    def is_active(self) -> bool:
        return self.status == VMStatus.RUNNING

    def get_id(self) -> str:
        return self.vmId

    def to_dict(self) -> Dict[str, Any]:
        return {
            "vmId": self.vmId,
            "name": self.name,
            "status": self.status.value,
            "createdAt": self.createdAt.isoformat(),
            "provider": self.provider,
            "vcpus": self.vcpus,
            "memoryGB": self.memoryGB,
            "memoryOptimization": self.memoryOptimization,
            "diskOptimization": self.diskOptimization,
            "keyPairName": self.keyPairName,
            "instance_type": self.instance_type,
            "network": self.network.to_dict() if self.network else None,
            "disks": [d.to_dict() for d in self.disks] if self.disks else []
        }

    def clone(self, new_name: Optional[str] = None, **customizations) -> 'MachineVirtual':
        """
        Patrón Prototype: Clona la VM creando una copia profunda.

        Args:
            new_name: Nuevo nombre para la VM clonada
            **customizations: Parámetros opcionales para personalizar el clon:
                - vcpus: Número de vCPUs
                - memoryGB: Memoria RAM en GB
                - region: Nueva región (también clonará network y disks con nueva región)
                - clone_network: Si False, no clona la red (default: True)
                - clone_disks: Si False, no clona los discos (default: True)

        Returns:
            Nueva instancia de MachineVirtual clonada
        """
        # Crear copia profunda de la VM
        cloned = copy.deepcopy(self)

        # Generar nuevo ID único
        cloned.vmId = f"{self.provider}-vm-{uuid.uuid4().hex[:8]}"

        # Establecer nombre
        if new_name:
            cloned.name = new_name
        else:
            cloned.name = f"{self.name}-clone"

        # Resetear timestamp y status
        cloned.createdAt = datetime.now()
        cloned.status = VMStatus.PENDING

        # Aplicar customizaciones opcionales
        if 'vcpus' in customizations:
            cloned.vcpus = customizations['vcpus']

        if 'memoryGB' in customizations:
            cloned.memoryGB = customizations['memoryGB']

        if 'instance_type' in customizations:
            cloned.instance_type = customizations['instance_type']

        if 'memoryOptimization' in customizations:
            cloned.memoryOptimization = customizations['memoryOptimization']

        if 'diskOptimization' in customizations:
            cloned.diskOptimization = customizations['diskOptimization']

        if 'keyPairName' in customizations:
            cloned.keyPairName = customizations['keyPairName']

        # Clonar network si existe y no se especifica lo contrario
        clone_network = customizations.get('clone_network', True)
        new_region = customizations.get('region')

        if cloned.network and clone_network:
            network_name = f"{cloned.name}-network"
            cloned.network = cloned.network.clone(new_name=network_name)
            if new_region:
                cloned.network.region = new_region

        # Clonar disks si existen y no se especifica lo contrario
        clone_disks = customizations.get('clone_disks', True)

        if cloned.disks and clone_disks:
            cloned_disks = []
            for idx, disk in enumerate(cloned.disks):
                disk_name = f"{cloned.name}-disk-{idx}"
                cloned_disk = disk.clone(new_name=disk_name)
                if new_region:
                    cloned_disk.region = new_region
                cloned_disks.append(cloned_disk)
            cloned.disks = cloned_disks

        return cloned

    def customize(self, **kwargs) -> 'MachineVirtual':
        """
        Permite personalizar atributos de la VM después de crearla.
        Útil para modificar configuraciones específicas sin reconstruir toda la VM.

        Returns:
            La misma instancia modificada (patrón Fluent Interface)
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        return self


@dataclass
class ProvisioningResult:
    success: bool
    vm_id: Optional[str] = None
    message: str = ""
    error_detail: Optional[str] = None
    provider: str = ""
    vm_details: Optional[Dict[str, Any]] = None

    def to_dict(self):
        return {
            "success": self.success,
            "vm_id": self.vm_id,
            "message": self.message,
            "error_detail": self.error_detail,
            "provider": self.provider,
            "vm_details": self.vm_details
        }


# Tipos de máquina según el PDF (Páginas 2-4)
class VMInstanceType:
    """
    Tipos de instancia con vCPU y memoria RAM exactos según el PDF
    """
    
    # Amazon AWS (Página 2)
    AWS_TYPES = {
        # General Purpose (Standard)
        "t3.medium": {"vcpus": 2, "memoryGB": 4},
        "m5.large": {"vcpus": 2, "memoryGB": 8},
        "m5.xlarge": {"vcpus": 4, "memoryGB": 16},
        
        # Memory-Optimized
        "r5.large": {"vcpus": 2, "memoryGB": 16},
        "r5.xlarge": {"vcpus": 4, "memoryGB": 32},
        "r5.2xlarge": {"vcpus": 8, "memoryGB": 64},
        
        # Compute-Optimized (Disk-Optimized según PDF)
        "c5.large": {"vcpus": 2, "memoryGB": 4},
        "c5.xlarge": {"vcpus": 4, "memoryGB": 8},
        "c5.2xlarge": {"vcpus": 8, "memoryGB": 16}
    }
    
    # Microsoft Azure (Página 3)
    AZURE_TYPES = {
        # Standard / General Purpose
        "D2s_v3": {"vcpus": 2, "memoryGB": 8},
        "D4s_v3": {"vcpus": 4, "memoryGB": 16},
        "D8s_v3": {"vcpus": 8, "memoryGB": 32},
        
        # Memory-Optimized
        "E2s_v3": {"vcpus": 2, "memoryGB": 16},
        "E4s_v3": {"vcpus": 4, "memoryGB": 32},
        "E8s_v3": {"vcpus": 8, "memoryGB": 64},
        
        # Compute-Optimized (Disk-Optimized)
        "F2s_v2": {"vcpus": 2, "memoryGB": 4},
        "F4s_v2": {"vcpus": 4, "memoryGB": 8},
        "F8s_v2": {"vcpus": 8, "memoryGB": 16}
    }
    
    # Google Cloud Platform (Página 3)
    GCP_TYPES = {
        # Standard / General Purpose
        "e2-standard-2": {"vcpus": 2, "memoryGB": 8},
        "e2-standard-4": {"vcpus": 4, "memoryGB": 16},
        "e2-standard-8": {"vcpus": 8, "memoryGB": 32},
        
        # Memory-Optimized
        "n2-highmem-2": {"vcpus": 2, "memoryGB": 16},
        "n2-highmem-4": {"vcpus": 4, "memoryGB": 32},
        "n2-highmem-8": {"vcpus": 8, "memoryGB": 64},
        
        # Compute-Optimized (High CPU / Disk-Optimized)
        "n2-highcpu-2": {"vcpus": 2, "memoryGB": 2},
        "n2-highcpu-4": {"vcpus": 4, "memoryGB": 4},
        "n2-highcpu-8": {"vcpus": 8, "memoryGB": 8}
    }
    
    # On-Premise (Página 4)
    ONPREMISE_TYPES = {
        # Standard
        "onprem-std1": {"vcpus": 2, "memoryGB": 4},
        "onprem-std2": {"vcpus": 4, "memoryGB": 8},
        "onprem-std3": {"vcpus": 8, "memoryGB": 16},
        
        # Memory-Optimized
        "onprem-mem1": {"vcpus": 2, "memoryGB": 16},
        "onprem-mem2": {"vcpus": 4, "memoryGB": 32},
        "onprem-mem3": {"vcpus": 8, "memoryGB": 64},
        
        # Compute-Optimized (Disk-Optimized)
        "onprem-cpu1": {"vcpus": 2, "memoryGB": 2},
        "onprem-cpu2": {"vcpus": 4, "memoryGB": 4},
        "onprem-cpu3": {"vcpus": 8, "memoryGB": 8}
    }
    
    @classmethod
    def get_specs(cls, provider: str, instance_type: str) -> Optional[Dict[str, int]]:
        """
        Obtiene las especificaciones (vCPU, memoryGB) para un tipo de instancia
        """
        provider_map = {
            'aws': cls.AWS_TYPES,
            'azure': cls.AZURE_TYPES,
            'google': cls.GCP_TYPES,
            'gcp': cls.GCP_TYPES,
            'onpremise': cls.ONPREMISE_TYPES,
            'on-premise': cls.ONPREMISE_TYPES
        }
        
        types_dict = provider_map.get(provider.lower())
        if types_dict:
            return types_dict.get(instance_type)
        return None
    
    @classmethod
    def get_instance_by_type(cls, provider: str, vm_type: str, size: str = "medium") -> Optional[str]:
        """
        Obtiene el instance_type según el tipo de VM y tamaño
        
        vm_type: 'standard', 'memory-optimized', 'disk-optimized'
        size: 'small', 'medium', 'large'
        """
        provider = provider.lower()
        size_map = {'small': 0, 'medium': 1, 'large': 2}
        idx = size_map.get(size, 1)
        
        if provider == 'aws':
            if vm_type == 'standard':
                aws_keys = list(cls.AWS_TYPES.keys())
                return aws_keys[0:3][idx] if idx < len(aws_keys[0:3]) else None
            elif vm_type == 'memory-optimized':
                aws_keys = list(cls.AWS_TYPES.keys())
                return aws_keys[3:6][idx] if idx < len(aws_keys[3:6]) else None
            elif vm_type == 'disk-optimized':
                aws_keys = list(cls.AWS_TYPES.keys())
                return aws_keys[6:9][idx] if idx < len(aws_keys[6:9]) else None

        elif provider in ['azure']:
            if vm_type == 'standard':
                azure_keys = list(cls.AZURE_TYPES.keys())
                return azure_keys[0:3][idx] if idx < len(azure_keys[0:3]) else None
            elif vm_type == 'memory-optimized':
                azure_keys = list(cls.AZURE_TYPES.keys())
                return azure_keys[3:6][idx] if idx < len(azure_keys[3:6]) else None
            elif vm_type == 'disk-optimized':
                azure_keys = list(cls.AZURE_TYPES.keys())
                return azure_keys[6:9][idx] if idx < len(azure_keys[6:9]) else None

        elif provider in ['google', 'gcp']:
            if vm_type == 'standard':
                gcp_keys = list(cls.GCP_TYPES.keys())
                return gcp_keys[0:3][idx] if idx < len(gcp_keys[0:3]) else None
            elif vm_type == 'memory-optimized':
                gcp_keys = list(cls.GCP_TYPES.keys())
                return gcp_keys[3:6][idx] if idx < len(gcp_keys[3:6]) else None
            elif vm_type == 'disk-optimized':
                gcp_keys = list(cls.GCP_TYPES.keys())
                return gcp_keys[6:9][idx] if idx < len(gcp_keys[6:9]) else None

        elif provider in ['onpremise', 'on-premise']:
            if vm_type == 'standard':
                onprem_keys = list(cls.ONPREMISE_TYPES.keys())
                return onprem_keys[0:3][idx] if idx < len(onprem_keys[0:3]) else None
            elif vm_type == 'memory-optimized':
                onprem_keys = list(cls.ONPREMISE_TYPES.keys())
                return onprem_keys[3:6][idx] if idx < len(onprem_keys[3:6]) else None
            elif vm_type == 'disk-optimized':
                onprem_keys = list(cls.ONPREMISE_TYPES.keys())
                return onprem_keys[6:9][idx] if idx < len(onprem_keys[6:9]) else None

        return None