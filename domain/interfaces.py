"""
Domain Layer - Interfaces
Abstracciones que definen contratos (DIP - Dependency Inversion Principle)
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
from domain.entities import MachineVirtual


class ProveedorAbstracto(ABC):
    """
    Interfaz base para todos los proveedores de cloud
    Aplicando DIP: Los módulos de alto nivel dependen de esta abstracción
    Aplicando OCP: Podemos extender sin modificar el código existente
    """
    
    def __init__(self):
        self._estado = True
        self._provisional = None
    
    @abstractmethod
    def crear_vm(self) -> MachineVirtual:
        """
        Método Factory que debe ser implementado por cada proveedor concreto
        Factory Method Pattern: Define la interfaz para crear objetos
        """
        pass
    
    def estado(self) -> bool:
        """Retorna el estado del proveedor"""
        return self._estado
    
    def provisionar(self) -> MachineVirtual:
        """
        Template Method: Define el algoritmo general de aprovisionamiento
        """
        # Validaciones generales
        if not self._estado:
            raise Exception("Proveedor no disponible")
        
        # Delega la creación específica al método abstracto
        vm = self.crear_vm()
        
        return vm