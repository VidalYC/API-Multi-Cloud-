import uuid
from datetime import datetime
from typing import Dict, Any
import logging

from domain.interfaces import ProveedorAbstracto
from domain.entities import MachineVirtual, VMStatus

# Obtener logger 
logger = logging.getLogger(__name__)


class AWS(ProveedorAbstracto):
    """
    Concrete Creator: Implementación específica para AWS
    """
    
    def __init__(self, field_type: str, method_type: str):
        super().__init__()
        self.field = field_type
        self.method = method_type
    
    def crear_vm(self) -> MachineVirtual:
        """Factory Method implementado para AWS"""
        vm_id = f"aws-{uuid.uuid4()}"
        
        logger.info(f"Creando VM en AWS - ID: {vm_id}, Tipo: {self.field}")
        
        # Simulación de creación en AWS
        vm = MachineVirtual(
            vmId=vm_id,
            name=f"aws-instance-{vm_id[:8]}",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="aws"
        )
        
        return vm


class Azure(ProveedorAbstracto):
    """
    Concrete Creator: Implementación específica para Azure
    """
    
    def __init__(self, field_type: str, method_type: str):
        super().__init__()
        self.field = field_type
        self.method = method_type
    
    def crear_vm(self) -> MachineVirtual:
        """Factory Method implementado para Azure"""
        vm_id = f"azure-{uuid.uuid4()}"
        
        logger.info(f"Creando VM en Azure - ID: {vm_id}, Tipo: {self.field}")
        
        vm = MachineVirtual(
            vmId=vm_id,
            name=f"azure-vm-{vm_id[:8]}",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="azure"
        )
        
        return vm


class Google(ProveedorAbstracto):
    """
    Concrete Creator: Implementación específica para Google Cloud
    """
    
    def __init__(self, field_type: str, method_type: str):
        super().__init__()
        self.field = field_type
        self.method = method_type
    
    def crear_vm(self) -> MachineVirtual:
        """Factory Method implementado para GCP"""
        vm_id = f"gcp-{uuid.uuid4()}"
        
        logger.info(f"Creando VM en Google Cloud - ID: {vm_id}, Tipo: {self.field}")
        
        vm = MachineVirtual(
            vmId=vm_id,
            name=f"gcp-instance-{vm_id[:8]}",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="google"
        )
        
        return vm


class OnPremise(ProveedorAbstracto):
    """
    Concrete Creator: Implementación específica para On-Premise
    """
    
    def __init__(self, field_type: str, method_type: str):
        super().__init__()
        self.field = field_type
        self.method = method_type
    
    def crear_vm(self) -> MachineVirtual:
        """Factory Method implementado para On-Premise"""
        vm_id = f"onprem-{uuid.uuid4()}"
        
        logger.info(f"Creando VM On-Premise - ID: {vm_id}, Tipo: {self.field}")
        
        vm = MachineVirtual(
            vmId=vm_id,
            name=f"onprem-vm-{vm_id[:8]}",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="on-premise"
        )
        
        return vm


# Concrete Products: VMs específicas por proveedor

class AWSVM:
    """Producto concreto: VM de AWS con parámetros específicos"""
    
    def __init__(self, tipo_instancia: bool, region: str, vpc: str, ami: str):
        self.TipoInstancia = tipo_instancia
        self.Region = region
        self.VPC = vpc
        self.AMI = ami
    
    def provisionar(self):
        logger.info(f"Aprovisionando AWS VM - Region: {self.Region}, VPC: {self.VPC}")
        return f"AWS VM creada en {self.Region}"


class AzureVM:
    """Producto concreto: VM de Azure con parámetros específicos"""
    
    def __init__(self, tamano_maquina: str, resource_group: str, imagen: str, red_v: str):
        self.TamanoMaquina = tamano_maquina
        self.resource_group = resource_group
        self.imagen = imagen
        self.red_v = red_v
    
    def provisionar(self):
        logger.info(f"Aprovisionando Azure VM - Resource Group: {self.resource_group}")
        return f"Azure VM creada en {self.resource_group}"


class GoogleChromeVM:
    """Producto concreto: VM de Google Cloud con parámetros específicos"""
    
    def __init__(self, tipo_mo: str, zona: str, disco_base: str, proyecto: str):
        self.TipoMo = tipo_mo
        self.zona = zona
        self.DiscoBase = disco_base
        self.Proyecto = proyecto
    
    def provisionar(self):
        logger.info(f"Aprovisionando GCP VM - Proyecto: {self.Proyecto}, Zona: {self.zona}")
        return f"GCP VM creada en proyecto {self.Proyecto}"


class OnPremiseVM:
    """Producto concreto: VM On-Premise con parámetros específicos"""
    
    def __init__(self, rc_cpu: int, ram: int, disco: int, red_fisica: str):
        self.Rc_CPU = rc_cpu
        self.ram = ram
        self.disco = disco
        self.Red_Fisica = red_fisica
    
    def provisionar(self):
        logger.info(f"Aprovisionando On-Premise VM - CPU: {self.Rc_CPU}, RAM: {self.ram}GB")
        return f"On-Premise VM creada con {self.Rc_CPU} CPUs y {self.ram}GB RAM"