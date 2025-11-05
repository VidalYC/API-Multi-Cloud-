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

### Opción 1: Docker (Recomendado) 🐳

#### Requisitos
- Docker Desktop
- Docker Compose

#### Despliegue Rápido

```bash
# Clonar el repositorio
cd API-Proveedores

# Construir y ejecutar con Docker Compose
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

**URLs de acceso:**
- Frontend: http://localhost
- Backend API: http://localhost:5000
- Health Check: http://localhost:5000/health

#### Usando Imágenes de Docker Hub

Las imágenes están disponibles públicamente en Docker Hub:

```bash
# Descargar imágenes
docker pull yoriel/api-proveedores-backend:latest
docker pull yoriel/api-proveedores-frontend:latest

# Ejecutar backend
docker run -d -p 5000:5000 --name backend yoriel/api-proveedores-backend:latest

# Ejecutar frontend
docker run -d -p 80:80 --name frontend yoriel/api-proveedores-frontend:latest
```

**Repositorios Docker Hub:**
- Backend: https://hub.docker.com/r/yoriel/api-proveedores-backend
- Frontend: https://hub.docker.com/r/yoriel/api-proveedores-frontend

#### Arquitectura Docker

El proyecto incluye:
- **Backend Dockerfile**: Python 3.11-slim con Flask
- **Frontend Dockerfile**: Multi-stage build (Node.js + Nginx)
- **docker-compose.yml**: Orquestación de servicios
- **nginx.conf**: Proxy reverso para comunicación backend-frontend
- **Health checks**: Monitoreo automático de contenedores
- **Networking**: Red interna para comunicación entre servicios

### Opción 2: Instalación Local

#### Requisitos
- Python 3.8+
- pip
- Node.js 18+ (para frontend)

#### Backend

```bash
# Ir al directorio del backend
cd Backend

# Instalar dependencias
pip install -r requirements.txt

# O usar setup.py
pip install -e .

# Ejecutar servidor
python api/main.py
```

#### Frontend

```bash
# Ir al directorio del frontend
cd frontend

# Instalar dependencias
npm install

# Modo desarrollo
npm start

# Construir para producción
npm run build
```

## 📚 Uso de la API

### Iniciar el servidor

**Con Docker:**
```bash
docker-compose up -d
```

**Sin Docker:**
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

## 🐳 Información Detallada de Docker

### Estructura de Dockerización

```
API-Proveedores/
├── Backend/
│   ├── Dockerfile              # Imagen del backend Flask
│   └── .dockerignore          # Archivos excluidos del build
├── frontend/
│   ├── Dockerfile              # Multi-stage build React + Nginx
│   ├── nginx.conf             # Configuración proxy reverso
│   └── .dockerignore          # Archivos excluidos del build
└── docker-compose.yml          # Orquestación de servicios
```

### Características de las Imágenes

#### Backend (233MB)
- **Base**: `python:3.11-slim`
- **Puerto expuesto**: 5000
- **Características**:
  - Instalación automática de dependencias desde `requirements.txt`
  - Instalación del paquete local con `setup.py`
  - Health check en `/health`
  - Variables de entorno configurables
  - Reinicio automático (`restart: unless-stopped`)

#### Frontend (84.2MB)
- **Build Stage**: `node:18-alpine`
- **Production Stage**: `nginx:alpine`
- **Puerto expuesto**: 80
- **Características**:
  - Build optimizado de React
  - Compresión gzip habilitada
  - Cache de assets estáticos
  - Proxy reverso al backend
  - Soporte para SPA (Single Page Application)

### Docker Compose

El archivo `docker-compose.yml` orquesta ambos servicios:

```yaml
services:
  backend:
    - Puerto: 5000:5000
    - Health check activo
    - Red: api-network

  frontend:
    - Puerto: 80:80
    - Depende del backend
    - Nginx con proxy reverso
    - Red: api-network
```

**Red interna**: `api-network` permite comunicación entre servicios

### Comandos Útiles Docker

```bash
# Ver logs en tiempo real
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f backend
docker-compose logs -f frontend

# Reiniciar servicios
docker-compose restart

# Ver estado de contenedores
docker-compose ps

# Reconstruir imágenes
docker-compose build --no-cache

# Ejecutar comandos dentro del contenedor
docker-compose exec backend python -c "print('Hello')"

# Ver uso de recursos
docker stats

# Limpiar recursos
docker-compose down -v
docker system prune -a
```

### Variables de Entorno

**Backend:**
- `FLASK_APP`: api.main:app
- `FLASK_RUN_PORT`: 5000
- `PYTHONUNBUFFERED`: 1

**Frontend:**
- Configuradas en build time
- API_URL configurado en nginx.conf

### Troubleshooting Docker

**Problema: Contenedores no inician**
```bash
# Ver logs detallados
docker-compose logs

# Verificar estado
docker-compose ps
```

**Problema: Puerto en uso**
```bash
# Cambiar puertos en docker-compose.yml
ports:
  - "8080:5000"  # Backend en 8080
  - "8000:80"    # Frontend en 8000
```

**Problema: Imágenes desactualizadas**
```bash
# Reconstruir todo
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Despliegue en Producción

Para desplegar en producción usando las imágenes de Docker Hub:

```bash
# 1. Descargar imágenes
docker pull yoriel/api-proveedores-backend:1.0.0
docker pull yoriel/api-proveedores-frontend:latest

# 2. Ejecutar con docker-compose
docker-compose up -d

# 3. Verificar
curl http://localhost:5000/health
```

### CI/CD con Docker

Las imágenes pueden ser parte de un pipeline CI/CD:

```bash
# Build
docker-compose build

# Test
docker-compose run backend pytest

# Push a registry
docker push yoriel/api-proveedores-backend:latest
docker push yoriel/api-proveedores-frontend:latest
```

---

## 📄 Licencia

Este proyecto es de uso académico.
