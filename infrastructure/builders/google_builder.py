"""
Google Cloud VM Builder - Concrete Builder para GCP
Implementa construcción paso a paso de VMs en Google Cloud
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
import logging

from domain.builder import VMBuilder
from domain.entities import MachineVirtual, VMStatus, Network, StorageDisk

logger = logging.getLogger(__name__)


class GoogleVMBuilder(VMBuilder):
    """
    Concrete Builder: Implementa construcción de VMs para Google Cloud
    """

    def __init__(self):
        super().__init__()
        self._config = {
            'provider': 'google',
            'zone': 'us-central1-a',
            'machine_type': 'n1-standard-1',
            'disk_type': 'pd-standard',
            'size_gb': 10
        }

    def reset(self) -> 'GoogleVMBuilder':
        """Reinicia el builder"""
        self.__init__()
        return self

    def set_basic_config(self, name: str, vm_type: str) -> 'GoogleVMBuilder':
        """Configura parámetros básicos de GCP"""
        self._config['name'] = name

        # Mapeo de tipos a machine types de GCP
        type_mapping = {
            'minimal': 'f1-micro',
            'standard': 'n1-standard-1',
            'high-performance': 'n1-standard-8',
            'custom': 'n1-standard-2'
        }

        self._config['machine_type'] = type_mapping.get(vm_type, vm_type)
        logger.info(f"Google Builder: Configuración básica - Nombre: {name}, Tipo: {self._config['machine_type']}")

        return self

    def set_compute_resources(self, cpu: Optional[int] = None,
                             ram: Optional[int] = None) -> 'GoogleVMBuilder':
        """Configura recursos de cómputo"""
        if cpu or ram:
            # Mapeo aproximado de CPU/RAM a machine types
            if cpu and ram:
                if cpu <= 1 and ram <= 1:
                    self._config['machine_type'] = 'f1-micro'
                elif cpu <= 2 and ram <= 4:
                    self._config['machine_type'] = 'n1-standard-1'
                elif cpu <= 4 and ram <= 16:
                    self._config['machine_type'] = 'n1-standard-4'
                elif cpu <= 8 and ram <= 32:
                    self._config['machine_type'] = 'n1-standard-8'
                else:
                    self._config['machine_type'] = 'n1-standard-16'

            self._config['cpu'] = cpu
            self._config['ram'] = ram
            logger.info(f"Google Builder: Recursos de cómputo - CPU: {cpu}, RAM: {ram}GB")

        return self

    def set_storage(self, size_gb: int, disk_type: Optional[str] = None) -> 'GoogleVMBuilder':
        """Configura persistent disks"""
        self._config['size_gb'] = size_gb

        # Mapeo de tipos de disco
        disk_mapping = {
            'ssd': 'pd-ssd',
            'standard': 'pd-standard',
            'balanced': 'pd-balanced'
        }

        self._config['disk_type'] = disk_mapping.get(disk_type, 'pd-standard') if disk_type else 'pd-standard'
        logger.info(f"Google Builder: Almacenamiento - {size_gb}GB, Tipo: {self._config['disk_type']}")

        return self

    def set_network(self, network_id: Optional[str] = None,
                   cidr: Optional[str] = None) -> 'GoogleVMBuilder':
        """Configura VPC y red"""
        self._config['network_name'] = network_id or 'default-net'
        self._config['cidr_block'] = cidr or '10.2.0.0/16'
        logger.info(f"Google Builder: Red - Network: {self._config['network_name']}")

        return self

    def set_location(self, location: str) -> 'GoogleVMBuilder':
        """Configura zona de GCP"""
        self._config['zone'] = location
        logger.info(f"Google Builder: Ubicación - Zona: {location}")

        return self

    def set_advanced_options(self, options: Dict[str, Any]) -> 'GoogleVMBuilder':
        """Configura opciones avanzadas de GCP"""
        if 'optimized' in options:
            self._config['preemptible'] = not options['optimized']

        if 'monitoring' in options:
            self._config['enable_monitoring'] = options['monitoring']

        if 'labels' in options:
            self._config['labels'] = options['labels']

        self._config.update(options)
        logger.info(f"Google Builder: Opciones avanzadas configuradas")

        return self

    def build(self) -> MachineVirtual:
        """Construye la VM de GCP con toda la configuración"""
        vm_id = f"gcp-{uuid.uuid4()}"

        # Crear Network
        network = Network(
            networkId=self._config.get('network_name', 'default-net'),
            name=self._config.get('network_name', 'default-net'),
            cidr_block=self._config.get('cidr_block', '10.2.0.0/16'),
            provider='google'
        )

        # Crear Disk
        disk = StorageDisk(
            diskId=f"disk-{uuid.uuid4().hex[:8]}",
            name=f"gcp-disk-{self._config.get('disk_type', 'pd-standard')}",
            size_gb=self._config.get('size_gb', 10),
            disk_type=self._config.get('disk_type', 'pd-standard'),
            provider='google'
        )

        # Crear VM
        vm = MachineVirtual(
            vmId=vm_id,
            name=self._config.get('name', f"gcp-vm-{vm_id[:4]}"),
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider='google',
            network=network,
            disks=[disk]
        )

        logger.info(f"Google Builder: VM construida exitosamente - ID: {vm_id}")

        return vm
