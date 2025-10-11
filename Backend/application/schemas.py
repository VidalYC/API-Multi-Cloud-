"""
Esquemas de Validación de Configuración con Pydantic

Define la estructura y las reglas de validación para el objeto `config`
de cada proveedor, cumpliendo con la extensión opcional del PDF.
"""
from pydantic import BaseModel, Field
from typing import Optional, Type, Dict, Any


class AWSConfig(BaseModel):
    """Esquema de validación para AWS."""
    type: str = Field(default='t2.micro', description="Tipo de instancia de AWS")
    region: str = Field(default='us-east-1', description="Región de AWS")
    sizeGB: int = Field(default=20, gt=0, description="Tamaño del disco en GB")
    volumeType: str = Field(default='gp2', description="Tipo de volumen EBS")
    vpcId: Optional[str] = None


class AzureConfig(BaseModel):
    """Esquema de validación para Azure."""
    type: str = Field(default='Standard_B1s', description="Tamaño de la VM en Azure")
    resource_group: str = Field(default='default-rg', description="Grupo de recursos")
    sizeGB: int = Field(default=30, gt=0, description="Tamaño del disco en GB")
    diskSku: str = Field(default='Standard_LRS', description="SKU del disco")
    virtualNetwork: Optional[str] = None


class GoogleConfig(BaseModel):
    """Esquema de validación para Google Cloud."""
    type: str = Field(default='n1-standard-1', description="Tipo de máquina en GCP")
    zone: str = Field(default='us-central1-a', description="Zona de GCP")
    sizeGB: int = Field(default=10, gt=0, description="Tamaño del disco en GB")
    diskType: str = Field(default='pd-standard', description="Tipo de disco persistente")
    networkName: Optional[str] = None


class OnPremiseConfig(BaseModel):
    """Esquema de validación para On-Premise."""
    cpu: int = Field(default=2, gt=0, description="Número de CPUs")
    ram: int = Field(default=4, gt=0, description="RAM en GB")
    disk: int = Field(default=50, gt=0, description="Disco en GB")
    vlanId: Optional[int] = None
    storagePool: Optional[str] = None
    raidLevel: Optional[int] = None


# Mapeo para obtener el validador correcto
_validators: Dict[str, Type[BaseModel]] = {
    'aws': AWSConfig,
    'azure': AzureConfig,
    'google': GoogleConfig,
    'gcp': GoogleConfig,
    'onpremise': OnPremiseConfig,
    'on-premise': OnPremiseConfig
}

def get_validator_for(provider_type: str) -> Optional[Type[BaseModel]]:
    """Retorna la clase de validación para un proveedor."""
    return _validators.get(provider_type.lower().strip())