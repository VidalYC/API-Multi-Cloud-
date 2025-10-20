from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from domain.entities import MachineVirtual, Network, StorageDisk


class ProveedorAbstracto(ABC):
    
    
    def __init__(self):
        self._estado = True
        self._provisional = None
    
    @abstractmethod
    def crear_vm(self) -> MachineVirtual:
        
        pass

    @abstractmethod
    def crear_network(self) -> Network:
        
        pass

    @abstractmethod
    def crear_disk(self) -> StorageDisk:
        
        pass
    
    def estado(self) -> bool:
        
        return self._estado
    
    def provisionar(self) -> MachineVirtual:
        
        
        if not self._estado:
            raise Exception("Proveedor no disponible")
        
        
        network = self.crear_network()
        disk = self.crear_disk()
        
        
        vm = self.crear_vm()
        vm.network = network
        vm.disks = [disk]

        return vm


class Prototype(ABC):
    

    @abstractmethod
    def clone(self) -> 'Prototype':
        
        pass

    @abstractmethod
    def customize(self, **kwargs) -> 'Prototype':
        
        pass