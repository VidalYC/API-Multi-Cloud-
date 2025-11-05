# API Multi-Cloud VM Provisioning

Sistema de aprovisionamiento de máquinas virtuales multi-cloud implementando los patrones **Factory Method** y **Builder** con principios SOLID.

## 📋 Descripción

API REST que permite aprovisionar máquinas virtuales en diferentes proveedores cloud (AWS, Azure, Google Cloud, On-Premise) utilizando dos enfoques:

1. **Factory Pattern**: Para aprovisionamiento rápido con configuraciones estándar
2. **Builder Pattern**: Para construcción detallada y personalizada de VMs paso a paso

## 🏗️ Arquitectura

### Patrones de Diseño Implementados

- **Factory Method**: Creación de proveedores cloud de forma dinámica
- **Abstract Factory**: Creación de familias de recursos relacionados (VM, Network, Disk)
- **Builder**: Construcción compleja de VMs paso a paso
- **Director**: Encapsula algoritmos de construcción predefinidos

### Principios SOLID

- **SRP**: Cada clase tiene una única responsabilidad
- **OCP**: Abierto para extensión, cerrado para modificación
- **LSP**: Las subclases pueden sustituir a sus clases base
- **ISP**: Interfaces específicas para cada cliente
- **DIP**: Dependencia de abstracciones, no de implementaciones

### Estructura del Proyecto

```
API-Proveedores/
├── api/
│   └── main.py                    # REST API endpoints
├── application/
│   ├── factory.py                 # Factory & Builder services
│   └── schemas.py                 # Pydantic validation schemas
├── domain/
│   ├── builder.py                 # Builder abstract interface & Director
│   ├── entities.py                # Domain entities
│   └── interfaces.py              # Abstract interfaces
├── infrastructure/
│   ├── builders/                  # Concrete builders
│   │   ├── aws_builder.py
│   │   ├── azure_builder.py
│   │   ├── google_builder.py
│   │   └── onpremise_builder.py
│   └── providers/                 # Concrete providers
│       ├── aws.py
│       ├── azure.py
│       ├── google.py
│       └── onpremise.py
└── tests/
    ├── test_all.py                # Factory tests
    ├── test_api_endpoints.py      # API integration tests
    └── test_builder.py            # Builder tests
```

## 🚀 Instalación

### Requisitos

- Python 3.8+
- pip

### Pasos

```bash
# Clonar el repositorio
cd API-Proveedores

# Instalar dependencias
pip install -r requirements.txt

# O usar setup.py
pip install -e .
```

## 📚 Uso de la API

### Iniciar el servidor

```bash
python api/main.py
```

El servidor se iniciará en `http://localhost:5000`

---

## 🔧 Endpoints Disponibles

### 1. Health Check

```http
GET /health
```

**Respuesta:**
```json
{
  "status": "healthy",
  "service": "VM Provisioning API",
  "version": "1.0.0"
}
```

---

### 2. Listar Proveedores

```http
GET /api/providers
```

**Respuesta:**
```json
{
  "success": true,
  "providers": ["aws", "azure", "google", "gcp", "onpremise", "on-premise"],
  "count": 6
}
```

---

### 3. Provisionar VM (Factory Pattern)

Aprovisionamiento rápido con configuraciones estándar.

```http
POST /api/vm/provision
Content-Type: application/json
```

**Request Body:**
```json
{
  "provider": "aws",
  "config": {
    "type": "t2.micro",
    "region": "us-east-1",
    "sizeGB": 20,
    "volumeType": "gp2"
  }
}
```

**Respuesta:**
```json
{
  "success": true,
  "vm_id": "aws-a1b2c3d4-...",
  "message": "VM creada exitosamente en aws",
  "provider": "aws",
  "vm_details": {
    "vmId": "aws-a1b2c3d4-...",
    "name": "aws-t2.micro-us-east-1-a1b2",
    "status": "running",
    "createdAt": "2025-01-07T...",
    "provider": "aws",
    "network": {
      "networkId": "vpc-12345678",
      "name": "aws-net-us-east-1",
      "cidr_block": "10.0.0.0/16",
      "provider": "aws"
    },
    "disks": [...]
  }
}
```

