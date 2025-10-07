"""
AWS VM Builder - Concrete Builder para AWS
Implementa construcción paso a paso de VMs en AWS
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any
import logging

from domain.builder import VMBuilder
from domain.entities import MachineVirtual, VMStatus, Network, StorageDisk

logger = logging.getLogger(__name__)


class AWSVMBuilder(VMBuilder):
    """
    Concrete Builder: Implementa construcción de VMs para AWS

    Aplicando:
    - Builder Pattern: Construcción paso a paso específica para AWS
    - Fluent Interface: Retorna self para encadenar llamadas
    """

    def __init__(self):
        super().__init__()
        self._config = {
            'provider': 'aws',
            'region': 'us-east-1',
            'instance_type': 't2.micro',
            'volume_type': 'gp2',
            'size_gb': 20
        }

    def reset(self) -> 'AWSVMBuilder':
        """Reinicia el builder"""
        self.__init__()
        return self

    def set_basic_config(self, name: str, vm_type: str) -> 'AWSVMBuilder':
        """Configura parámetros básicos de AWS"""
        self._config['name'] = name

        # Mapeo de tipos a instance types de AWS
        type_mapping = {
            'minimal': 't2.micro',
            'standard': 't2.small',
            'high-performance': 't2.xlarge',
            'custom': 't2.medium'
        }

        self._config['instance_type'] = type_mapping.get(vm_type, vm_type)
        logger.info(f"AWS Builder: Configuración básica - Nombre: {name}, Tipo: {self._config['instance_type']}")

        return self

    def set_compute_resources(self, cpu: Optional[int] = None,
                             ram: Optional[int] = None) -> 'AWSVMBuilder':
        """Configura recursos de cómputo"""
        if cpu or ram:
            # Mapeo aproximado de CPU/RAM a instance types
            if cpu and ram:
                if cpu <= 1 and ram <= 1:
                    self._config['instance_type'] = 't2.micro'
                elif cpu <= 2 and ram <= 4:
                    self._config['instance_type'] = 't2.small'
                elif cpu <= 4 and ram <= 16:
                    self._config['instance_type'] = 't2.large'
                elif cpu <= 8 and ram <= 32:
                    self._config['instance_type'] = 't2.xlarge'
                else:
                    self._config['instance_type'] = 't2.2xlarge'

            self._config['cpu'] = cpu
            self._config['ram'] = ram
            logger.info(f"AWS Builder: Recursos de cómputo - CPU: {cpu}, RAM: {ram}GB")

        return self

    def set_storage(self, size_gb: int, disk_type: Optional[str] = None) -> 'AWSVMBuilder':
        """Configura almacenamiento EBS"""
        self._config['size_gb'] = size_gb

        # Mapeo de tipos de disco
        disk_mapping = {
            'ssd': 'gp3',
            'standard': 'gp2',
            'magnetic': 'standard',
            'io': 'io2'
        }

        self._config['volume_type'] = disk_mapping.get(disk_type, 'gp2') if disk_type else 'gp2'
        logger.info(f"AWS Builder: Almacenamiento - {size_gb}GB, Tipo: {self._config['volume_type']}")

        return self

    def set_network(self, network_id: Optional[str] = None,
                   cidr: Optional[str] = None) -> 'AWSVMBuilder':
        """Configura VPC y red"""
        self._config['vpc_id'] = network_id or f"vpc-{uuid.uuid4().hex[:8]}"
        self._config['cidr_block'] = cidr or '10.0.0.0/16'
        logger.info(f"AWS Builder: Red - VPC: {self._config['vpc_id']}")

        return self

    def set_location(self, location: str) -> 'AWSVMBuilder':
        """Configura región de AWS"""
        self._config['region'] = location
        logger.info(f"AWS Builder: Ubicación - Región: {location}")

        return self

    def set_advanced_options(self, options: Dict[str, Any]) -> 'AWSVMBuilder':
        """Configura opciones avanzadas de AWS"""
        if 'optimized' in options:
            self._config['ebs_optimized'] = options['optimized']

        if 'monitoring' in options:
            self._config['detailed_monitoring'] = options['monitoring']

        if 'security_group' in options:
            self._config['security_group'] = options['security_group']

        self._config.update(options)
        logger.info(f"AWS Builder: Opciones avanzadas configuradas")

        return self

    def build(self) -> MachineVirtual:
        """Construye la VM de AWS con toda la configuración"""
        vm_id = f"aws-{uuid.uuid4()}"

        # Crear Network
        network = Network(
            networkId=self._config.get('vpc_id', f"vpc-{uuid.uuid4().hex[:8]}"),
            name=f"aws-net-{self._config.get('region', 'us-east-1')}",
            cidr_block=self._config.get('cidr_block', '10.0.0.0/16'),
            provider='aws'
        )

        # Crear Disk
        disk = StorageDisk(
            diskId=f"vol-{uuid.uuid4().hex[:12]}",
            name=f"aws-disk-{self._config.get('volume_type', 'gp2')}",
            size_gb=self._config.get('size_gb', 20),
            disk_type=self._config.get('volume_type', 'gp2'),
            provider='aws'
        )

        # Crear VM
        vm = MachineVirtual(
            vmId=vm_id,
            name=self._config.get('name', f"aws-vm-{vm_id[:4]}"),
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider='aws',
            network=network,
            disks=[disk]
        )

        logger.info(f"AWS Builder: VM construida exitosamente - ID: {vm_id}")

        return vm
