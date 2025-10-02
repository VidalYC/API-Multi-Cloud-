"""
Domain Layer - Interfaces
Abstracciones que definen contratos (DIP - Dependency Inversion Principle)
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from domain.entities import MachineVirtual, Network, StorageDisk


class ProveedorAbstracto(ABC):
    """
    Abstract Factory: Define la interfaz para crear familias de objetos relacionados (VM, Network, Disk).
    Aplicando DIP: Los módulos de alto nivel dependen de esta abstracción
    Aplicando OCP: Podemos extender sin modificar el código existente
    """
    
    def __init__(self):
        self._estado = True
        self._provisional = None
    
    @abstractmethod
    def crear_vm(self) -> MachineVirtual:
        """
        Crea el producto: Máquina Virtual.
        """
        pass

    @abstractmethod
    def crear_network(self) -> Network:
        """
        Crea el producto: Red.
        """
        pass

    @abstractmethod
    def crear_disk(self) -> StorageDisk:
        """
        Crea el producto: Disco.
        """
        pass
    
    def estado(self) -> bool:
        """Retorna el estado del proveedor"""
        return self._estado
    
    def provisionar(self) -> MachineVirtual:
        """
        Template Method: Orquesta la creación de la familia de recursos.
        Cumple con RNF1 (Consistencia): VM no se crea sin Red y Disco.
        """
        # Validaciones generales
        if not self._estado:
            raise Exception("Proveedor no disponible")
        
        # 1. Crear recursos dependientes (Red y Disco)
        network = self.crear_network()
        disk = self.crear_disk()
        
        # 2. Crear el recurso principal (VM) y asociar los otros
        vm = self.crear_vm()
        vm.network = network
        vm.disks = [disk]
        
        return vm