---

### 4. Provisionar VM por URL (Factory Pattern)

```http
POST /api/vm/provision/azure
Content-Type: application/json
```

**Request Body:**
```json
{
  "config": {
    "type": "Standard_B1s",
    "resource_group": "production-rg",
    "sizeGB": 50
  }
}
```

---

### 5. Construir VM Personalizada (Builder Pattern) 🆕

Construcción detallada con control total sobre todos los parámetros.

```http
POST /api/vm/build
Content-Type: application/json
```

**Request Body:**
```json
{
  "provider": "aws",
  "build_config": {
    "name": "production-web-server",
    "vm_type": "standard",
    "cpu": 4,
    "ram": 16,
    "disk_gb": 200,
    "disk_type": "ssd",
    "location": "us-west-2",
    "network_id": "vpc-custom-123",
    "cidr": "10.5.0.0/16",
    "advanced_options": {
      "monitoring": true,
      "optimized": true,
      "security_group": "sg-web-servers"
    }
  }
}
```

**Respuesta:**
```json
{
  "success": true,
  "vm_id": "aws-...",
  "message": "VM construida exitosamente en aws usando Builder Pattern",
  "provider": "aws",
  "vm_details": {...}
}
```

---

### 6. Construir VM Predefinida (Director) 🆕

Uso del Director para crear VMs con configuraciones predefinidas.

```http
POST /api/vm/build/preset
Content-Type: application/json
```

**Request Body:**
```json
{
  "provider": "google",
  "preset": "high-performance",
  "name": "analytics-server",
  "location": "us-central1-a"
}
```

**Presets disponibles:**
- `minimal`: CPU: 1, RAM: 1GB, Disk: 10GB (desarrollo/testing)
- `standard`: CPU: 2, RAM: 4GB, Disk: 50GB (aplicaciones web)
- `high-performance`: CPU: 8, RAM: 32GB, Disk: 500GB (bases de datos, analytics)

**Respuesta:**
```json
{
  "success": true,
  "vm_id": "gcp-...",
  "message": "VM 'high-performance' construida exitosamente en google",
  "provider": "google",
  "vm_details": {...}
}
```

---

## 📖 Ejemplos de Uso

### Ejemplo 1: Provisionar VM Rápida en AWS (Factory)

```bash
curl -X POST http://localhost:5000/api/vm/provision \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "aws",
    "config": {
      "type": "t2.small",
      "region": "us-east-1"
    }
  }'
```

### Ejemplo 2: Construir VM Personalizada en Azure (Builder)

```bash
curl -X POST http://localhost:5000/api/vm/build \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "azure",
    "build_config": {
      "name": "database-server",
      "vm_type": "high-performance",
      "cpu": 8,
      "ram": 32,
      "disk_gb": 1000,
      "disk_type": "ssd",
      "location": "eastus",
      "advanced_options": {
        "monitoring": true,
        "resource_group": "production"
      }
    }
  }'
```

### Ejemplo 3: Crear VM Mínima para Testing (Director)

```bash
curl -X POST http://localhost:5000/api/vm/build/preset \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "onpremise",
    "preset": "minimal",
    "name": "test-vm",
    "location": "datacenter-1"
  }'
```

---

## 🎯 Diferencias entre Factory y Builder

### Factory Pattern (`/api/vm/provision`)
- ✅ Aprovisionamiento rápido
- ✅ Configuraciones estándar del proveedor
- ✅ Validación con Pydantic
- ✅ Valores por defecto automáticos
- ❌ Menos control sobre detalles

**Usar cuando:** Necesitas crear VMs rápidamente con configuraciones típicas del proveedor.

### Builder Pattern (`/api/vm/build`)
- ✅ Control total sobre la configuración
- ✅ Construcción paso a paso
- ✅ Configuraciones complejas y personalizadas
- ✅ Opciones avanzadas específicas
- ✅ Director con presets predefinidos

