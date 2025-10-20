import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
import logging

from domain.builder import VMBuilder
from domain.entities import MachineVirtual, VMStatus, Network, StorageDisk, VMInstanceType

logger = logging.getLogger(__name__)


class AWSVMBuilder(VMBuilder):
    
    
    def __init__(self):
        super().__init__()
        self._config = {
            'provider': 'aws',
            'region': 'us-east-1',
            'instance_type': 't3.medium',  
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
        
        self._config['name'] = name
        self._config['vm_type'] = vm_type
        
        
        if vm_type == 'standard':
            self._config['instance_type'] = 't3.medium'  
            self._config['memoryOptimization'] = False
            self._config['diskOptimization'] = False
        elif vm_type == 'memory-optimized':
            self._config['instance_type'] = 'r5.large'  
            self._config['memoryOptimization'] = True
            self._config['diskOptimization'] = False
        elif vm_type == 'disk-optimized':
            self._config['instance_type'] = 'c5.large'  
            self._config['memoryOptimization'] = False
            self._config['diskOptimization'] = True
        else:
            
            self._config['instance_type'] = vm_type
        
        
        specs = VMInstanceType.get_specs('aws', self._config['instance_type'])
        if specs:
            self._config['vcpus'] = specs['vcpus']
            self._config['memoryGB'] = specs['memoryGB']
        
        logger.info(f"AWS Builder: Configuración básica - Nombre: {name}, Tipo: {vm_type}, Instance: {self._config['instance_type']}")
        return self

    def set_instance_type(self, instance_type: str) -> 'AWSVMBuilder':
        
        self._config['instance_type'] = instance_type
        
        
        specs = VMInstanceType.get_specs('aws', instance_type)
        if specs:
            self._config['vcpus'] = specs['vcpus']
            self._config['memoryGB'] = specs['memoryGB']
            logger.info(f"AWS Builder: Instance Type configurado - {instance_type} ({specs['vcpus']} vCPUs, {specs['memoryGB']} GB RAM)")
        else:
            logger.warning(f"AWS Builder: Instance Type '{instance_type}' no reconocido, usando valores por defecto")
        
        return self

    def set_compute_resources(self, cpu: Optional[int] = None, ram: Optional[int] = None) -> 'AWSVMBuilder':
       
        if cpu is not None:
            self._config['vcpus'] = cpu
        if ram is not None:
            self._config['memoryGB'] = ram
        
        logger.info(f"AWS Builder: Recursos de cómputo - CPU: {self._config['vcpus']}, RAM: {self._config['memoryGB']}GB")
        return self

    def set_storage(self, size_gb: int, disk_type: Optional[str] = None,
                    iops: Optional[int] = None) -> 'AWSVMBuilder':
        
        self._config['size_gb'] = size_gb
        
        disk_mapping = {
            'ssd': 'gp3',
            'standard': 'gp2',
            'magnetic': 'standard',
            'io': 'io2'
        }
        self._config['volume_type'] = disk_mapping.get(disk_type, 'gp2') if disk_type else 'gp2'
        
        
        if iops is not None:
            self._config['iops'] = iops
        
        logger.info(f"AWS Builder: Almacenamiento - {size_gb}GB, Tipo: {self._config['volume_type']}, IOPS: {iops}")
        return self

    def set_network(self, network_id: Optional[str] = None, cidr: Optional[str] = None,
                    firewall_rules: Optional[list] = None, public_ip: Optional[bool] = None) -> 'AWSVMBuilder':
        
        self._config['vpc_id'] = network_id or f"vpc-{uuid.uuid4().hex[:8]}"
        self._config['cidr_block'] = cidr or '10.0.0.0/16'
        
        
        if firewall_rules is not None:
            self._config['firewallRules'] = firewall_rules
        if public_ip is not None:
            self._config['publicIP'] = public_ip
        
        logger.info(f"AWS Builder: Red - VPC: {self._config['vpc_id']}, Firewall: {firewall_rules}, Public IP: {public_ip}")
        return self

    def set_location(self, location: str) -> 'AWSVMBuilder':
        
        self._config['region'] = location
        logger.info(f"AWS Builder: Ubicación - Región: {location}")
        return self

    def set_advanced_options(self, options: Dict[str, Any]) -> 'AWSVMBuilder':
        
        if 'memoryOptimization' in options:
            self._config['memoryOptimization'] = options['memoryOptimization']
        if 'diskOptimization' in options:
            self._config['diskOptimization'] = options['diskOptimization']
        if 'keyPairName' in options:
            self._config['keyPairName'] = options['keyPairName']
        
        
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
        
        region = self._config.get('region', 'us-east-1')
        
        
        network = Network(
            networkId=self._config.get('vpc_id', f"vpc-{uuid.uuid4().hex[:8]}"),
            name=f"aws-net-{region}",
            cidr_block=self._config.get('cidr_block', '10.0.0.0/16'),
            provider='aws',
            region=region,  
            firewallRules=self._config.get('firewallRules'),  
            publicIP=self._config.get('publicIP')  
        )
        
        
        disk = StorageDisk(
            diskId=f"vol-{uuid.uuid4().hex[:12]}",
            name=f"aws-disk-{self._config.get('volume_type', 'gp2')}",
            size_gb=self._config.get('size_gb', 50),
            disk_type=self._config.get('volume_type', 'gp2'),
            provider='aws',
            region=region,  
            iops=self._config.get('iops')  
        )
        
        
        if network.region != disk.region:
            logger.error(f"Error de coherencia: Network región={network.region}, Disk región={disk.region}")
            raise ValueError(f"Error: La región de Network y Disk deben coincidir. Network: {network.region}, Disk: {disk.region}")
        
        vm_id = f"aws-{uuid.uuid4()}"
        
        
        vm = MachineVirtual(
            vmId=vm_id,
            name=self._config.get('name', f"aws-vm-{vm_id[:4]}"),
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider='aws',  
            vcpus=self._config.get('vcpus', 2),  
            memoryGB=self._config.get('memoryGB', 4),  
            network=network,
            disks=[disk],
            memoryOptimization=self._config.get('memoryOptimization'),  
            diskOptimization=self._config.get('diskOptimization'),  
            keyPairName=self._config.get('keyPairName'),  
            instance_type=self._config.get('instance_type')
        )
        
        logger.info(f"AWS Builder: VM construida exitosamente - ID: {vm_id}, Instance: {vm.instance_type}, vCPUs: {vm.vcpus}, RAM: {vm.memoryGB}GB")
        logger.info(f"AWS Builder: Validación de región exitosa - Región: {region}")
        
        return vm