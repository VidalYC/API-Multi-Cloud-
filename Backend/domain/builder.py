from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from domain.entities import MachineVirtual, Network, StorageDisk, VMInstanceType


class VMBuilder(ABC):
    """
    Builder abstracto para construcción de VMs
    Permite construcción paso a paso con validación de región
    """
    def __init__(self):
        self._vm: Optional[MachineVirtual] = None
        self._network: Optional[Network] = None
        self._disk: Optional[StorageDisk] = None
        self._config: Dict[str, Any] = {}

    @abstractmethod
    def reset(self) -> 'VMBuilder':
        """Reinicia el builder"""
        pass

    @abstractmethod
    def set_basic_config(self, name: str, vm_type: str) -> 'VMBuilder':
        """
        Configura nombre y tipo de VM
        vm_type: 'standard', 'memory-optimized', 'disk-optimized'
        """
        pass

    @abstractmethod
    def set_compute_resources(self, cpu: Optional[int] = None,
                              ram: Optional[int] = None) -> 'VMBuilder':
        """Configura recursos de cómputo (vCPU y memoria)"""
        pass

    @abstractmethod
    def set_storage(self, size_gb: int, disk_type: Optional[str] = None,
                    iops: Optional[int] = None) -> 'VMBuilder':
        """
        Configura almacenamiento
        iops: Parámetro opcional del PDF
        """
        pass

    @abstractmethod
    def set_network(self, network_id: Optional[str] = None,
                    cidr: Optional[str] = None,
                    firewall_rules: Optional[list] = None,
                    public_ip: Optional[bool] = None) -> 'VMBuilder':
        """
        Configura red
        firewall_rules: Parámetro opcional del PDF
        public_ip: Parámetro opcional del PDF
        """
        pass

    @abstractmethod
    def set_location(self, location: str) -> 'VMBuilder':
        """Configura ubicación/región"""
        pass

    @abstractmethod
    def set_advanced_options(self, options: Dict[str, Any]) -> 'VMBuilder':
        """
        Configura opciones avanzadas
        memoryOptimization, diskOptimization, keyPairName del PDF
        """
        pass

    @abstractmethod
    def set_instance_type(self, instance_type: str) -> 'VMBuilder':
        """
        Configura el tipo de instancia exacto del proveedor
        Ejemplo: t3.medium, D2s_v3, e2-standard-2, onprem-std1
        """
        pass

    @abstractmethod
    def build(self) -> MachineVirtual:
        """Construye la VM final con validación de región"""
        pass

    def get_config(self) -> Dict[str, Any]:
        return self._config.copy()


