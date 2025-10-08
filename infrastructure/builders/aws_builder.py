import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
import logging

from domain.builder import VMBuilder
from domain.entities import MachineVirtual, VMStatus, Network, StorageDisk, VMInstanceType

logger = logging.getLogger(__name__)


class AWSVMBuilder(VMBuilder):
    """
    Builder concreto para AWS con parámetros del PDF
    Implementa validación de región y tipos de instancia exactos
    """
    
    def __init__(self):
        super().__init__()
        self._config = {
            'provider': 'aws',
            'region': 'us-east-1',
            'instance_type': 't3.medium',  # Default: Standard VM
            'vcpus': 2,
            'memoryGB': 4,
            'volume_type': 'gp2',
            'size_gb': 50,
            'memoryOptimization': False,
            'diskOptimization': False,
            'keyPairName': None,
            'firewallRules': None,
            'publicIP': None,
            'iops': None
        }

    def reset(self) -> 'AWSVMBuilder':
        self.__init__()
        return self

    def set_basic_config(self, name: str, vm_type: str) -> 'AWSVMBuilder':
        """
        Configura el tipo de VM según el PDF
        vm_type: 'standard', 'memory-optimized', 'disk-optimized'
        """
        self._config['name'] = name
        self._config['vm_type'] = vm_type
        
        # Mapeo de tipos de VM a instance_type según PDF (Página 2)
        if vm_type == 'standard':
            self._config['instance_type'] = 't3.medium'  # General Purpose
            self._config['memoryOptimization'] = False
            self._config['diskOptimization'] = False
        elif vm_type == 'memory-optimized':
            self._config['instance_type'] = 'r5.large'  # Memory-Optimized
            self._config['memoryOptimization'] = True
            self._config['diskOptimization'] = False
        elif vm_type == 'disk-optimized':
            self._config['instance_type'] = 'c5.large'  # Compute-Optimized
            self._config['memoryOptimization'] = False
            self._config['diskOptimization'] = True
        else:
            # Tipo personalizado
            self._config['instance_type'] = vm_type
        
        # Obtener vCPU y memoria del tipo de instancia
        specs = VMInstanceType.get_specs('aws', self._config['instance_type'])
        if specs:
            self._config['vcpus'] = specs['vcpus']
            self._config['memoryGB'] = specs['memoryGB']
        
        logger.info(f"AWS Builder: Configuración básica - Nombre: {name}, Tipo: {vm_type}, Instance: {self._config['instance_type']}")
        return self

    def set_instance_type(self, instance_type: str) -> 'AWSVMBuilder':
        """
        Configura un tipo de instancia específico de AWS
        Ejemplo: t3.medium, m5.large, r5.xlarge, c5.2xlarge
        """
        self._config['instance_type'] = instance_type
        
        # Obtener vCPU y memoria automáticamente
        specs = VMInstanceType.get_specs('aws', instance_type)
        if specs:
            self._config['vcpus'] = specs['vcpus']
            self._config['memoryGB'] = specs['memoryGB']
            logger.info(f"AWS Builder: Instance Type configurado - {instance_type} ({specs['vcpus']} vCPUs, {specs['memoryGB']} GB RAM)")
        else:
            logger.warning(f"AWS Builder: Instance Type '{instance_type}' no reconocido, usando valores por defecto")
        
        return self

    def set_compute_resources(self, cpu: Optional[int] = None, ram: Optional[int] = None) -> 'AWSVMBuilder':
        """Configura recursos de cómputo (anula el instance_type)"""
        if cpu is not None:
            self._config['vcpus'] = cpu
        if ram is not None:
            self._config['memoryGB'] = ram
        
        logger.info(f"AWS Builder: Recursos de cómputo - CPU: {self._config['vcpus']}, RAM: {self._config['memoryGB']}GB")
        return self

    def set_storage(self, size_gb: int, disk_type: Optional[str] = None,
                    iops: Optional[int] = None) -> 'AWSVMBuilder':
        """
        Configura almacenamiento
        iops: Parámetro opcional del PDF (Página 2)
        """
        self._config['size_gb'] = size_gb
        
        disk_mapping = {
            'ssd': 'gp3',
            'standard': 'gp2',
            'magnetic': 'standard',
            'io': 'io2'
        }
        self._config['volume_type'] = disk_mapping.get(disk_type, 'gp2') if disk_type else 'gp2'
        
        # IOPS del PDF (Página 2)
        if iops is not None:
            self._config['iops'] = iops
        
        logger.info(f"AWS Builder: Almacenamiento - {size_gb}GB, Tipo: {self._config['volume_type']}, IOPS: {iops}")
        return self

    def set_network(self, network_id: Optional[str] = None, cidr: Optional[str] = None,
                    firewall_rules: Optional[list] = None, public_ip: Optional[bool] = None) -> 'AWSVMBuilder':
        """
        Configura red con parámetros del PDF (Página 2)
        firewall_rules: Reglas de seguridad (opcional)
        public_ip: IP pública asignada (opcional)
        """
        self._config['vpc_id'] = network_id or f"vpc-{uuid.uuid4().hex[:8]}"
        self._config['cidr_block'] = cidr or '10.0.0.0/16'
        
        # Parámetros opcionales del PDF
        if firewall_rules is not None:
            self._config['firewallRules'] = firewall_rules
        if public_ip is not None:
            self._config['publicIP'] = public_ip
        
        logger.info(f"AWS Builder: Red - VPC: {self._config['vpc_id']}, Firewall: {firewall_rules}, Public IP: {public_ip}")
        return self

    def set_location(self, location: str) -> 'AWSVMBuilder':
        """Configura la región de AWS"""
        self._config['region'] = location
        logger.info(f"AWS Builder: Ubicación - Región: {location}")
        return self

    def set_advanced_options(self, options: Dict[str, Any]) -> 'AWSVMBuilder':
        """
        Configura opciones avanzadas del PDF (Página 2)
        - memoryOptimization
        - diskOptimization
        - keyPairName
        """
        if 'memoryOptimization' in options:
            self._config['memoryOptimization'] = options['memoryOptimization']
        if 'diskOptimization' in options:
            self._config['diskOptimization'] = options['diskOptimization']
        if 'keyPairName' in options:
            self._config['keyPairName'] = options['keyPairName']
        
        # Otras opciones avanzadas
        if 'optimized' in options:
            self._config['ebs_optimized'] = options['optimized']
        if 'monitoring' in options:
            self._config['detailed_monitoring'] = options['monitoring']
        if 'security_group' in options:
            self._config['security_group'] = options['security_group']
        
        self._config.update(options)
        logger.info("AWS Builder: Opciones avanzadas configuradas")
        return self

    def build(self) -> MachineVirtual:
        """
        Construye la VM con validación de región
        RF5: Los recursos deben validarse para garantizar coherencia de región
        """
        region = self._config.get('region', 'us-east-1')
        
        # Crear Network con región obligatoria (PDF Página 2)
        network = Network(
            networkId=self._config.get('vpc_id', f"vpc-{uuid.uuid4().hex[:8]}"),
            name=f"aws-net-{region}",
            cidr_block=self._config.get('cidr_block', '10.0.0.0/16'),
            provider='aws',
            region=region,  # ✅ OBLIGATORIO según PDF
            firewallRules=self._config.get('firewallRules'),  # ✅ OPCIONAL según PDF
            publicIP=self._config.get('publicIP')  # ✅ OPCIONAL según PDF
        )
        
        # Crear Disk con región obligatoria (PDF Página 2)
        disk = StorageDisk(
            diskId=f"vol-{uuid.uuid4().hex[:12]}",
            name=f"aws-disk-{self._config.get('volume_type', 'gp2')}",
            size_gb=self._config.get('size_gb', 50),
            disk_type=self._config.get('volume_type', 'gp2'),
            provider='aws',
            region=region,  # ✅ OBLIGATORIO según PDF
            iops=self._config.get('iops')  # ✅ OPCIONAL según PDF
        )
        
        # ✅ VALIDACIÓN DE REGIÓN (RNF3, RF5)
        if network.region != disk.region:
            logger.error(f"Error de coherencia: Network región={network.region}, Disk región={disk.region}")
            raise ValueError(f"Error: La región de Network y Disk deben coincidir. Network: {network.region}, Disk: {disk.region}")
        
        vm_id = f"aws-{uuid.uuid4()}"
        
        # Crear VM con todos los parámetros obligatorios del PDF (Página 2)
        vm = MachineVirtual(
            vmId=vm_id,
            name=self._config.get('name', f"aws-vm-{vm_id[:4]}"),
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider='aws',  # ✅ OBLIGATORIO
            vcpus=self._config.get('vcpus', 2),  # ✅ OBLIGATORIO
            memoryGB=self._config.get('memoryGB', 4),  # ✅ OBLIGATORIO
            network=network,
            disks=[disk],
            memoryOptimization=self._config.get('memoryOptimization'),  # ✅ OPCIONAL
            diskOptimization=self._config.get('diskOptimization'),  # ✅ OPCIONAL
            keyPairName=self._config.get('keyPairName'),  # ✅ OPCIONAL
            instance_type=self._config.get('instance_type')
        )
        
        logger.info(f"AWS Builder: VM construida exitosamente - ID: {vm_id}, Instance: {vm.instance_type}, vCPUs: {vm.vcpus}, RAM: {vm.memoryGB}GB")
        logger.info(f"AWS Builder: Validación de región exitosa - Región: {region}")
        
        return vm