**Usar cuando:** Necesitas VMs altamente personalizadas o construcción incremental.

---

## 🔬 Testing

### Ejecutar todos los tests

```bash
# Tests del Factory Pattern
python tests/test_all.py

# Tests de endpoints API
python tests/test_api_endpoints.py

# Tests del Builder Pattern
python tests/test_builder.py
```

### Cobertura de Tests

- ✅ 80+ tests unitarios e integración
- ✅ Tests de endpoints API
- ✅ Validación de principios SOLID
- ✅ Tests de patrones de diseño (Factory + Builder)

---

## 🔐 Validación de Configuraciones

El sistema usa **Pydantic** para validar automáticamente las configuraciones:

### AWS Config
```python
{
  "type": "t2.micro",       # default: t2.micro
  "region": "us-east-1",    # default: us-east-1
  "sizeGB": 20,             # default: 20 (must be > 0)
  "volumeType": "gp2",      # default: gp2
  "vpcId": "vpc-xxx"        # optional
}
```

### Azure Config
```python
{
  "type": "Standard_B1s",   # default: Standard_B1s
  "resource_group": "rg",   # default: default-rg
  "sizeGB": 30,             # default: 30 (must be > 0)
  "diskSku": "Standard_LRS",# default: Standard_LRS
  "virtualNetwork": "vnet"  # optional
}
```

### Google Config
```python
{
  "type": "n1-standard-1",  # default: n1-standard-1
  "zone": "us-central1-a",  # default: us-central1-a
  "sizeGB": 10,             # default: 10 (must be > 0)
  "diskType": "pd-standard",# default: pd-standard
  "networkName": "net"      # optional
}
```

### OnPremise Config
```python
{
  "cpu": 2,                 # default: 2 (must be > 0)
  "ram": 4,                 # default: 4 (must be > 0)
  "disk": 50,               # default: 50 (must be > 0)
  "vlanId": 100,            # optional
  "storagePool": "pool",    # optional
  "raidLevel": 5            # optional
}
```

---

## 📊 Respuestas de Error

### Error de validación
```json
{
  "success": false,
  "message": "Error de validación de parámetros",
  "error_detail": "[{\"loc\": [\"sizeGB\"], \"msg\": \"ensure this value is greater than 0\"}]",
  "provider": "aws"
}
```

### Proveedor no soportado
```json
{
  "success": false,
  "message": "Proveedor 'invalid' no soportado",
  "error_detail": "Proveedores disponibles: aws, azure, google, onpremise",
  "provider": "invalid"
}
```

---

## 🛠️ Extensibilidad

### Agregar un nuevo proveedor

1. **Crear el proveedor concreto:**
```python
# infrastructure/providers/digitalocean.py
from domain.interfaces import ProveedorAbstracto

class DigitalOcean(ProveedorAbstracto):
    def crear_vm(self) -> MachineVirtual:
        # Implementación
        pass
```

2. **Crear el builder:**
```python
# infrastructure/builders/digitalocean_builder.py
from domain.builder import VMBuilder

class DigitalOceanVMBuilder(VMBuilder):
    # Implementación
    pass
```

3. **Registrar en los factories:**
```python
VMProviderFactory.register_provider('digitalocean', DigitalOcean)
```

---

## 📝 Notas Técnicas

### Requisitos Funcionales (RF)
- **RF1**: Aprovisionar VMs en múltiples clouds
- **RF2**: Invocar lógica según proveedor
- **RF3**: Devolver estado del aprovisionamiento
- **RF4**: Registrar logs sin información sensible
- **RF5**: Listar proveedores disponibles

### Requisitos No Funcionales (RNF)
- **RNF1**: Consistencia - VM no se crea sin Red y Disco
- **RNF3**: Logging seguro sin credenciales
- **RNF4**: API Stateless para escalabilidad
- **RNF5**: Comunicación vía JSON

---

## 👥 Autores

- Universidad Popular del Cesar
- Curso: Patrones de Diseño

---

## 📄 Licencia

Este proyecto es de uso académico.