class VMDirector:
    """
    Director que define algoritmos de construcción para los 3 tipos de VM del PDF:
    1. Standard VM
    2. VM Optimizada en Memoria
    3. VM Optimizada en Disco
    """
    
    def __init__(self, builder: VMBuilder):
        self._builder = builder

    def change_builder(self, builder: VMBuilder) -> None:
        """Cambia el builder para usar otro proveedor"""
        self._builder = builder

    # ===== 1. STANDARD VM (según PDF) =====
    def build_standard_vm(self, name: str, location: str, size: str = "medium") -> MachineVirtual:
        """
        Construye una Standard VM (General Purpose)
        
        Según PDF página 2-4:
        - AWS: t3.medium (2 vCPU, 4 GiB), m5.large (2 vCPU, 8 GiB), m5.xlarge (4 vCPU, 16 GiB)
        - Azure: D2s_v3 (2 vCPU, 8 GiB), D4s_v3 (4 vCPU, 16 GiB), D8s_v3 (8 vCPU, 32 GiB)
        - GCP: e2-standard-2 (2 vCPU, 8 GiB), e2-standard-4 (4 vCPU, 16 GiB), e2-standard-8 (8 vCPU, 32 GiB)
        - OnPremise: onprem-std1 (2 vCPU, 4 GiB), onprem-std2 (4 vCPU, 8 GiB), onprem-std3 (8 vCPU, 16 GiB)
        
        Args:
            name: Nombre de la VM
            location: Región/ubicación
            size: Tamaño ('small', 'medium', 'large')
        """
        return (self._builder
                .reset()
                .set_basic_config(name, "standard")
                .set_location(location)
                .set_storage(size_gb=50, disk_type="standard")
                .set_network(public_ip=True, firewall_rules=["HTTP", "HTTPS"])
                .set_advanced_options({
                    "memoryOptimization": False,
                    "diskOptimization": False
                })
                .build())

    # ===== 2. VM OPTIMIZADA EN MEMORIA (según PDF) =====
    def build_memory_optimized_vm(self, name: str, location: str, size: str = "medium") -> MachineVirtual:
        """
        Construye una VM Optimizada en Memoria (Memory-Optimized)
        
        Según PDF página 2-4:
        - AWS: r5.large (2 vCPU, 16 GiB), r5.xlarge (4 vCPU, 32 GiB), r5.2xlarge (8 vCPU, 64 GiB)
        - Azure: E2s_v3 (2 vCPU, 16 GiB), E4s_v3 (4 vCPU, 32 GiB), E8s_v3 (8 vCPU, 64 GiB)
        - GCP: n2-highmem-2 (2 vCPU, 16 GiB), n2-highmem-4 (4 vCPU, 32 GiB), n2-highmem-8 (8 vCPU, 64 GiB)
        - OnPremise: onprem-mem1 (2 vCPU, 16 GiB), onprem-mem2 (4 vCPU, 32 GiB), onprem-mem3 (8 vCPU, 64 GiB)
        
        Args:
            name: Nombre de la VM
            location: Región/ubicación
            size: Tamaño ('small', 'medium', 'large')
        """
        return (self._builder
                .reset()
                .set_basic_config(name, "memory-optimized")
                .set_location(location)
                .set_storage(size_gb=100, disk_type="standard")
                .set_network(public_ip=False, firewall_rules=["SSH"])
                .set_advanced_options({
                    "memoryOptimization": True,  # ✅ Optimización de memoria activada
                    "diskOptimization": False,
                    "keyPairName": "memory-key"
                })
                .build())

    # ===== 3. VM OPTIMIZADA EN DISCO (según PDF) =====
    def build_disk_optimized_vm(self, name: str, location: str, size: str = "medium") -> MachineVirtual:
        """
        Construye una VM Optimizada en Disco (Compute-Optimized / High CPU)
        
        Según PDF página 2-4:
        - AWS: c5.large (2 vCPU, 4 GiB), c5.xlarge (4 vCPU, 8 GiB), c5.2xlarge (8 vCPU, 16 GiB)
        - Azure: F2s_v2 (2 vCPU, 4 GiB), F4s_v2 (4 vCPU, 8 GiB), F8s_v2 (8 vCPU, 16 GiB)
        - GCP: n2-highcpu-2 (2 vCPU, 2 GiB), n2-highcpu-4 (4 vCPU, 4 GiB), n2-highcpu-8 (8 vCPU, 8 GiB)
        - OnPremise: onprem-cpu1 (2 vCPU, 2 GiB), onprem-cpu2 (4 vCPU, 4 GiB), onprem-cpu3 (8 vCPU, 8 GiB)
        
        Args:
            name: Nombre de la VM
            location: Región/ubicación
            size: Tamaño ('small', 'medium', 'large')
        """
        return (self._builder
                .reset()
                .set_basic_config(name, "disk-optimized")
                .set_location(location)
                .set_storage(size_gb=500, disk_type="ssd", iops=3000)  # ✅ IOPS del PDF
                .set_network(public_ip=True, firewall_rules=["HTTP", "HTTPS", "SSH"])
                .set_advanced_options({
                    "memoryOptimization": False,
                    "diskOptimization": True,  # ✅ Optimización de disco activada
                    "keyPairName": "disk-key"
                })
                .build())

    # ===== Métodos adicionales (compatibilidad) =====
    def build_minimal_vm(self, name: str) -> MachineVirtual:
        """VM mínima para desarrollo/testing"""
        return (self._builder
                .reset()
                .set_basic_config(name, "standard")
                .set_compute_resources(cpu=1, ram=1)
                .set_storage(size_gb=10)
                .build())

    def build_high_performance_vm(self, name: str, location: str) -> MachineVirtual:
        """VM de alto rendimiento (alias para disk-optimized)"""
        return self.build_disk_optimized_vm(name, location, size="large")

    def build_custom_vm(self, name: str, cpu: int, ram: int,
                        disk_gb: int, location: str) -> MachineVirtual:
        """VM personalizada con especificaciones exactas"""
        return (self._builder
                .reset()
                .set_basic_config(name, "custom")
                .set_location(location)
                .set_compute_resources(cpu=cpu, ram=ram)
                .set_storage(size_gb=disk_gb)
                .set_network()
                .build())