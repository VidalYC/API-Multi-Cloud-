"""
Domain Layer - Builder Pattern
Implementación del patrón Builder para construcción compleja de VMs
Aplicando Builder Pattern para construcción paso a paso
"""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from domain.entities import MachineVirtual, Network, StorageDisk


class VMBuilder(ABC):
    """
    Builder Abstracto: Define la interfaz para construir VMs paso a paso

    Aplicando:
    - Builder Pattern: Construcción compleja de objetos paso a paso
    - SRP: Solo se encarga de construir VMs
    - OCP: Fácil agregar nuevos builders sin modificar código existente
    """

    def __init__(self):
        self._vm: Optional[MachineVirtual] = None
        self._network: Optional[Network] = None
        self._disk: Optional[StorageDisk] = None
        self._config: Dict[str, Any] = {}

    @abstractmethod
    def reset(self) -> 'VMBuilder':
        """
        Reinicia el builder para comenzar una nueva construcción
        """
        pass

    @abstractmethod
    def set_basic_config(self, name: str, vm_type: str) -> 'VMBuilder':
        """
        Configura los parámetros básicos de la VM

        Args:
            name: Nombre de la VM
            vm_type: Tipo de instancia/tamaño
        """
        pass

    @abstractmethod
    def set_compute_resources(self, cpu: Optional[int] = None,
                             ram: Optional[int] = None) -> 'VMBuilder':
        """
        Configura recursos de cómputo (CPU, RAM)

        Args:
            cpu: Número de CPUs
            ram: RAM en GB
        """
        pass

    @abstractmethod
    def set_storage(self, size_gb: int, disk_type: Optional[str] = None) -> 'VMBuilder':
        """
        Configura el almacenamiento de la VM

        Args:
            size_gb: Tamaño del disco en GB
            disk_type: Tipo de disco (SSD, HDD, etc)
        """
        pass

    @abstractmethod
    def set_network(self, network_id: Optional[str] = None,
                   cidr: Optional[str] = None) -> 'VMBuilder':
        """
        Configura la red de la VM

        Args:
            network_id: ID de la red/VPC
            cidr: Bloque CIDR
        """
        pass

    @abstractmethod
    def set_location(self, location: str) -> 'VMBuilder':
        """
        Configura la ubicación (región, zona, datacenter)

        Args:
            location: Ubicación donde se desplegará la VM
        """
        pass

    @abstractmethod
    def set_advanced_options(self, options: Dict[str, Any]) -> 'VMBuilder':
        """
        Configura opciones avanzadas específicas del proveedor

        Args:
            options: Diccionario con opciones avanzadas
        """
        pass

    @abstractmethod
    def build(self) -> MachineVirtual:
        """
        Construye y retorna la VM configurada

        Returns:
            MachineVirtual completamente configurada
        """
        pass

    def get_config(self) -> Dict[str, Any]:
        """Retorna la configuración actual"""
        return self._config.copy()


class VMDirector:
    """
    Director: Define el orden de los pasos de construcción para crear
    configuraciones predefinidas de VMs

    Aplicando:
    - Director Pattern: Encapsula el algoritmo de construcción
    - SRP: Solo se encarga de orquestar la construcción
    """

    def __init__(self, builder: VMBuilder):
        self._builder = builder

    def change_builder(self, builder: VMBuilder) -> None:
        """Cambia el builder utilizado"""
        self._builder = builder

    def build_minimal_vm(self, name: str) -> MachineVirtual:
        """
        Construye una VM con configuración mínima (desarrollo/testing)

        Args:
            name: Nombre de la VM

        Returns:
            VM con configuración mínima
        """
        return (self._builder
                .reset()
                .set_basic_config(name, "minimal")
                .set_compute_resources(cpu=1, ram=1)
                .set_storage(size_gb=10)
                .build())

    def build_standard_vm(self, name: str, location: str) -> MachineVirtual:
        """
        Construye una VM con configuración estándar (aplicaciones web)

        Args:
            name: Nombre de la VM
            location: Ubicación de despliegue

        Returns:
            VM con configuración estándar
        """
        return (self._builder
                .reset()
                .set_basic_config(name, "standard")
                .set_location(location)
                .set_compute_resources(cpu=2, ram=4)
                .set_storage(size_gb=50)
                .set_network()
                .build())

    def build_high_performance_vm(self, name: str, location: str) -> MachineVirtual:
        """
        Construye una VM de alto rendimiento (bases de datos, analytics)

        Args:
            name: Nombre de la VM
            location: Ubicación de despliegue

        Returns:
            VM con configuración de alto rendimiento
        """
        return (self._builder
                .reset()
                .set_basic_config(name, "high-performance")
                .set_location(location)
                .set_compute_resources(cpu=8, ram=32)
                .set_storage(size_gb=500, disk_type="ssd")
                .set_network()
                .set_advanced_options({"optimized": True, "monitoring": True})
                .build())

    def build_custom_vm(self, name: str, cpu: int, ram: int,
                       disk_gb: int, location: str) -> MachineVirtual:
        """
        Construye una VM con configuración personalizada

        Args:
            name: Nombre de la VM
            cpu: Número de CPUs
            ram: RAM en GB
            disk_gb: Tamaño del disco en GB
            location: Ubicación de despliegue

        Returns:
            VM con configuración personalizada
        """
        return (self._builder
                .reset()
                .set_basic_config(name, "custom")
                .set_location(location)
                .set_compute_resources(cpu=cpu, ram=ram)
                .set_storage(size_gb=disk_gb)
                .set_network()
                .build())
