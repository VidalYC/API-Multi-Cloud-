"""
Domain Layer - Prototype Registry
Gestiona un catálogo de prototipos de VMs predefinidos que pueden clonarse.
Implementa el patrón Prototype combinado con Singleton para el registro.
"""
from typing import Dict, Optional, List, Any
from datetime import datetime
from domain.entities import MachineVirtual, Network, StorageDisk, VMStatus


class VMPrototypeRegistry:
    """
    Patrón Prototype Registry: Gestiona un catálogo de prototipos de VMs.
    Permite registrar, obtener y clonar VMs predefinidas.

    Aplicando SRP: Responsabilidad única de gestionar el catálogo de prototipos.
    Aplicando OCP: Permite agregar nuevos prototipos sin modificar la clase.
    """

    _instance = None
    _prototypes: Dict[str, MachineVirtual] = {}

    def __new__(cls):
        """Singleton: Asegura una única instancia del registro."""
        if cls._instance is None:
            cls._instance = super(VMPrototypeRegistry, cls).__new__(cls)
            cls._instance._initialize_default_prototypes()
        return cls._instance

    def _initialize_default_prototypes(self):
        """
        Inicializa prototipos predefinidos para casos de uso comunes.
        Estos prototipos pueden clonarse para crear VMs rápidamente.
        """
        # Prototipo: Servidor Web AWS
        self.register_prototype(
            "aws-web-server",
            MachineVirtual(
                vmId="aws-vm-prototype-web",
                name="web-server-template",
                status=VMStatus.PENDING,
                createdAt=datetime.now(),
                provider="aws",
                vcpus=2,
                memoryGB=4,
                instance_type="t3.medium",
                memoryOptimization=False,
                diskOptimization=False,
                keyPairName="web-server-key",
                network=Network(
                    networkId="aws-net-prototype-web",
                    name="web-server-network",
                    cidr_block="10.0.0.0/16",
                    provider="aws",
                    region="us-east-1",
                    firewallRules=["allow-http-80", "allow-https-443", "allow-ssh-22"],
                    publicIP=True
                ),
                disks=[
                    StorageDisk(
                        diskId="aws-disk-prototype-web",
                        name="web-server-disk",
                        size_gb=50,
                        disk_type="gp3",
                        provider="aws",
                        region="us-east-1",
                        iops=3000
                    )
                ]
            )
        )

        # Prototipo: Base de Datos Azure (Memory-Optimized)
        self.register_prototype(
            "azure-database",
            MachineVirtual(
                vmId="azure-vm-prototype-db",
                name="database-template",
                status=VMStatus.PENDING,
                createdAt=datetime.now(),
                provider="azure",
                vcpus=4,
                memoryGB=32,
                instance_type="E4s_v3",
                memoryOptimization=True,
                diskOptimization=False,
                keyPairName="db-key",
                network=Network(
                    networkId="azure-net-prototype-db",
                    name="database-network",
                    cidr_block="10.1.0.0/16",
                    provider="azure",
                    region="eastus",
                    firewallRules=["allow-postgres-5432", "allow-mysql-3306"],
                    publicIP=False
                ),
                disks=[
                    StorageDisk(
                        diskId="azure-disk-prototype-db",
                        name="database-disk",
                        size_gb=500,
                        disk_type="Premium_LRS",
                        provider="azure",
                        region="eastus",
                        iops=5000
                    )
                ]
            )
        )

        # Prototipo: Procesamiento de Datos GCP (Disk-Optimized)
        self.register_prototype(
            "gcp-data-processing",
            MachineVirtual(
                vmId="gcp-vm-prototype-data",
                name="data-processing-template",
                status=VMStatus.PENDING,
                createdAt=datetime.now(),
                provider="google",
                vcpus=8,
                memoryGB=16,
                instance_type="c2-standard-8",
                memoryOptimization=False,
                diskOptimization=True,
                keyPairName="data-processing-key",
                network=Network(
                    networkId="gcp-net-prototype-data",
                    name="data-processing-network",
                    cidr_block="10.2.0.0/16",
                    provider="google",
                    region="us-central1",
                    firewallRules=["allow-internal"],
                    publicIP=False
                ),
                disks=[
                    StorageDisk(
                        diskId="gcp-disk-prototype-data",
                        name="data-processing-disk",
                        size_gb=1000,
                        disk_type="pd-ssd",
                        provider="google",
                        region="us-central1",
                        iops=None
                    )
                ]
            )
        )

        # Prototipo: Desarrollo/Testing On-Premise (Minimal)
        self.register_prototype(
            "onpremise-dev",
            MachineVirtual(
                vmId="onpremise-vm-prototype-dev",
                name="dev-environment-template",
                status=VMStatus.PENDING,
                createdAt=datetime.now(),
                provider="onpremise",
                vcpus=2,
                memoryGB=4,
                instance_type="onprem-std1",
                memoryOptimization=False,
                diskOptimization=False,
                keyPairName=None,
                network=Network(
                    networkId="onpremise-net-prototype-dev",
                    name="dev-network",
                    cidr_block="192.168.1.0/24",
                    provider="onpremise",
                    region="datacenter-1",
                    firewallRules=["allow-all-internal"],
                    publicIP=False
                ),
                disks=[
                    StorageDisk(
                        diskId="onpremise-disk-prototype-dev",
                        name="dev-disk",
                        size_gb=100,
                        disk_type="ssd",
                        provider="onpremise",
                        region="datacenter-1",
                        iops=None
                    )
                ]
            )
        )

    def register_prototype(self, name: str, prototype: MachineVirtual) -> None:
        """
        Registra un nuevo prototipo en el catálogo.

        Args:
            name: Identificador único del prototipo
            prototype: Instancia de MachineVirtual a usar como prototipo
        """
        self._prototypes[name] = prototype

    def get_prototype(self, name: str) -> Optional[MachineVirtual]:
        """
        Obtiene un prototipo del catálogo (sin clonarlo).

        Args:
            name: Identificador del prototipo

        Returns:
            Prototipo si existe, None en caso contrario
        """
        return self._prototypes.get(name)

    def clone_prototype(self, name: str, new_name: Optional[str] = None, **customizations) -> Optional[MachineVirtual]:
        """
        Clona un prototipo del catálogo con opciones de personalización.

        Args:
            name: Identificador del prototipo a clonar
            new_name: Nombre para la VM clonada
            **customizations: Parámetros para personalizar el clon

        Returns:
            Nueva VM clonada o None si el prototipo no existe
        """
        prototype = self.get_prototype(name)
        if prototype:
            return prototype.clone(new_name=new_name, **customizations)
        return None

    def list_prototypes(self) -> List[Dict[str, Any]]:
        """
        Lista todos los prototipos disponibles con sus detalles básicos.

        Returns:
            Lista de diccionarios con información de cada prototipo
        """
        prototypes_info = []
        for name, vm in self._prototypes.items():
            prototypes_info.append({
                "name": name,
                "provider": vm.provider,
                "vcpus": vm.vcpus,
                "memoryGB": vm.memoryGB,
                "instance_type": vm.instance_type,
                "description": self._get_prototype_description(name),
                "disk_size_gb": vm.disks[0].size_gb if vm.disks and len(vm.disks) > 0 else 0,
                "has_public_ip": vm.network.publicIP if vm.network else False
            })
        return prototypes_info

    def _get_prototype_description(self, name: str) -> str:
        """Retorna una descripción amigable del prototipo."""
        descriptions = {
            "aws-web-server": "Servidor web en AWS con balanceo de carga y acceso público",
            "azure-database": "Servidor de base de datos optimizado para memoria en Azure",
            "gcp-data-processing": "VM para procesamiento de datos en Google Cloud",
            "onpremise-dev": "Entorno de desarrollo/testing on-premise"
        }
        return descriptions.get(name, "Prototipo personalizado")

    def remove_prototype(self, name: str) -> bool:
        """
        Elimina un prototipo del catálogo.

        Args:
            name: Identificador del prototipo a eliminar

        Returns:
            True si se eliminó, False si no existía
        """
        if name in self._prototypes:
            del self._prototypes[name]
            return True
        return False

    def prototype_exists(self, name: str) -> bool:
        """Verifica si un prototipo existe en el catálogo."""
        return name in self._prototypes
