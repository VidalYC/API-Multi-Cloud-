# 🎨 PATRONES DE DISEÑO Y DIAGRAMAS UML
## Documentación Completa con Diagramas

**Universidad Popular del Cesar**
**Especialización en Ingeniería de Software**
**Proyecto:** API Multi-Cloud VM Provisioning

---

## 📋 TABLA DE CONTENIDOS

1. [Factory Method Pattern - Explicación Completa](#1-factory-method-pattern)
2. [Abstract Factory Pattern - Explicación Completa](#2-abstract-factory-pattern)
3. [Builder Pattern - Explicación Completa](#3-builder-pattern)
4. [Director Pattern - Explicación Completa](#4-director-pattern)
5. [Diagramas UML de Clases](#5-diagramas-uml-de-clases)
6. [Diagramas de Secuencia](#6-diagramas-de-secuencia)
7. [Diagramas de Colaboración](#7-diagramas-de-colaboración)
8. [Comparación de Patrones](#8-comparación-de-patrones)

---

## 1. FACTORY METHOD PATTERN

### 📖 Definición Formal

> **Factory Method** es un patrón de diseño creacional que proporciona una interfaz para crear objetos en una superclase, pero permite que las subclases alteren el tipo de objetos que se crearán.

### 🎯 Problema que Resuelve

**Escenario:**
Tienes una aplicación que necesita crear diferentes tipos de objetos (AWS VMs, Azure VMs, Google VMs), pero no quieres acoplar tu código a clases concretas específicas.

**Sin Factory Method:**
```python
# ❌ Código acoplado y difícil de mantener
def provisionar_vm(proveedor, config):
    if proveedor == "aws":
        vm = AWS(config)  # Acoplamiento a clase concreta
        vm.crear()
    elif proveedor == "azure":
        vm = Azure(config)  # Más acoplamiento
        vm.crear()
    elif proveedor == "google":
        vm = Google(config)  # Aún más acoplamiento
        vm.crear()
    # ¿Agregar Oracle? Modificar toda esta función ❌ OCP
```

**Problemas:**
- ❌ Violación de Open/Closed Principle
- ❌ Alto acoplamiento
- ❌ Difícil de testear
- ❌ No escalable

**Con Factory Method:**
```python
# ✅ Código desacoplado y extensible
def provisionar_vm(proveedor, config):
    provider = VMProviderFactory.create_provider(proveedor, config)
    return provider.provisionar()  # Polimorfismo
```

**Beneficios:**
- ✅ Cumple Open/Closed Principle
- ✅ Bajo acoplamiento
- ✅ Fácil de testear (mocks)
- ✅ Escalable

### 🏗️ Estructura del Patrón

#### Participantes:

1. **Product (Producto):**
   - Define la interfaz de los objetos que el factory method crea
   - En nuestro caso: `ProveedorAbstracto`

2. **Concrete Products (Productos Concretos):**
   - Implementaciones específicas del producto
   - En nuestro caso: `AWS`, `Azure`, `Google`, `OnPremise`

3. **Creator (Creador):**
   - Declara el factory method
   - Puede proporcionar implementación por defecto
   - En nuestro caso: `ProveedorAbstracto` (también actúa como creator con `provisionar()`)

4. **Concrete Creators (Creadores Concretos):**
   - Sobrescriben el factory method para retornar diferentes tipos de productos
   - En nuestro caso: Cada proveedor implementa `crear_vm()`

5. **Factory (Fábrica):**
   - Clase auxiliar que centraliza la creación
   - En nuestro caso: `VMProviderFactory`

### 💻 Implementación en el Proyecto

#### Paso 1: Product (Interfaz Común)

```python
# domain/interfaces.py
from abc import ABC, abstractmethod
from domain.entities import MachineVirtual

class ProveedorAbstracto(ABC):
    """
    Product: Define la interfaz común para todos los proveedores

    Esta es la abstracción que permite el polimorfismo
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Constructor común

        Args:
            config: Configuración específica del proveedor
        """
        self.config = config

    @abstractmethod
    def crear_vm(self) -> MachineVirtual:
        """
        Factory Method: Método abstracto que cada proveedor implementa

        Este es el núcleo del patrón Factory Method.
        Cada subclase decide QUÉ tipo de VM crear.

        Returns:
            MachineVirtual: VM específica del proveedor
        """
        pass

    @abstractmethod
    def estado(self) -> bool:
        """
        Verifica si el proveedor está disponible

        Returns:
            bool: True si está disponible
        """
        pass

    def provisionar(self) -> MachineVirtual:
        """
        Template Method: Define el algoritmo de aprovisionamiento

        Este método orquesta el proceso:
        1. Verifica estado
        2. Llama al factory method (crear_vm)
        3. Retorna resultado

        Returns:
            MachineVirtual: VM provisionada
        """
        if not self.estado():
            raise Exception(f"Proveedor no disponible")

        # Aquí llamamos al factory method
        vm = self.crear_vm()  # Polimorfismo: cada subclase implementa diferente

        return vm
```

**Análisis del Código:**

- `ProveedorAbstracto` es el **Product** y **Creator** al mismo tiempo
- `crear_vm()` es el **Factory Method** (método abstracto)
- `provisionar()` es un **Template Method** que usa el Factory Method
- Las subclases implementan `crear_vm()` de forma específica

#### Paso 2: Concrete Products (Proveedores Específicos)

```python
# infrastructure/providers/aws.py
import uuid
from datetime import datetime
from domain.interfaces import ProveedorAbstracto
from domain.entities import MachineVirtual, VMStatus, Network, StorageDisk

class AWS(ProveedorAbstracto):
    """
    Concrete Product: Implementación específica para AWS

    Sobrescribe el Factory Method para crear VMs de AWS
    """

    def crear_vm(self) -> MachineVirtual:
        """
        Factory Method Implementation: Crea VM específica de AWS

        Pasos:
        1. Extrae configuración específica de AWS
        2. Crea recursos relacionados (Network, Storage)
        3. Ensambla la VM
        4. Retorna VM con todo configurado

        Returns:
            MachineVirtual: VM de AWS completamente configurada
        """
        # Generar ID único con formato AWS
        vm_id = f"aws-{uuid.uuid4()}"

        # Extraer configuración
        instance_type = self.config.get('type', 't2.micro')
        region = self.config.get('region', 'us-east-1')
        size_gb = self.config.get('sizeGB', 20)
        volume_type = self.config.get('volumeType', 'gp2')

        # Crear recursos relacionados (Abstract Factory implícito)

        # 1. Network (VPC de AWS)
        network = Network(
            networkId=f"vpc-{uuid.uuid4().hex[:8]}",  # Formato AWS
            name=f"aws-net-{region}",
            cidr_block="10.0.0.0/16",
            provider="aws"
        )

        # 2. Storage (EBS Volume)
        disk = StorageDisk(
            diskId=f"vol-{uuid.uuid4().hex[:12]}",  # Formato AWS
            name=f"aws-disk-{volume_type}",
            size_gb=size_gb,
            disk_type=volume_type,
            provider="aws"
        )

        # 3. VM (EC2 Instance)
        vm = MachineVirtual(
            vmId=vm_id,
            name=f"aws-{instance_type}-{region}-{vm_id[:4]}",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="aws",
            network=network,
            disks=[disk]
        )

        return vm

    def estado(self) -> bool:
        """
        Implementación: Verifica disponibilidad de AWS

        En un sistema real:
        - Verificaría conexión con AWS API
        - Validaría credenciales
        - Comprobaría cuotas

        Returns:
            bool: True (simulado como siempre disponible)
        """
        return True
```

**Análisis:**

- `AWS` es un **Concrete Product**
- Implementa `crear_vm()` de forma específica para AWS
- Usa nomenclatura y convenciones de AWS (vpc-, vol-, etc.)
- Crea familia de recursos relacionados (Network, Storage, VM)

```python
# infrastructure/providers/azure.py
class Azure(ProveedorAbstracto):
    """Concrete Product: Implementación para Azure"""

    def crear_vm(self) -> MachineVirtual:
        """Factory Method: Crea VM de Azure con sus especificidades"""
        vm_id = f"azure-{uuid.uuid4()}"

        # Configuración específica de Azure
        vm_size = self.config.get('type', 'Standard_B1s')
        resource_group = self.config.get('resource_group', 'default-rg')

        # Network (VNet de Azure)
        network = Network(
            networkId=f"vnet-{resource_group}",  # Formato Azure
            name=f"azure-net-{resource_group}",
            cidr_block="10.1.0.0/16",
            provider="azure"
        )

        # Storage (Managed Disk)
        disk = StorageDisk(
            diskId=f"disk-{uuid.uuid4().hex[:8]}",
            name=f"azure-disk-{resource_group}",
            size_gb=self.config.get('sizeGB', 30),
            disk_type=self.config.get('diskSku', 'Standard_LRS'),
            provider="azure"
        )

        # VM
        vm = MachineVirtual(
            vmId=vm_id,
            name=f"azure-{vm_size}-{vm_id[:4]}",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="azure",
            network=network,
            disks=[disk]
        )

        return vm

    def estado(self) -> bool:
        return True
```

#### Paso 3: Factory (Centralizador de Creación)

```python
# application/factory.py
from typing import Dict, Any, Optional

class VMProviderFactory:
    """
    Factory: Centraliza la creación de proveedores

    Esta clase no es parte estándar del patrón Factory Method,
    pero es una práctica común para:
    - Centralizar la lógica de selección
    - Facilitar el registro de nuevos proveedores
    - Aplicar Open/Closed Principle

    Responsabilidades:
    1. Mantener registro de proveedores disponibles
    2. Crear instancias según el tipo solicitado
    3. Permitir registro dinámico de nuevos proveedores
    """

    # Registro de proveedores (mapeo string -> clase)
    _providers = {
        'aws': AWS,
        'azure': Azure,
        'google': Google,
        'gcp': Google,  # Alias
        'onpremise': OnPremise,
        'on-premise': OnPremise  # Alias
    }

    @classmethod
    def create_provider(cls, provider_type: str, config: Dict[str, Any]) -> Optional[ProveedorAbstracto]:
        """
        Factory Method Principal: Crea proveedor según tipo

        Este método implementa el patrón Factory Method a nivel de fábrica:
        1. Recibe tipo de proveedor como string
        2. Busca clase correspondiente en el registro
        3. Instancia la clase
        4. Retorna como abstracción (ProveedorAbstracto)

        Args:
            provider_type: Tipo de proveedor ('aws', 'azure', etc.)
            config: Configuración específica del proveedor

        Returns:
            ProveedorAbstracto: Instancia del proveedor (polimorfismo)
            None: Si el proveedor no existe

        Ejemplo:
            >>> provider = VMProviderFactory.create_provider('aws', {'type': 't2.micro'})
            >>> vm = provider.provisionar()  # Polimorfismo en acción
        """
        # Normalizar entrada
        provider_type = provider_type.lower().strip()

        # Buscar clase en registro
        provider_class = cls._providers.get(provider_type)

        if provider_class is None:
            logger.error(f"Proveedor no soportado: {provider_type}")
            return None

        try:
            # Crear instancia de la clase concreta
            # Importante: Se retorna como ProveedorAbstracto (abstracción)
            provider = provider_class(config)

            logger.info(f"Proveedor creado exitosamente: {provider_type}")
            return provider  # Retorna abstracción, no implementación concreta

        except Exception as e:
            logger.error(f"Error creando proveedor {provider_type}: {str(e)}")
            return None

    @classmethod
    def register_provider(cls, name: str, provider_class):
        """
        Registro Dinámico: Permite agregar nuevos proveedores sin modificar código

        Este método es clave para cumplir Open/Closed Principle:
        - Abierto para extensión: Podemos agregar nuevos proveedores
        - Cerrado para modificación: No modificamos la fábrica internamente

        Args:
            name: Nombre del proveedor
            provider_class: Clase que implementa ProveedorAbstracto

        Ejemplo:
            >>> class Oracle(ProveedorAbstracto):
            ...     def crear_vm(self): ...
            >>> VMProviderFactory.register_provider('oracle', Oracle)
            >>> # Ahora 'oracle' está disponible sin modificar Factory
        """
        cls._providers[name.lower()] = provider_class
        logger.info(f"Proveedor registrado: {name}")

    @classmethod
    def get_available_providers(cls) -> list:
        """
        Retorna lista de proveedores disponibles

        Returns:
            list: Lista de nombres de proveedores
        """
        return list(cls._providers.keys())
```

### 🎨 Diagrama UML - Factory Method

```
┌─────────────────────────────────────────────────────────────────┐
│                     <<interface>>                                │
│                   ProveedorAbstracto                             │
├─────────────────────────────────────────────────────────────────┤
│ # config: Dict[str, Any]                                         │
├─────────────────────────────────────────────────────────────────┤
│ + __init__(config: Dict)                                         │
│ + provisionar(): MachineVirtual                                  │
│ + estado(): bool                                                 │
│ + crear_vm(): MachineVirtual  «abstract» «factory method»       │
└──────────────────┬──────────────────────────────────────────────┘
                   │
                   │ implements
        ┌──────────┴────────┬────────────┬──────────────┐
        │                   │            │              │
┌───────▼────────┐ ┌────────▼─────┐ ┌───▼────────┐ ┌──▼──────────┐
│      AWS       │ │    Azure     │ │   Google   │ │  OnPremise  │
├────────────────┤ ├──────────────┤ ├────────────┤ ├─────────────┤
│ crear_vm()     │ │ crear_vm()   │ │crear_vm()  │ │ crear_vm()  │
│ estado()       │ │ estado()     │ │estado()    │ │ estado()    │
└────────┬───────┘ └──────┬───────┘ └────┬───────┘ └──────┬──────┘
         │                │              │                 │
         │ creates        │ creates      │ creates         │ creates
         │                │              │                 │
┌────────▼──────────────────────────────────────────────────────────┐
│                                                                    │
│                      MachineVirtual                                │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐          │
│  │   Network    │   │ StorageDisk  │   │  VMStatus    │          │
│  └──────────────┘   └──────────────┘   └──────────────┘          │
└────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    VMProviderFactory                             │
│                     «static factory»                             │
├─────────────────────────────────────────────────────────────────┤
│ - _providers: Dict[str, Type[ProveedorAbstracto]]               │
├─────────────────────────────────────────────────────────────────┤
│ + create_provider(type: str, config: Dict): ProveedorAbstracto  │
│ + register_provider(name: str, class: Type)                     │
│ + get_available_providers(): List[str]                          │
└─────────────────────────────────────────────────────────────────┘
            │
            │ uses
            ▼
   ┌────────────────┐
   │ProveedorAbstracto│
   └────────────────┘
```

### 🔄 Diagrama de Secuencia - Factory Method

```
Cliente        VMProviderFactory      AWS           MachineVirtual
  │                   │                │                  │
  │ 1. create_provider("aws", config) │                  │
  ├──────────────────>│                │                  │
  │                   │                │                  │
  │                   │ 2. new AWS(config)                │
  │                   ├───────────────>│                  │
  │                   │                │                  │
  │                   │ 3. return AWS instance            │
  │                   │<───────────────┤                  │
  │                   │                │                  │
  │ 4. return ProveedorAbstracto       │                  │
  │<──────────────────┤                │                  │
  │                   │                │                  │
  │ 5. provisionar()  │                │                  │
  ├──────────────────────────────────>│                  │
  │                   │                │                  │
  │                   │                │ 6. crear_vm()    │
  │                   │                │                  │
  │                   │                │ 7. new MachineVirtual()
  │                   │                ├─────────────────>│
  │                   │                │                  │
  │                   │                │ 8. return VM     │
  │                   │                │<─────────────────┤
  │                   │                │                  │
  │ 9. return VM      │                │                  │
  │<──────────────────────────────────┤                  │
  │                   │                │                  │
```

### 💡 Explicación Paso a Paso

**Escenario:** Cliente quiere aprovisionar VM en AWS

```python
# 1. Cliente solicita creación
provider = VMProviderFactory.create_provider('aws', {'type': 't2.micro'})
```

**¿Qué pasa internamente?**

1. **Factory busca en registro:**
   ```python
   # _providers = {'aws': AWS, 'azure': Azure, ...}
   provider_class = _providers.get('aws')  # Obtiene clase AWS
   ```

2. **Factory instancia la clase:**
   ```python
   provider = provider_class(config)  # provider = AWS(config)
   ```

3. **Factory retorna como abstracción:**
   ```python
   return provider  # Tipo: ProveedorAbstracto, no AWS
   ```

```python
# 2. Cliente aprovisiona
vm = provider.provisionar()
```

**¿Qué pasa internamente?**

1. **provisionar() llama a crear_vm():**
   ```python
   def provisionar(self):
       vm = self.crear_vm()  # Polimorfismo: AWS.crear_vm()
       return vm
   ```

2. **AWS.crear_vm() crea recursos:**
   ```python
   def crear_vm(self):
       network = Network(...)  # VPC de AWS
       disk = StorageDisk(...)  # EBS de AWS
       vm = MachineVirtual(...)  # EC2 Instance
       return vm
   ```

### 📊 Ventajas del Factory Method

| Ventaja | Descripción | Ejemplo en el Proyecto |
|---------|-------------|------------------------|
| **Desacoplamiento** | Cliente no conoce clases concretas | `VMProvisioningService` no conoce `AWS`, solo `ProveedorAbstracto` |
| **Extensibilidad** | Agregar nuevos tipos sin modificar código | Agregar Oracle: crear clase, registrar, listo |
| **Polimorfismo** | Tratar diferentes tipos uniformemente | Cualquier proveedor puede usarse con `provisionar()` |
| **SRP** | Creación separada de uso | `VMProviderFactory` crea, `Service` usa |
| **OCP** | Abierto extensión, cerrado modificación | `register_provider()` permite extensión |
| **Testabilidad** | Fácil usar mocks | Test puede inyectar mock de `ProveedorAbstracto` |

### ⚠️ Cuándo Usar Factory Method

**Usar cuando:**
- ✅ No sabes de antemano qué tipos exactos de objetos necesitarás
- ✅ Quieres que los usuarios de tu biblioteca extiendan componentes
- ✅ Quieres ahorrar recursos reutilizando objetos existentes
- ✅ Necesitas crear familias de objetos relacionados

**No usar cuando:**
- ❌ Solo tienes un tipo de objeto (usar constructor simple)
- ❌ La creación es trivial sin lógica compleja
- ❌ No planeas agregar más tipos en el futuro

---

## 2. ABSTRACT FACTORY PATTERN

### 📖 Definición Formal

> **Abstract Factory** es un patrón de diseño creacional que permite producir familias de objetos relacionados sin especificar sus clases concretas.

### 🎯 Problema que Resuelve

**Escenario:**
Necesitas crear no solo UNA VM, sino una FAMILIA de recursos relacionados:
- VM (EC2, Azure VM, Compute Instance)
- Network (VPC, VNet, VPC Network)
- Storage (EBS, Managed Disk, Persistent Disk)

Y todos deben ser **compatibles entre sí** (mismo proveedor).

**Sin Abstract Factory:**
```python
# ❌ Recursos incompatibles
def crear_recursos():
    vm = AWS.crear_vm()
    network = Azure.crear_network()  # ¡Error! Red de Azure con VM de AWS
    storage = Google.crear_storage()  # ¡Error! Storage de Google

    # Recursos incompatibles entre proveedores
```

**Con Abstract Factory:**
```python
# ✅ Familia de recursos coherente
def crear_recursos(provider):
    vm = provider.crear_vm()  # VM de AWS
    # Internamente, provider también crea:
    # - Network de AWS (compatible)
    # - Storage de AWS (compatible)

    # Todos los recursos son del mismo proveedor
```

### 🏗️ Estructura del Patrón

#### Participantes:

1. **Abstract Factory:**
   - Declara interfaz para crear familia de productos
   - En nuestro caso: `ProveedorAbstracto` (implícito)

2. **Concrete Factories:**
   - Implementan operaciones para crear productos
   - En nuestro caso: `AWS`, `Azure`, `Google`, `OnPremise`

3. **Abstract Products:**
   - Declaran interfaces para tipos de productos
   - En nuestro caso: `MachineVirtual`, `Network`, `StorageDisk`

4. **Concrete Products:**
   - Implementaciones específicas de productos
   - En nuestro caso: Instances con provider='aws', provider='azure', etc.

### 💻 Implementación en el Proyecto

#### Familia de Productos

```python
# domain/entities.py

class Network:
    """
    Abstract Product: Representa red

    Cada proveedor crea su propia versión:
    - AWS: VPC
    - Azure: VNet
    - Google: VPC Network
    - OnPremise: VLAN
    """

    def __init__(self, networkId: str, name: str, cidr_block: str, provider: str):
        self.networkId = networkId
        self.name = name
        self.cidr_block = cidr_block
        self.provider = provider  # Identificador de familia

    def to_dict(self) -> Dict:
        return {
            'networkId': self.networkId,
            'name': self.name,
            'cidr_block': self.cidr_block,
            'provider': self.provider
        }


class StorageDisk:
    """
    Abstract Product: Representa almacenamiento

    Cada proveedor crea su propia versión:
    - AWS: EBS Volume
    - Azure: Managed Disk
    - Google: Persistent Disk
    - OnPremise: Local Disk
    """

    def __init__(self, diskId: str, name: str, size_gb: int, disk_type: str, provider: str):
        self.diskId = diskId
        self.name = name
        self.size_gb = size_gb
        self.disk_type = disk_type
        self.provider = provider  # Identificador de familia

    def to_dict(self) -> Dict:
        return {
            'diskId': self.diskId,
            'name': self.name,
            'size_gb': self.size_gb,
            'disk_type': self.disk_type,
            'provider': self.provider
        }


class MachineVirtual:
    """
    Abstract Product: Representa máquina virtual

    Cada proveedor crea su propia versión:
    - AWS: EC2 Instance
    - Azure: Azure VM
    - Google: Compute Instance
    - OnPremise: KVM/VMware VM
    """

    def __init__(self, vmId: str, name: str, status: VMStatus,
                 createdAt: datetime, provider: str,
                 network: Network, disks: List[StorageDisk]):
        self.vmId = vmId
        self.name = name
        self.status = status
        self.createdAt = createdAt
        self.provider = provider  # Identificador de familia
        self.network = network  # Red relacionada
        self.disks = disks  # Storage relacionado

    def to_dict(self) -> Dict:
        return {
            'vmId': self.vmId,
            'name': self.name,
            'status': self.status.value,
            'createdAt': self.createdAt.isoformat(),
            'provider': self.provider,
            'network': self.network.to_dict(),
            'disks': [disk.to_dict() for disk in self.disks]
        }
```

#### Concrete Factory (AWS)

```python
# infrastructure/providers/aws.py

class AWS(ProveedorAbstracto):
    """
    Concrete Factory: Crea familia de productos AWS

    Garantiza que todos los recursos sean compatibles:
    - VPC (Network de AWS)
    - EBS Volume (Storage de AWS)
    - EC2 Instance (VM de AWS)

    Todos comparten:
    - provider = 'aws'
    - region = misma región
    - Nomenclatura consistente (vpc-, vol-, i-)
    """

    def crear_vm(self) -> MachineVirtual:
        """
        Factory Method que coordina creación de familia completa

        Pasos:
        1. Crear Network (producto de familia AWS)
        2. Crear Storage (producto de familia AWS)
        3. Crear VM (producto de familia AWS)
        4. Ensamblar familia completa

        Returns:
            MachineVirtual: Con Network y Storage de la misma familia
        """
        # Extraer configuración
        region = self.config.get('region', 'us-east-1')

        # 1. Crear Network de la familia AWS
        network = self._crear_network_aws(region)

        # 2. Crear Storage de la familia AWS
        storage = self._crear_storage_aws(region)

        # 3. Crear VM de la familia AWS
        vm = self._crear_vm_aws(network, storage, region)

        return vm

    def _crear_network_aws(self, region: str) -> Network:
        """
        Crea Network específica de AWS (VPC)

        Características AWS:
        - ID con formato vpc-xxxxxxxx
        - CIDR block configurado
        - provider = 'aws'

        Args:
            region: Región de AWS

        Returns:
            Network: VPC de AWS
        """
        return Network(
            networkId=f"vpc-{uuid.uuid4().hex[:8]}",  # Formato AWS
            name=f"aws-net-{region}",
            cidr_block="10.0.0.0/16",  # CIDR típico de AWS
            provider="aws"  # Marca de familia
        )

    def _crear_storage_aws(self, region: str) -> StorageDisk:
        """
        Crea Storage específico de AWS (EBS Volume)

        Características AWS:
        - ID con formato vol-xxxxxxxxxxxx
        - Tipos: gp2, gp3, io1, io2
        - provider = 'aws'

        Args:
            region: Región de AWS

        Returns:
            StorageDisk: EBS Volume de AWS
        """
        return StorageDisk(
            diskId=f"vol-{uuid.uuid4().hex[:12]}",  # Formato AWS
            name=f"aws-disk-{region}",
            size_gb=self.config.get('sizeGB', 20),
            disk_type=self.config.get('volumeType', 'gp2'),
            provider="aws"  # Marca de familia
        )

    def _crear_vm_aws(self, network: Network, storage: StorageDisk, region: str) -> MachineVirtual:
        """
        Crea VM específica de AWS (EC2 Instance)

        Características AWS:
        - ID con formato aws-uuid
        - Instance types: t2.micro, m5.large, etc.
        - provider = 'aws'
        - Asociada a Network y Storage de la misma familia

        Args:
            network: VPC de AWS (misma familia)
            storage: EBS de AWS (misma familia)
            region: Región de AWS

        Returns:
            MachineVirtual: EC2 Instance de AWS
        """
        vm_id = f"aws-{uuid.uuid4()}"

        return MachineVirtual(
            vmId=vm_id,
            name=f"aws-{self.config.get('type', 't2.micro')}-{region}-{vm_id[:4]}",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="aws",  # Marca de familia
            network=network,  # Network de la misma familia
            disks=[storage]  # Storage de la misma familia
        )
```

**Garantía de Coherencia:**

```python
# Todos los productos de la familia tienen:
network.provider == "aws"
storage.provider == "aws"
vm.provider == "aws"

# Y están en la misma región:
network.name.includes(region)
storage.name.includes(region)
vm.name.includes(region)

# Nomenclatura consistente:
network.networkId.startswith("vpc-")
storage.diskId.startswith("vol-")
vm.vmId.startswith("aws-")
```

#### Concrete Factory (Azure)

```python
# infrastructure/providers/azure.py

class Azure(ProveedorAbstracto):
    """
    Concrete Factory: Crea familia de productos Azure

    Familia Azure:
    - VNet (Network de Azure)
    - Managed Disk (Storage de Azure)
    - Azure VM (VM de Azure)
    """

    def crear_vm(self) -> MachineVirtual:
        """Coordina creación de familia Azure"""
        resource_group = self.config.get('resource_group', 'default-rg')

        # Familia completa de Azure
        network = self._crear_network_azure(resource_group)
        storage = self._crear_storage_azure(resource_group)
        vm = self._crear_vm_azure(network, storage, resource_group)

        return vm

    def _crear_network_azure(self, rg: str) -> Network:
        """
        Crea Network de Azure (VNet)

        Características Azure:
        - ID con formato vnet-xxx
        - Resource group asociado
        - provider = 'azure'
        """
        return Network(
            networkId=f"vnet-{rg}",  # Formato Azure
            name=f"azure-net-{rg}",
            cidr_block="10.1.0.0/16",  # CIDR típico de Azure
            provider="azure"  # Marca de familia
        )

    def _crear_storage_azure(self, rg: str) -> StorageDisk:
        """
        Crea Storage de Azure (Managed Disk)

        Características Azure:
        - ID con formato disk-xxx
        - SKUs: Standard_LRS, Premium_LRS
        - provider = 'azure'
        """
        return StorageDisk(
            diskId=f"disk-{uuid.uuid4().hex[:8]}",  # Formato Azure
            name=f"azure-disk-{rg}",
            size_gb=self.config.get('sizeGB', 30),
            disk_type=self.config.get('diskSku', 'Standard_LRS'),
            provider="azure"  # Marca de familia
        )

    def _crear_vm_azure(self, network: Network, storage: StorageDisk, rg: str) -> MachineVirtual:
        """
        Crea VM de Azure

        Características Azure:
        - ID con formato azure-uuid
        - VM sizes: Standard_B1s, D4s_v3, etc.
        - provider = 'azure'
        """
        vm_id = f"azure-{uuid.uuid4()}"

        return MachineVirtual(
            vmId=vm_id,
            name=f"azure-{self.config.get('type', 'Standard_B1s')}-{vm_id[:4]}",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="azure",  # Marca de familia
            network=network,  # VNet de la misma familia
            disks=[storage]  # Managed Disk de la misma familia
        )
```

### 🎨 Diagrama UML - Abstract Factory

```
┌────────────────────────────────────────────────────────────────────┐
│                   <<interface>>                                     │
│                 ProveedorAbstracto                                  │
│               (Abstract Factory)                                    │
├────────────────────────────────────────────────────────────────────┤
│ + crear_vm(): MachineVirtual                                        │
│ # _crear_network(): Network                                         │
│ # _crear_storage(): StorageDisk                                     │
└───────────────────┬────────────────────────────────────────────────┘
                    │
                    │ implements
        ┌───────────┴───────────┬──────────────┬────────────┐
        │                       │              │            │
┌───────▼──────┐      ┌─────────▼────┐  ┌─────▼─────┐  ┌──▼─────────┐
│     AWS      │      │    Azure     │  │  Google   │  │ OnPremise  │
│(ConcreteFactory)    │(ConcreteFactory)│(ConcreteFactory)│(ConcreteFactory)
├──────────────┤      ├──────────────┤  ├───────────┤  ├────────────┤
│crear_vm()    │      │crear_vm()    │  │crear_vm() │  │crear_vm()  │
│_crear_network│      │_crear_network│  │_crear_net │  │_crear_net  │
│_crear_storage│      │_crear_storage│  │_crear_sto │  │_crear_sto  │
└──────┬───────┘      └──────┬───────┘  └─────┬─────┘  └──────┬─────┘
       │                     │                │                │
       │ creates family      │ creates family │ creates family │ creates family
       │                     │                │                │
   ┌───▼───────────────────────────────────────────────────────────────┐
   │                     FAMILIA DE PRODUCTOS                           │
   │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐│
   │  │ MachineVirtual   │  │    Network       │  │  StorageDisk     ││
   │  │(AbstractProduct) │  │(AbstractProduct) │  │(AbstractProduct) ││
   │  ├──────────────────┤  ├──────────────────┤  ├──────────────────┤│
   │  │+ provider: str   │  │+ provider: str   │  │+ provider: str   ││
   │  │+ network: Network│  │+ networkId: str  │  │+ diskId: str     ││
   │  │+ disks: List     │  │+ cidr: str       │  │+ size_gb: int    ││
   │  └──────────────────┘  └──────────────────┘  └──────────────────┘│
   └───────────────────────────────────────────────────────────────────┘

FAMILIAS CONCRETAS:

AWS Family:                 Azure Family:               Google Family:
┌────────────────┐         ┌────────────────┐         ┌────────────────┐
│ EC2 Instance   │         │   Azure VM     │         │Compute Instance│
│ provider='aws' │         │provider='azure'│         │provider='google│
├────────────────┤         ├────────────────┤         ├────────────────┤
│ VPC            │         │     VNet       │         │  VPC Network   │
│ provider='aws' │         │provider='azure'│         │provider='google│
├────────────────┤         ├────────────────┤         ├────────────────┤
│ EBS Volume     │         │ Managed Disk   │         │Persistent Disk │
│ provider='aws' │         │provider='azure'│         │provider='google│
└────────────────┘         └────────────────┘         └────────────────┘
```

### 🔄 Diagrama de Secuencia - Abstract Factory

```
Cliente          AWS              Network      StorageDisk   MachineVirtual
  │               │                  │              │               │
  │ 1. crear_vm() │                  │              │               │
  ├──────────────>│                  │              │               │
  │               │                  │              │               │
  │               │ 2. _crear_network_aws()         │               │
  │               ├─────────────────>│              │               │
  │               │                  │              │               │
  │               │ 3. new Network(provider='aws') │               │
  │               │<─────────────────┤              │               │
  │               │                  │              │               │
  │               │ 4. _crear_storage_aws()         │               │
  │               ├─────────────────────────────────>│               │
  │               │                  │              │               │
  │               │ 5. new StorageDisk(provider='aws')              │
  │               │<─────────────────────────────────┤               │
  │               │                  │              │               │
  │               │ 6. _crear_vm_aws(network, storage)              │
  │               ├─────────────────────────────────────────────────>│
  │               │                  │              │               │
  │               │ 7. new MachineVirtual(provider='aws', network, disk)
  │               │<─────────────────────────────────────────────────┤
  │               │                  │              │               │
  │ 8. return VM  │                  │              │               │
  │<──────────────┤                  │              │               │
  │               │                  │              │               │

  VERIFICACIÓN DE COHERENCIA:
  vm.provider == network.provider == storage.provider == 'aws' ✓
```

### 💡 Diferencia Clave: Factory Method vs Abstract Factory

| Aspecto | Factory Method | Abstract Factory |
|---------|---------------|------------------|
| **Propósito** | Crea UN producto | Crea FAMILIA de productos |
| **Enfoque** | Qué crear | Cómo crear familia relacionada |
| **Ejemplo** | Crear solo VM | Crear VM + Network + Storage |
| **Jerarquía** | 1 nivel (producto) | 2 niveles (familia y productos) |
| **Uso en Proyecto** | `VMProviderFactory.create_provider()` | `AWS.crear_vm()` crea familia |
| **Patrón Principal** | ✅ Explícito | ✅ Implícito (dentro de providers) |

### 📊 Coherencia de Familia - Validación

```python
def verificar_coherencia_familia(vm: MachineVirtual) -> bool:
    """
    Verifica que todos los recursos pertenezcan a la misma familia

    Args:
        vm: Máquina virtual con sus recursos

    Returns:
        bool: True si la familia es coherente

    Raises:
        ValueError: Si hay inconsistencia
    """
    provider = vm.provider

    # Verificar Network
    if vm.network.provider != provider:
        raise ValueError(
            f"Inconsistencia: VM es {provider} pero Network es {vm.network.provider}"
        )

    # Verificar Storage
    for disk in vm.disks:
        if disk.provider != provider:
            raise ValueError(
                f"Inconsistencia: VM es {provider} pero Disk es {disk.provider}"
            )

    return True

# Uso
vm = aws_provider.crear_vm()
verificar_coherencia_familia(vm)  # ✅ Pasa: todos son 'aws'
```

### ✅ Beneficios del Abstract Factory

| Beneficio | Descripción | Ejemplo |
|-----------|-------------|---------|
| **Coherencia** | Garantiza que productos sean compatibles | VPC + EBS + EC2 todos de AWS |
| **Encapsulación** | Oculta detalles de creación | Cliente no sabe cómo se crea VPC |
| **Intercambiabilidad** | Cambiar familia completa fácilmente | Cambiar de AWS a Azure en un lugar |
| **SRP** | Cada factory crea su familia | AWS crea recursos AWS, Azure recursos Azure |

---

## 3. BUILDER PATTERN

### 📖 Definición Formal

> **Builder** es un patrón de diseño creacional que permite construir objetos complejos paso a paso. El patrón permite producir distintos tipos y representaciones de un objeto usando el mismo código de construcción.

### 🎯 Problema que Resuelve

**Escenario:**
Necesitas crear objetos con muchas configuraciones opcionales:
- VM con CPU, RAM, Disk, Network, Location, Advanced Options
- No todos los parámetros son necesarios
- Diferentes combinaciones para diferentes casos de uso

**Sin Builder (Constructor Telescópico):**
```python
# ❌ Constructor telescópico (antipatrón)
class MachineVirtual:
    def __init__(self, name, cpu, ram, disk, network, location,
                 monitoring=False, optimized=False,
                 security_group=None, key_pair=None,
                 disk_type=None, network_id=None, cidr=None,
                 # ... más parámetros
                 ):
        # Constructor gigante e inmanejable

# Uso confuso
vm = MachineVirtual("test", 4, 16, 100, None, "us-east-1",
                    True, False, None, "key1", "ssd", "vpc-123", "10.0.0.0/16")
# ¿Qué es cada parámetro? Ilegible
```

**Con Builder:**
```python
# ✅ Construcción legible paso a paso
vm = (builder
      .reset()
      .set_basic_config("test", "high-performance")
      .set_compute_resources(cpu=4, ram=16)
      .set_storage(size_gb=100, disk_type="ssd")
      .set_network(network_id="vpc-123", cidr="10.0.0.0/16")
      .set_location("us-east-1")
      .set_advanced_options({"monitoring": True, "optimized": False})
      .build())
# Legible, flexible, mantenible
```

### 🏗️ Estructura del Patrón

Ver SUSTENTACION_COMPLETA.md sección 4.2 para detalles completos.

### 🎨 Diagrama UML - Builder Pattern

```
┌────────────────────────────────────────────────────────────────────┐
│                         <<abstract>>                                │
│                          VMBuilder                                  │
├────────────────────────────────────────────────────────────────────┤
│ # _config: Dict[str, Any]                                           │
│ # _vm: Optional[MachineVirtual]                                     │
│ # _network: Optional[Network]                                       │
│ # _disk: Optional[StorageDisk]                                      │
├────────────────────────────────────────────────────────────────────┤
│ + reset(): VMBuilder                                                │
│ + set_basic_config(name, type): VMBuilder                           │
│ + set_compute_resources(cpu, ram): VMBuilder                        │
│ + set_storage(size, type): VMBuilder                                │
│ + set_network(id, cidr): VMBuilder                                  │
│ + set_location(location): VMBuilder                                 │
│ + set_advanced_options(options): VMBuilder                          │
│ + build(): MachineVirtual                                           │
│ + get_config(): Dict                                                │
└──────────────────┬─────────────────────────────────────────────────┘
                   │
                   │ extends
        ┌──────────┴──────────┬──────────────┬────────────┐
        │                     │              │            │
┌───────▼───────┐    ┌────────▼──────┐ ┌────▼──────┐ ┌──▼─────────┐
│ AWSVMBuilder  │    │AzureVMBuilder │ │GoogleVMBld│ │OnPremVMBld │
├───────────────┤    ├───────────────┤ ├───────────┤ ├────────────┤
│+ reset()      │    │+ reset()      │ │+ reset()  │ │+ reset()   │
│+ set_basic..  │    │+ set_basic..  │ │+ set_basic│ │+ set_basic │
│+ set_compute  │    │+ set_compute  │ │+ set_comp │ │+ set_comp  │
│+ set_storage  │    │+ set_storage  │ │+ set_stor │ │+ set_stor  │
│+ set_network  │    │+ set_network  │ │+ set_netw │ │+ set_netw  │
│+ set_location │    │+ set_location │ │+ set_loc  │ │+ set_loc   │
│+ set_advanced │    │+ set_advanced │ │+ set_adv  │ │+ set_adv   │
│+ build()      │    │+ build()      │ │+ build()  │ │+ build()   │
└───────┬───────┘    └───────┬───────┘ └────┬──────┘ └──────┬─────┘
        │                    │               │               │
        │ builds             │ builds        │ builds        │ builds
        └────────────────────┴───────────────┴───────────────┘
                             │
                             ▼
                  ┌──────────────────┐
                  │ MachineVirtual   │
                  │   + Network      │
                  │   + StorageDisk  │
                  └──────────────────┘

┌────────────────────────────────────────────────────────────────────┐
│                          VMDirector                                 │
│                        (Optional)                                   │
├────────────────────────────────────────────────────────────────────┤
│ - _builder: VMBuilder                                               │
├────────────────────────────────────────────────────────────────────┤
│ + __init__(builder: VMBuilder)                                      │
│ + change_builder(builder: VMBuilder)                                │
│ + build_minimal_vm(name): MachineVirtual                            │
│ + build_standard_vm(name, location): MachineVirtual                 │
│ + build_high_performance_vm(name, location): MachineVirtual         │
│ + build_custom_vm(name, cpu, ram, disk, location): MachineVirtual  │
└────────────────────────────────────────────────────────────────────┘
            │
            │ uses
            ▼
   ┌────────────────┐
   │   VMBuilder    │
   └────────────────┘
```

### 🔄 Diagrama de Secuencia - Builder with Director

```
Cliente       VMDirector      AWSVMBuilder          MachineVirtual
  │                │                │                      │
  │ 1. new Director(builder)        │                      │
  ├───────────────>│                │                      │
  │                │                │                      │
  │ 2. build_high_performance_vm("db", "us-east-1")       │
  ├───────────────>│                │                      │
  │                │                │                      │
  │                │ 3. reset()     │                      │
  │                ├───────────────>│                      │
  │                │                │                      │
  │                │ 4. set_basic_config("db", "high-perf")│
  │                ├───────────────>│                      │
  │                │                │                      │
  │                │ 5. set_location("us-east-1")          │
  │                ├───────────────>│                      │
  │                │                │                      │
  │                │ 6. set_compute_resources(8, 32)       │
  │                ├───────────────>│                      │
  │                │                │                      │
  │                │ 7. set_storage(500, "ssd")            │
  │                ├───────────────>│                      │
  │                │                │                      │
  │                │ 8. set_network()                      │
  │                ├───────────────>│                      │
  │                │                │                      │
  │                │ 9. set_advanced_options({...})        │
  │                ├───────────────>│                      │
  │                │                │                      │
  │                │ 10. build()    │                      │
  │                ├───────────────>│                      │
  │                │                │                      │
  │                │                │ 11. new MachineVirtual()
  │                │                ├─────────────────────>│
  │                │                │                      │
  │                │                │ 12. return VM        │
  │                │                │<─────────────────────┤
  │                │                │                      │
  │                │ 13. return VM  │                      │
  │                │<───────────────┤                      │
  │                │                │                      │
  │ 14. return VM  │                │                      │
  │<───────────────┤                │                      │
  │                │                │                      │
```

---

## 4. DIRECTOR PATTERN

### 📖 Definición

> **Director** es una extensión del Builder que encapsula el algoritmo de construcción. Define el orden de los pasos de construcción y qué valores usar para crear configuraciones predefinidas.

### 💻 Implementación Detallada

Ver SUSTENTACION_COMPLETA.md sección 4.3 para código completo.

### 🎨 Diagrama de Colaboración - Director

```
┌─────────────────────────────────────────────────────────────┐
│                    ESCENARIO: build_high_performance_vm     │
└─────────────────────────────────────────────────────────────┘

   [Cliente]                [VMDirector]              [AWSVMBuilder]
       │                          │                          │
       │                          │                          │
       │  1: build_high_performance_vm("analytics", "us-east-1")
       ├─────────────────────────>│                          │
       │                          │                          │
       │                          │  2: reset()              │
       │                          ├─────────────────────────>│
       │                          │                          │
       │                          │  3: set_basic_config(    │
       │                          │     "analytics",         │
       │                          │     "high-performance")  │
       │                          ├─────────────────────────>│
       │                          │                          │
       │                          │  4: set_location(        │
       │                          │     "us-east-1")         │
       │                          ├─────────────────────────>│
       │                          │                          │
       │                          │  5: set_compute_resources(
       │                          │     cpu=8, ram=32)       │
       │                          ├─────────────────────────>│
       │                          │                          │
       │                          │  6: set_storage(         │
       │                          │     500, "ssd")          │
       │                          ├─────────────────────────>│
       │                          │                          │
       │                          │  7: set_network()        │
       │                          ├─────────────────────────>│
       │                          │                          │
       │                          │  8: set_advanced_options(│
       │                          │     {"optimized": True,  │
       │                          │      "monitoring": True})│
       │                          ├─────────────────────────>│
       │                          │                          │
       │                          │  9: build()              │
       │                          ├─────────────────────────>│
       │                          │                          │
       │                          │  10: return VM           │
       │                          │<─────────────────────────┤
       │                          │                          │
       │  11: return VM           │                          │
       │<─────────────────────────┤                          │
       │                          │                          │
```

---

## 5. DIAGRAMAS UML DE CLASES

### 5.1 Diagrama UML Completo del Sistema

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                            CAPA DE DOMINIO (DOMAIN)                              │
│                                                                                   │
│  ┌───────────────────────┐         ┌────────────────────────────────────────┐   │
│  │  <<interface>>        │         │        <<abstract>>                    │   │
│  │ ProveedorAbstracto    │         │         VMBuilder                      │   │
│  ├───────────────────────┤         ├────────────────────────────────────────┤   │
│  │+ crear_vm()           │         │+ reset()                               │   │
│  │+ provisionar()        │         │+ set_basic_config()                    │   │
│  │+ estado()             │         │+ set_compute_resources()               │   │
│  └───────────────────────┘         │+ set_storage()                         │   │
│                                    │+ set_network()                         │   │
│  ┌───────────────────────┐         │+ set_location()                        │   │
│  │   VMDirector          │         │+ set_advanced_options()                │   │
│  ├───────────────────────┤         │+ build()                               │   │
│  │- _builder: VMBuilder  │───────> └────────────────────────────────────────┘   │
│  ├───────────────────────┤                                                       │
│  │+ build_minimal_vm()   │         ┌────────────────────────────────────────┐   │
│  │+ build_standard_vm()  │         │           Entities                     │   │
│  │+ build_high_perf_vm() │         ├────────────────────────────────────────┤   │
│  └───────────────────────┘         │ MachineVirtual                         │   │
│                                    │ Network                                │   │
│                                    │ StorageDisk                            │   │
│                                    │ VMStatus                               │   │
│                                    │ ProvisioningResult                     │   │
│                                    └────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────┐
│                        CAPA DE APLICACIÓN (APPLICATION)                          │
│                                                                                   │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                        VMProviderFactory                                   │  │
│  ├───────────────────────────────────────────────────────────────────────────┤  │
│  │- _providers: Dict[str, Type[ProveedorAbstracto]]                          │  │
│  ├───────────────────────────────────────────────────────────────────────────┤  │
│  │+ create_provider(type, config): ProveedorAbstracto                        │  │
│  │+ register_provider(name, class)                                           │  │
│  │+ get_available_providers(): List[str]                                     │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                         │                                         │
│                                         │ uses                                    │
│                                         ▼                                         │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                     VMProvisioningService                                  │  │
│  ├───────────────────────────────────────────────────────────────────────────┤  │
│  │- orchestrator: ProviderOrchestrator                                       │  │
│  ├───────────────────────────────────────────────────────────────────────────┤  │
│  │+ provision_vm(provider, config): ProvisioningResult                       │  │
│  │+ get_supported_providers(): List[str]                                     │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                                                                   │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                        VMBuilderFactory                                    │  │
│  ├───────────────────────────────────────────────────────────────────────────┤  │
│  │- _builders: Dict[str, Type[VMBuilder]]                                    │  │
│  ├───────────────────────────────────────────────────────────────────────────┤  │
│  │+ create_builder(type): VMBuilder                                          │  │
│  │+ get_available_builders(): List[str]                                      │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                                         │                                         │
│                                         │ uses                                    │
│                                         ▼                                         │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                      VMBuildingService                                     │  │
│  ├───────────────────────────────────────────────────────────────────────────┤  │
│  │- builder_factory: VMBuilderFactory                                        │  │
│  ├───────────────────────────────────────────────────────────────────────────┤  │
│  │+ build_vm_with_config(provider, config): ProvisioningResult               │  │
│  │+ build_predefined_vm(provider, preset, name, location): ProvisioningResult│  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────┐
│                     CAPA DE INFRAESTRUCTURA (INFRASTRUCTURE)                     │
│                                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐        │
│  │                           PROVIDERS                                  │        │
│  │  ┌──────────┐  ┌───────────┐  ┌────────────┐  ┌───────────────┐    │        │
│  │  │   AWS    │  │  Azure    │  │   Google   │  │  OnPremise    │    │        │
│  │  │          │  │           │  │            │  │               │    │        │
│  │  │implements│  │implements │  │implements  │  │ implements    │    │        │
│  │  │Proveedor │  │Proveedor  │  │Proveedor   │  │ Proveedor     │    │        │
│  │  │Abstracto │  │Abstracto  │  │Abstracto   │  │ Abstracto     │    │        │
│  │  └──────────┘  └───────────┘  └────────────┘  └───────────────┘    │        │
│  └─────────────────────────────────────────────────────────────────────┘        │
│                                                                                   │
│  ┌─────────────────────────────────────────────────────────────────────┐        │
│  │                            BUILDERS                                  │        │
│  │  ┌────────────┐  ┌──────────────┐  ┌──────────────┐  ┌────────────┐│        │
│  │  │AWSVMBuilder│  │AzureVMBuilder│  │GoogleVMBuilder│  │OnPremVMBld││        │
│  │  │            │  │              │  │              │  │            ││        │
│  │  │  extends   │  │   extends    │  │   extends    │  │  extends   ││        │
│  │  │ VMBuilder  │  │  VMBuilder   │  │  VMBuilder   │  │ VMBuilder  ││        │
│  │  └────────────┘  └──────────────┘  └──────────────┘  └────────────┘│        │
│  └─────────────────────────────────────────────────────────────────────┘        │
└──────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────────────┐
│                             CAPA DE API (API)                                     │
│                                                                                   │
│  ┌───────────────────────────────────────────────────────────────────────────┐  │
│  │                            Flask Application                               │  │
│  ├───────────────────────────────────────────────────────────────────────────┤  │
│  │ Endpoints:                                                                 │  │
│  │  + GET  /health                                                            │  │
│  │  + GET  /api/providers                                                     │  │
│  │  + POST /api/vm/provision                                                  │  │
│  │  + POST /api/vm/provision/<provider>                                       │  │
│  │  + POST /api/vm/build                                                      │  │
│  │  + POST /api/vm/build/preset                                               │  │
│  └───────────────────────────────────────────────────────────────────────────┘  │
│                │                                      │                           │
│                │ uses                                 │ uses                      │
│                ▼                                      ▼                           │
│   VMProvisioningService                   VMBuildingService                      │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. DIAGRAMAS DE SECUENCIA

### 6.1 Secuencia Completa - Factory Pattern

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                 FLUJO COMPLETO: Factory Pattern                                 │
│              POST /api/vm/provision {"provider":"aws","config":{...}}          │
└────────────────────────────────────────────────────────────────────────────────┘

Usuario  API/Flask  VMProvisioningService  VMProviderFactory  AWS  MachineVirtual
  │         │                │                     │           │         │
  │ POST    │                │                     │           │         │
  ├────────>│                │                     │           │         │
  │         │                │                     │           │         │
  │         │ provision_vm("aws", config)          │           │         │
  │         ├───────────────>│                     │           │         │
  │         │                │                     │           │         │
  │         │                │ create_provider("aws", config)  │         │
  │         │                ├────────────────────>│           │         │
  │         │                │                     │           │         │
  │         │                │                     │ new AWS(config)     │
  │         │                │                     ├──────────>│         │
  │         │                │                     │           │         │
  │         │                │    return AWS (as ProveedorAbstracto)     │
  │         │                │<────────────────────┤           │         │
  │         │                │                     │           │         │
  │         │                │ provisionar()       │           │         │
  │         │                ├─────────────────────────────────>│         │
  │         │                │                     │           │         │
  │         │                │                     │  crear_vm()         │
  │         │                │                     │           │         │
  │         │                │                     │  new MachineVirtual()
  │         │                │                     │           ├────────>│
  │         │                │                     │           │         │
  │         │                │                     │  return VM│         │
  │         │                │                     │           │<────────┤
  │         │                │                     │           │         │
  │         │                │ return VM           │           │         │
  │         │                │<─────────────────────────────────┤         │
  │         │                │                     │           │         │
  │         │ return ProvisioningResult(vm)        │           │         │
  │         │<───────────────┤                     │           │         │
  │         │                │                     │           │         │
  │ JSON    │                │                     │           │         │
  │ Response│                │                     │           │         │
  │<────────┤                │                     │           │         │
  │         │                │                     │           │         │
```

### 6.2 Secuencia Completa - Builder Pattern

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                 FLUJO COMPLETO: Builder Pattern                                 │
│         POST /api/vm/build {"provider":"azure","build_config":{...}}           │
└────────────────────────────────────────────────────────────────────────────────┘

Usuario  API/Flask  VMBuildingService  VMBuilderFactory  AzureVMBuilder  MachineVirtual
  │         │              │                  │                 │               │
  │ POST    │              │                  │                 │               │
  ├────────>│              │                  │                 │               │
  │         │              │                  │                 │               │
  │         │ build_vm_with_config("azure", config)             │               │
  │         ├─────────────>│                  │                 │               │
  │         │              │                  │                 │               │
  │         │              │ create_builder("azure")            │               │
  │         │              ├─────────────────>│                 │               │
  │         │              │                  │                 │               │
  │         │              │                  │ new AzureVMBuilder()            │
  │         │              │                  ├────────────────>│               │
  │         │              │                  │                 │               │
  │         │              │ return AzureVMBuilder (as VMBuilder)               │
  │         │              │<─────────────────┤                 │               │
  │         │              │                  │                 │               │
  │         │              │                  │ reset()         │               │
  │         │              ├──────────────────────────────────>│               │
  │         │              │                  │                 │               │
  │         │              │     set_basic_config("name", "type")               │
  │         │              ├──────────────────────────────────>│               │
  │         │              │                  │                 │               │
  │         │              │     set_compute_resources(8, 32)   │               │
  │         │              ├──────────────────────────────────>│               │
  │         │              │                  │                 │               │
  │         │              │     set_storage(500, "ssd")        │               │
  │         │              ├──────────────────────────────────>│               │
  │         │              │                  │                 │               │
  │         │              │     set_location("eastus")         │               │
  │         │              ├──────────────────────────────────>│               │
  │         │              │                  │                 │               │
  │         │              │     build()      │                 │               │
  │         │              ├──────────────────────────────────>│               │
  │         │              │                  │                 │               │
  │         │              │                  │  new MachineVirtual()           │
  │         │              │                  │                 ├──────────────>│
  │         │              │                  │                 │               │
  │         │              │                  │  return VM      │               │
  │         │              │                  │                 │<──────────────┤
  │         │              │                  │                 │               │
  │         │              │ return VM        │                 │               │
  │         │              │<──────────────────────────────────┤               │
  │         │              │                  │                 │               │
  │         │ return ProvisioningResult(vm)   │                 │               │
  │         │<─────────────┤                  │                 │               │
  │         │              │                  │                 │               │
  │ JSON    │              │                  │                 │               │
  │ Response│              │                  │                 │               │
  │<────────┤              │                  │                 │               │
  │         │              │                  │                 │               │
```

### 6.3 Secuencia Completa - Director Pattern

```
┌────────────────────────────────────────────────────────────────────────────────┐
│                 FLUJO COMPLETO: Director Pattern                                │
│    POST /api/vm/build/preset {"provider":"google","preset":"high-performance"}│
└────────────────────────────────────────────────────────────────────────────────┘

Usuario  API  VMBuildingService  VMBuilderFactory  VMDirector  GoogleVMBuilder  MachineVirtual
  │       │          │                  │              │             │                │
  │ POST  │          │                  │              │             │                │
  ├──────>│          │                  │              │             │                │
  │       │          │                  │              │             │                │
  │       │ build_predefined_vm("google", "high-performance", "db", "us-central1-a") │
  │       ├─────────>│                  │              │             │                │
  │       │          │                  │              │             │                │
  │       │          │ create_builder("google")        │             │                │
  │       │          ├─────────────────>│              │             │                │
  │       │          │                  │              │             │                │
  │       │          │                  │ new GoogleVMBuilder()      │                │
  │       │          │                  ├─────────────────────────>│                │
  │       │          │                  │              │             │                │
  │       │          │ return GoogleVMBuilder          │             │                │
  │       │          │<─────────────────┤              │             │                │
  │       │          │                  │              │             │                │
  │       │          │ new VMDirector(builder)         │             │                │
  │       │          ├──────────────────────────────>│             │                │
  │       │          │                  │              │             │                │
  │       │          │                  │              │             │                │
  │       │          │ build_high_performance_vm("db", "us-central1-a")              │
  │       │          ├──────────────────────────────>│             │                │
  │       │          │                  │              │             │                │
  │       │          │                  │              │ reset()     │                │
  │       │          │                  │              ├────────────>│                │
  │       │          │                  │              │             │                │
  │       │          │                  │              │ set_basic_config("db", "hp")│
  │       │          │                  │              ├────────────>│                │
  │       │          │                  │              │             │                │
  │       │          │                  │              │ set_location("us-central1-a")│
  │       │          │                  │              ├────────────>│                │
  │       │          │                  │              │             │                │
  │       │          │                  │              │ set_compute_resources(8, 32)│
  │       │          │                  │              ├────────────>│                │
  │       │          │                  │              │             │                │
  │       │          │                  │              │ set_storage(500, "ssd")      │
  │       │          │                  │              ├────────────>│                │
  │       │          │                  │              │             │                │
  │       │          │                  │              │ set_network()│                │
  │       │          │                  │              ├────────────>│                │
  │       │          │                  │              │             │                │
  │       │          │                  │              │ set_advanced_options({...})  │
  │       │          │                  │              ├────────────>│                │
  │       │          │                  │              │             │                │
  │       │          │                  │              │ build()     │                │
  │       │          │                  │              ├────────────>│                │
  │       │          │                  │              │             │                │
  │       │          │                  │              │     new MachineVirtual()     │
  │       │          │                  │              │             ├───────────────>│
  │       │          │                  │              │             │                │
  │       │          │                  │              │     return VM│                │
  │       │          │                  │              │             │<───────────────┤
  │       │          │                  │              │             │                │
  │       │          │                  │              │ return VM   │                │
  │       │          │                  │              │<────────────┤                │
  │       │          │                  │              │             │                │
  │       │          │ return VM        │              │             │                │
  │       │          │<──────────────────────────────┤             │                │
  │       │          │                  │              │             │                │
  │       │ return ProvisioningResult   │              │             │                │
  │       │<─────────┤                  │              │             │                │
  │       │          │                  │              │             │                │
  │ JSON  │          │                  │              │             │                │
  │<──────┤          │                  │              │             │                │
  │       │          │                  │              │             │                │
```

---

## 7. DIAGRAMAS DE COLABORACIÓN

### 7.1 Colaboración entre Patrones

```
┌──────────────────────────────────────────────────────────────────────┐
│          COLABORACIÓN: Factory Method + Builder + Director           │
└──────────────────────────────────────────────────────────────────────┘

┌─────────────┐
│   Cliente   │
└──────┬──────┘
       │
       │ 1: Solicita VM personalizada
       │
       ▼
┌─────────────────────┐
│  VMBuildingService  │
└──────┬──────────────┘
       │
       │ 2: Crea Builder específico
       │
       ▼
┌─────────────────────┐         ┌──────────────┐
│ VMBuilderFactory    │────────>│  VMBuilder   │ (Abstract)
└──────┬──────────────┘         └──────┬───────┘
       │                               │
       │ 3: Retorna Builder            │ implements
       │                               │
       ▼                               ▼
┌─────────────────────┐         ┌──────────────────┐
│ AWSVMBuilder        │<────────│  VMDirector      │
└──────┬──────────────┘         └──────┬───────────┘
       │                               │
       │ 4: Director usa Builder       │
       │    para construir VM          │
       │                               │
       │ 5: Builder crea familia       │
       │    de recursos                │
       │                               │
       ▼                               │
┌─────────────────────┐               │
│ MachineVirtual      │               │
│   + Network         │               │
│   + StorageDisk     │               │
└──────┬──────────────┘               │
       │                               │
       │ 6: Retorna VM completa        │
       │<──────────────────────────────┘
       │
       ▼
┌─────────────────────┐
│  Cliente            │
└─────────────────────┘
```

---

## 8. COMPARACIÓN DE PATRONES

### 8.1 Tabla Comparativa

| Aspecto | Factory Method | Abstract Factory | Builder | Director |
|---------|---------------|------------------|---------|----------|
| **Objetivo** | Crear objetos sin especificar clase exacta | Crear familias de objetos relacionados | Construir objetos complejos paso a paso | Encapsular algoritmo de construcción |
| **Nivel** | Crea 1 producto | Crea familia de productos | Crea 1 producto complejo | Usa Builder para presets |
| **Complejidad** | Baja | Media | Media-Alta | Baja (usa Builder) |
| **Flexibilidad** | Alta (polimorfismo) | Alta (familias coherentes) | Muy Alta (construcción incremental) | Media (presets fijos) |
| **Uso Principal** | Selección de tipo | Coherencia de familia | Configuración compleja | Simplificación para usuario |
| **En el Proyecto** | `VMProviderFactory` | `AWS.crear_vm()` (implícito) | `AWSVMBuilder` | `VMDirector` |
| **Cuándo Usar** | Múltiples tipos a crear | Recursos deben ser compatibles | Muchas opciones de configuración | Configuraciones comunes |

### 8.2 Decisión de Uso

```
┌─────────────────────────────────────────────────────────────────┐
│              ¿QUÉ PATRÓN USAR? - Árbol de Decisión              │
└─────────────────────────────────────────────────────────────────┘

                    ¿Qué necesitas crear?
                            │
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
    ¿1 objeto simple?   ¿Familia de    ¿1 objeto complejo
                        objetos?        con muchas opciones?
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐   ┌──────────────┐   ┌────────────────┐
│Factory Method │   │Abstract      │   │    Builder     │
│               │   │Factory       │   │                │
│Ejemplo:       │   │              │   │Ejemplo:        │
│create_provider│   │Ejemplo:      │   │AWSVMBuilder    │
│("aws")        │   │AWS.crear_vm()│   │  .set_x()      │
│               │   │crea VM+Net+  │   │  .set_y()      │
│               │   │Storage       │   │  .build()      │
└───────────────┘   └──────────────┘   └───────┬────────┘
                                               │
                                               │
                                    ¿Necesitas presets
                                     predefinidos?
                                               │
                                        ┌──────┴──────┐
                                        │ Sí          │ No
                                        ▼             ▼
                                ┌──────────────┐   Usa Builder
                                │   Director   │   directamente
                                │              │
                                │build_standard│
                                │build_high_perf
                                └──────────────┘
```

---

## 📚 CONCLUSIÓN

Este documento complementa **[SUSTENTACION_COMPLETA.md](SUSTENTACION_COMPLETA.md)** proporcionando:

✅ **Explicaciones detalladas** de Factory Method y Abstract Factory
✅ **Diagramas UML completos** de clases
✅ **Diagramas de secuencia** para todos los flujos
✅ **Diagramas de colaboración** mostrando interacciones
✅ **Comparaciones** entre patrones
✅ **Árboles de decisión** para elegir patrón apropiado

### 📖 Documentos del Proyecto

1. **[README.md](README.md)** - Documentación general y uso
2. **[SUSTENTACION_COMPLETA.md](SUSTENTACION_COMPLETA.md)** - Cumplimiento de requisitos, pruebas, sustentación
3. **[PATRONES_Y_UML.md](PATRONES_Y_UML.md)** - Este documento: Patrones y diagramas UML
4. **[IMPLEMENTACION_BUILDER.md](IMPLEMENTACION_BUILDER.md)** - Detalles de implementación
5. **[QUICKSTART.md](QUICKSTART.md)** - Guía rápida de inicio

---

**Creado por:** Sistema de Documentación Técnica
**Fecha:** 2025
**Universidad Popular del Cesar** - Especialización en Ingeniería de Software
