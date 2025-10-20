from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from domain.entities import MachineVirtual, Network, StorageDisk, VMInstanceType


class VMBuilder(ABC):
    
    def __init__(self):
        self._vm: Optional[MachineVirtual] = None
        self._network: Optional[Network] = None
        self._disk: Optional[StorageDisk] = None
        self._config: Dict[str, Any] = {}

    @abstractmethod
    def reset(self) -> 'VMBuilder':
        
        pass

    @abstractmethod
    def set_basic_config(self, name: str, vm_type: str) -> 'VMBuilder':
        
        pass

    @abstractmethod
    def set_compute_resources(self, cpu: Optional[int] = None,
                              ram: Optional[int] = None) -> 'VMBuilder':
        
        pass

    @abstractmethod
    def set_storage(self, size_gb: int, disk_type: Optional[str] = None,
                    iops: Optional[int] = None) -> 'VMBuilder':
        
        pass

    @abstractmethod
    def set_network(self, network_id: Optional[str] = None,
                    cidr: Optional[str] = None,
                    firewall_rules: Optional[list] = None,
                    public_ip: Optional[bool] = None) -> 'VMBuilder':
       
        pass

    @abstractmethod
    def set_location(self, location: str) -> 'VMBuilder':
        
        pass

    @abstractmethod
    def set_advanced_options(self, options: Dict[str, Any]) -> 'VMBuilder':
        
        pass

    @abstractmethod
    def set_instance_type(self, instance_type: str) -> 'VMBuilder':
        
        pass

    @abstractmethod
    def build(self) -> MachineVirtual:
        
        pass

    def get_config(self) -> Dict[str, Any]:
        return self._config.copy()


class VMDirector:
    
    
    def __init__(self, builder: VMBuilder):
        self._builder = builder

    def change_builder(self, builder: VMBuilder) -> None:
        
        self._builder = builder

    
    def build_standard_vm(self, name: str, location: str, size: str = "medium") -> MachineVirtual:
        
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

    
    def build_memory_optimized_vm(self, name: str, location: str, size: str = "medium") -> MachineVirtual:
        
        return (self._builder
                .reset()
                .set_basic_config(name, "memory-optimized")
                .set_location(location)
                .set_storage(size_gb=100, disk_type="standard")
                .set_network(public_ip=False, firewall_rules=["SSH"])
                .set_advanced_options({
                    "memoryOptimization": True,  
                    "diskOptimization": False,
                    "keyPairName": "memory-key"
                })
                .build())

    
    def build_disk_optimized_vm(self, name: str, location: str, size: str = "medium") -> MachineVirtual:
        
        return (self._builder
                .reset()
                .set_basic_config(name, "disk-optimized")
                .set_location(location)
                .set_storage(size_gb=500, disk_type="ssd", iops=3000)  
                .set_network(public_ip=True, firewall_rules=["HTTP", "HTTPS", "SSH"])
                .set_advanced_options({
                    "memoryOptimization": False,
                    "diskOptimization": True,  
                    "keyPairName": "disk-key"
                })
                .build())

    
    def build_minimal_vm(self, name: str) -> MachineVirtual:
       
        return (self._builder
                .reset()
                .set_basic_config(name, "standard")
                .set_compute_resources(cpu=1, ram=1)
                .set_storage(size_gb=10)
                .build())

    def build_high_performance_vm(self, name: str, location: str) -> MachineVirtual:
        
        return self.build_disk_optimized_vm(name, location, size="large")

    def build_custom_vm(self, name: str, cpu: int, ram: int,
                        disk_gb: int, location: str) -> MachineVirtual:
        
        return (self._builder
                .reset()
                .set_basic_config(name, "custom")
                .set_location(location)
                .set_compute_resources(cpu=cpu, ram=ram)
                .set_storage(size_gb=disk_gb)
                .set_network()
                .build())