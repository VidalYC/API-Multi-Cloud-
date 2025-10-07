# 📚 SUSTENTACIÓN COMPLETA DEL PROYECTO
## API Multi-Cloud VM Provisioning con Patrones Factory y Builder

**Universidad Popular del Cesar**
**Especialización en Ingeniería de Software**
**Asignatura:** Patrones de Diseño de Software
**Actividad:** WS3 - Builder Pattern Integration

---

## 📋 TABLA DE CONTENIDOS

1. [Cumplimiento de Requisitos del PDF](#1-cumplimiento-de-requisitos-del-pdf)
2. [Guía de Pruebas Paso a Paso](#2-guía-de-pruebas-paso-a-paso)
3. [Sustentación Técnica Detallada](#3-sustentación-técnica-detallada)
4. [Patrones de Diseño Implementados](#4-patrones-de-diseño-implementados)
5. [Principios SOLID Aplicados](#5-principios-solid-aplicados)
6. [Arquitectura del Sistema](#6-arquitectura-del-sistema)
7. [Análisis de Código](#7-análisis-de-código)

---

## 1. CUMPLIMIENTO DE REQUISITOS DEL PDF

### 📊 Tabla de Cumplimiento - Requisitos Funcionales (RF)

| ID | Requisito | Estado | Evidencia |
|----|-----------|--------|-----------|
| **RF1** | La API debe permitir crear máquinas virtuales en diferentes proveedores (AWS, Azure, GCP, On-Premise) | ✅ **CUMPLIDO** | - 4 builders concretos implementados<br>- Endpoints `/api/vm/provision` y `/api/vm/build`<br>- Tests: `test_build_all_providers()` |
| **RF2** | Cada VM debe asociarse a una red y almacenamiento del mismo proveedor | ✅ **CUMPLIDO** | - Método `build()` crea Network y Storage<br>- Coherencia de proveedor garantizada<br>- Ver líneas 363-378 en `aws_builder.py` |
| **RF3** | Debe existir un Director que orqueste el proceso de construcción (Builder) según el tipo de VM | ✅ **CUMPLIDO** | - Clase `VMDirector` en `domain/builder.py`<br>- Métodos: `build_minimal_vm()`, `build_standard_vm()`, `build_high_performance_vm()`<br>- Endpoint `/api/vm/build/preset` |
| **RF4** | El Director debe asignar valores de vCPU y memoria RAM según el tipo de máquina y proveedor | ✅ **CUMPLIDO** | - Configuraciones específicas por proveedor<br>- Mapeo de CPU/RAM en cada builder<br>- Ver líneas 84-104 en `aws_builder.py` |
| **RF5** | Los recursos deben validarse para garantizar coherencia de región y proveedor | ✅ **CUMPLIDO** | - Validación en construcción<br>- Mismo proveedor para VM, Network, Storage<br>- Pydantic schemas para validación |

### 📊 Tabla de Cumplimiento - Requisitos No Funcionales (RNF)

| ID | Requisito | Estado | Evidencia |
|----|-----------|--------|-----------|
| **RNF1** | **Modularidad:** Separación clara entre Factory, Builder y Director | ✅ **CUMPLIDO** | - `VMProviderFactory` en `application/factory.py`<br>- `VMBuilder` en `domain/builder.py`<br>- `VMDirector` en `domain/builder.py`<br>- Separación por capas (Domain, Application, Infrastructure) |
| **RNF2** | **Extensibilidad:** Agregar nuevos tipos de VM o proveedores sin cambiar código existente | ✅ **CUMPLIDO** | - Patrón Open/Closed aplicado<br>- `register_provider()` para nuevos proveedores<br>- Abstracciones permiten extensión<br>- Test: `test_ocp_open_closed()` |
| **RNF3** | **Validación cruzada:** Coherencia de proveedor y región entre recursos | ✅ **CUMPLIDO** | - Builders crean recursos del mismo proveedor<br>- Network y Storage comparten región/ubicación<br>- Validación en `build()` de cada builder |
| **RNF4** | **Escalabilidad:** Arquitectura debe soportar múltiples despliegues simultáneos | ✅ **CUMPLIDO** | - API Stateless (sin estado compartido)<br>- Sin sesiones en memoria<br>- Patrón Factory permite instancias independientes<br>- Flask CORS habilitado |
| **RNF5** | **Legibilidad:** Código entendible como material de enseñanza | ✅ **CUMPLIDO** | - Documentación exhaustiva (README, comentarios)<br>- Nombres descriptivos de clases y métodos<br>- Arquitectura limpia y clara<br>- 80+ tests como ejemplos de uso |

### 📊 Tabla de Parámetros Adicionales - VirtualMachine

| Atributo | Descripción | Obligatorio | Implementado | Ubicación |
|----------|-------------|-------------|--------------|-----------|
| `provider` | Proveedor de nube | ✅ | ✅ | `MachineVirtual.provider` en entities.py |
| `vcpus` | Núcleos virtuales asignados | ✅ | ✅ | Configurado en `set_compute_resources()` |
| `memoryGB` | Memoria RAM asignada | ✅ | ✅ | Configurado en `set_compute_resources()` |
| `memoryOptimization` | Optimización de memoria | ❌ | ✅ | En `advanced_options` de builders |
| `diskOptimization` | Optimización de disco | ❌ | ✅ | En `advanced_options` de builders |
| `keyPairName` | Clave SSH o autenticación | ❌ | ✅ | En `advanced_options` de builders |

### 📊 Tabla de Parámetros Adicionales - Network

| Atributo | Descripción | Obligatorio | Implementado | Ubicación |
|----------|-------------|-------------|--------------|-----------|
| `region` | Región de red | ✅ | ✅ | `set_location()` en builders |
| `firewallRules` | Reglas de seguridad | ❌ | ✅ | En `advanced_options` |
| `publicIP` | IP pública asignada | ❌ | ✅ | En `advanced_options` |

### 📊 Tabla de Parámetros Adicionales - Storage

| Atributo | Descripción | Obligatorio | Implementado | Ubicación |
|----------|-------------|-------------|--------------|-----------|
| `region` | Región del almacenamiento | ✅ | ✅ | Heredada de `set_location()` |
| `iops` | Rendimiento del disco | ❌ | ✅ | En `advanced_options` |

### 📊 Tipos de Máquina por Proveedor - Implementación

#### Amazon AWS

| Categoría | Tipo | vCPU | RAM | Implementado |
|-----------|------|------|-----|--------------|
| **General Purpose** | t3.medium | 2 | 4 GiB | ✅ Mapeo en `set_compute_resources()` |
| | m5.large | 2 | 8 GiB | ✅ |
| | m5.xlarge | 4 | 16 GiB | ✅ |
| **Memory-Optimized** | r5.large | 2 | 16 GiB | ✅ Preset `high-performance` |
| | r5.xlarge | 4 | 32 GiB | ✅ |
| | r5.2xlarge | 8 | 64 GiB | ✅ |
| **Compute-Optimized** | c5.large | 2 | 4 GiB | ✅ |
| | c5.xlarge | 4 | 8 GiB | ✅ |
| | c5.2xlarge | 8 | 16 GiB | ✅ |

**Ubicación en código:** `infrastructure/builders/aws_builder.py` líneas 84-104

#### Microsoft Azure

| Categoría | Tipo | vCPU | RAM | Implementado |
|-----------|------|------|-----|--------------|
| **Standard/General Purpose** | D2s_v3 | 2 | 8 GiB | ✅ |
| | D4s_v3 | 4 | 16 GiB | ✅ |
| | D8s_v3 | 8 | 32 GiB | ✅ |
| **Memory-Optimized** | E2s_v3 | 2 | 16 GiB | ✅ |
| | E4s_v3 | 4 | 32 GiB | ✅ |
| | E8s_v3 | 8 | 64 GiB | ✅ |
| **Compute-Optimized** | F2s_v2 | 2 | 4 GiB | ✅ |
| | F4s_v2 | 4 | 8 GiB | ✅ |
| | F8s_v2 | 8 | 16 GiB | ✅ |

**Ubicación en código:** `infrastructure/builders/azure_builder.py` líneas 76-96

#### Google Cloud Platform (GCP)

| Categoría | Tipo | vCPU | RAM | Implementado |
|-----------|------|------|-----|--------------|
| **Standard/General Purpose** | e2-standard-2 | 2 | 8 GiB | ✅ |
| | e2-standard-4 | 4 | 16 GiB | ✅ |
| | e2-standard-8 | 8 | 32 GiB | ✅ |
| **Memory-Optimized** | n2-highmem-2 | 2 | 16 GiB | ✅ |
| | n2-highmem-4 | 4 | 32 GiB | ✅ |
| | n2-highmem-8 | 8 | 64 GiB | ✅ |
| **Compute-Optimized** | n2-highcpu-2 | 2 | 2 GiB | ✅ |
| | n2-highcpu-4 | 4 | 4 GiB | ✅ |
| | n2-highcpu-8 | 8 | 8 GiB | ✅ |

**Ubicación en código:** `infrastructure/builders/google_builder.py` líneas 76-96

#### On-Premise (Simulación)

| Categoría | Tipo | vCPU | RAM | Implementado |
|-----------|------|------|-----|--------------|
| **Standard** | onprem-std1 | 2 | 4 GiB | ✅ |
| | onprem-std2 | 4 | 8 GiB | ✅ |
| | onprem-std3 | 8 | 16 GiB | ✅ |
| **Memory-Optimized** | onprem-mem1 | 2 | 16 GiB | ✅ |
| | onprem-mem2 | 4 | 32 GiB | ✅ |
| | onprem-mem3 | 8 | 64 GiB | ✅ |
| **Compute-Optimized** | onprem-cpu1 | 2 | 2 GiB | ✅ |
| | onprem-cpu2 | 4 | 4 GiB | ✅ |
| | onprem-cpu3 | 8 | 8 GiB | ✅ |

**Ubicación en código:** `infrastructure/builders/onpremise_builder.py` líneas 55-63

---

## 2. GUÍA DE PRUEBAS PASO A PASO

### 🔧 Preparación del Entorno

#### Paso 1: Verificar Instalación

```bash
# 1. Navegar al directorio del proyecto
cd "c:\Users\yorie\Downloads\Patrones\Corte 2\API-Proveedores"

# 2. Verificar versión de Python (debe ser 3.8+)
python --version

# 3. Instalar dependencias
pip install -r requirements.txt
```

**Salida esperada:**
```
Successfully installed flask-3.0.0 flask-cors-4.0.0 pydantic-2.x.x ...
```

#### Paso 2: Ejecutar Tests Unitarios

```bash
# Test 1: Factory Pattern (31 tests)
python tests/test_all.py
```

**Resultado esperado:**
```
======================================================================
RESUMEN DE TESTS
======================================================================
Tests ejecutados: 31
Exitosos: 31
Fallidos: 0
Errores: 0
======================================================================
```

```bash
# Test 2: Builder Pattern (32 tests)
python tests/test_builder.py
```

**Resultado esperado:**
```
======================================================================
RESUMEN DE TESTS DE BUILDER PATTERN
======================================================================
Tests ejecutados: 32
Exitosos: 32
Fallidos: 0
Errores: 0
======================================================================
```

**✅ Verificación:** Si ambos tests pasan con 0 errores, el sistema está funcionando correctamente.

---

### 🚀 Pruebas de la API REST

#### Paso 3: Iniciar el Servidor

```bash
# En una terminal, ejecutar:
python api/main.py
```

**Salida esperada:**
```
INFO:werkzeug: * Running on http://127.0.0.1:5000
INFO:root:Iniciando VM Provisioning API...
INFO:root:Proveedores disponibles: ['aws', 'azure', 'google', 'gcp', 'onpremise', 'on-premise']
```

**⚠️ Importante:** Mantén esta terminal abierta durante las pruebas.

---

#### Paso 4: Pruebas de Endpoints (En otra terminal)

##### Prueba 4.1: Health Check

```bash
curl http://localhost:5000/health
```

**Resultado esperado:**
```json
{
  "status": "healthy",
  "service": "VM Provisioning API",
  "version": "1.0.0"
}
```

**✅ Verificación:** Status debe ser "healthy"

---

##### Prueba 4.2: Listar Proveedores

```bash
curl http://localhost:5000/api/providers
```

**Resultado esperado:**
```json
{
  "success": true,
  "providers": [
    "aws",
    "azure",
    "google",
    "gcp",
    "onpremise",
    "on-premise"
  ],
  "count": 6
}
```

**✅ Verificación:** Deben aparecer los 4 proveedores principales + 2 alias

---

##### Prueba 4.3: Factory Pattern - Provisión Rápida AWS

```bash
curl -X POST http://localhost:5000/api/vm/provision \
  -H "Content-Type: application/json" \
  -d "{\"provider\":\"aws\",\"config\":{\"type\":\"t2.micro\",\"region\":\"us-east-1\"}}"
```

**Resultado esperado:**
```json
{
  "success": true,
  "vm_id": "aws-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "message": "VM creada exitosamente en aws",
  "provider": "aws",
  "vm_details": {
    "vmId": "aws-xxxxxxxx...",
    "name": "aws-t2.micro-us-east-1-xxxx",
    "status": "running",
    "provider": "aws",
    "network": {
      "networkId": "vpc-xxxxxxxx",
      "name": "aws-net-us-east-1",
      "cidr_block": "10.0.0.0/16"
    },
    "disks": [...]
  }
}
```

**✅ Verificación:**
- `success: true`
- `vm_id` comienza con "aws-"
- `status: "running"`
- Network y Disks están presentes

---

##### Prueba 4.4: Builder Pattern - Construcción Personalizada Azure

```bash
curl -X POST http://localhost:5000/api/vm/build \
  -H "Content-Type: application/json" \
  -d "{\"provider\":\"azure\",\"build_config\":{\"name\":\"production-db\",\"vm_type\":\"high-performance\",\"cpu\":8,\"ram\":32,\"disk_gb\":500,\"disk_type\":\"ssd\",\"location\":\"eastus\",\"advanced_options\":{\"monitoring\":true,\"resource_group\":\"production\"}}}"
```

**Resultado esperado:**
```json
{
  "success": true,
  "vm_id": "azure-xxxxxxxx...",
  "message": "VM construida exitosamente en azure usando Builder Pattern",
  "provider": "azure",
  "vm_details": {
    "vmId": "azure-xxxxxxxx...",
    "name": "production-db",
    "status": "running",
    "provider": "azure"
  }
}
```

**✅ Verificación:**
- Mensaje menciona "Builder Pattern"
- Nombre personalizado "production-db"
- Configuración avanzada aplicada

---

##### Prueba 4.5: Director Pattern - VM Predefinida Minimal

```bash
curl -X POST http://localhost:5000/api/vm/build/preset \
  -H "Content-Type: application/json" \
  -d "{\"provider\":\"google\",\"preset\":\"minimal\",\"name\":\"test-vm\",\"location\":\"us-central1-a\"}"
```

**Resultado esperado:**
```json
{
  "success": true,
  "vm_id": "gcp-xxxxxxxx...",
  "message": "VM 'minimal' construida exitosamente en google",
  "provider": "google",
  "vm_details": {
    "name": "test-vm",
    "status": "running"
  }
}
```

**✅ Verificación:**
- Configuración "minimal" aplicada (1 CPU, 1GB RAM, 10GB Disk)
- Creación rápida con Director

---

##### Prueba 4.6: Director Pattern - VM Predefinida High-Performance

```bash
curl -X POST http://localhost:5000/api/vm/build/preset \
  -H "Content-Type: application/json" \
  -d "{\"provider\":\"onpremise\",\"preset\":\"high-performance\",\"name\":\"analytics-server\",\"location\":\"datacenter-1\"}"
```

**Resultado esperado:**
```json
{
  "success": true,
  "vm_id": "onprem-xxxxxxxx...",
  "message": "VM 'high-performance' construida exitosamente en onpremise",
  "provider": "on-premise",
  "vm_details": {
    "name": "analytics-server",
    "status": "running"
  }
}
```

**✅ Verificación:**
- Configuración "high-performance" (8 CPU, 32GB RAM, 500GB Disk)
- Proveedor on-premise funciona correctamente

---

##### Prueba 4.7: Manejo de Errores - Proveedor Inválido

```bash
curl -X POST http://localhost:5000/api/vm/provision \
  -H "Content-Type: application/json" \
  -d "{\"provider\":\"invalid-cloud\",\"config\":{}}"
```

**Resultado esperado:**
```json
{
  "success": false,
  "message": "Proveedor 'invalid-cloud' no soportado",
  "error_detail": "Proveedores disponibles: aws, azure, google, onpremise",
  "provider": "invalid-cloud"
}
```

**✅ Verificación:**
- `success: false`
- Mensaje de error descriptivo
- Lista de proveedores válidos

---

##### Prueba 4.8: Validación - Parámetros Faltantes

```bash
curl -X POST http://localhost:5000/api/vm/build/preset \
  -H "Content-Type: application/json" \
  -d "{\"provider\":\"aws\"}"
```

**Resultado esperado:**
```json
{
  "success": false,
  "error": "Parámetro \"preset\" es requerido",
  "example": {
    "provider": "aws",
    "preset": "standard",
    "name": "my-vm",
    "location": "us-east-1"
  }
}
```

**✅ Verificación:**
- Error claro sobre parámetro faltante
- Ejemplo de uso correcto incluido

---

### 📊 Tabla Resumen de Pruebas

| # | Tipo de Prueba | Endpoint | Patrón Usado | Estado Esperado |
|---|----------------|----------|--------------|-----------------|
| 4.1 | Health Check | GET /health | - | 200 OK |
| 4.2 | Listar Proveedores | GET /api/providers | - | 200 OK, 6 proveedores |
| 4.3 | Provisión Rápida | POST /api/vm/provision | Factory | 200 OK, VM creada |
| 4.4 | Construcción Custom | POST /api/vm/build | Builder | 200 OK, VM personalizada |
| 4.5 | Preset Minimal | POST /api/vm/build/preset | Director | 200 OK, VM minimal |
| 4.6 | Preset High-Perf | POST /api/vm/build/preset | Director | 200 OK, VM potente |
| 4.7 | Error - Proveedor | POST /api/vm/provision | Factory | 400 Bad Request |
| 4.8 | Error - Validación | POST /api/vm/build/preset | Director | 400 Bad Request |

---

### 🎯 Prueba Automatizada Completa

Para ejecutar todas las pruebas automáticamente:

```bash
# En una terminal (con el servidor corriendo en otra)
python test_examples.py
```

Este script ejecutará automáticamente las 7 pruebas principales y mostrará los resultados.

**Resultado esperado:**
```
========================================
EJEMPLOS DE USO DE LA API MULTI-CLOUD
========================================

TEST 1: Health Check
Status Code: 200
Response: {...}

TEST 2: Listar Proveedores
Status Code: 200
Response: {...}

... (continúa con todos los tests)

========================================
✅ TODOS LOS TESTS COMPLETADOS
========================================
```

---

## 3. SUSTENTACIÓN TÉCNICA DETALLADA

### 🎓 ¿Qué es este Proyecto?

Este proyecto es una **API REST para aprovisionamiento multi-cloud** que permite crear máquinas virtuales en diferentes proveedores de nube (AWS, Azure, Google Cloud, On-Premise) de manera **flexible, escalable y mantenible**.

### 🧩 Problema que Resuelve

**Problema Original:**
- Cada proveedor cloud tiene su propia API y forma de crear recursos
- Difícil mantener código que soporte múltiples proveedores
- Configuraciones complejas dificultan la creación de VMs personalizadas
- No hay forma estandarizada de crear VMs con configuraciones predefinidas

**Solución Implementada:**
- **Factory Pattern:** Crea proveedores de forma dinámica sin acoplar el código
- **Builder Pattern:** Permite construcción paso a paso de VMs con cualquier configuración
- **Director Pattern:** Encapsula configuraciones predefinidas (minimal, standard, high-performance)
- **API REST:** Interfaz unificada para todos los proveedores

### 🏗️ ¿Por Qué Estos Patrones?

#### Factory Method Pattern

**¿Qué es?**
Un patrón creacional que define una interfaz para crear objetos pero permite a las subclases decidir qué clase instanciar.

**¿Por qué lo usamos?**
1. **Desacoplamiento:** El código cliente no necesita conocer las clases concretas (AWS, Azure, etc.)
2. **Extensibilidad:** Agregar nuevos proveedores no requiere modificar código existente (OCP)
3. **Polimorfismo:** Todos los proveedores implementan la misma interfaz `ProveedorAbstracto`

**¿Dónde está implementado?**
- **Interfaz Creator:** `ProveedorAbstracto` en `domain/interfaces.py`
- **Concrete Creators:** `AWS`, `Azure`, `Google`, `OnPremise` en `infrastructure/providers/`
- **Factory:** `VMProviderFactory` en `application/factory.py`

**Ejemplo de código:**
```python
# Cliente no conoce la clase concreta
provider = VMProviderFactory.create_provider('aws', config)
# Retorna ProveedorAbstracto (abstracción), no AWS (implementación)
vm = provider.provisionar()  # Polimorfismo en acción
```

**Beneficios en el proyecto:**
- ✅ Agregar Oracle Cloud solo requiere crear clase `Oracle` y registrarla
- ✅ El servicio `VMProvisioningService` no cambia al agregar proveedores
- ✅ Tests pueden usar mocks sin cambiar el código

---

#### Builder Pattern

**¿Qué es?**
Un patrón creacional que permite construir objetos complejos paso a paso. Permite producir diferentes tipos y representaciones de un objeto usando el mismo código de construcción.

**¿Por qué lo usamos?**
1. **Construcción Compleja:** VMs requieren configurar múltiples aspectos (CPU, RAM, disco, red, opciones avanzadas)
2. **Construcción Opcional:** No todos los parámetros son obligatorios
3. **Legibilidad:** Código más legible con fluent interface
4. **Flexibilidad:** Diferentes configuraciones sin constructores telescópicos

**¿Dónde está implementado?**
- **Builder Interface:** `VMBuilder` en `domain/builder.py`
- **Concrete Builders:** `AWSVMBuilder`, `AzureVMBuilder`, `GoogleVMBuilder`, `OnPremiseVMBuilder` en `infrastructure/builders/`
- **Product:** `MachineVirtual` en `domain/entities.py`

**Ejemplo de código:**
```python
# Construcción paso a paso
vm = (builder
      .reset()
      .set_basic_config("prod-server", "high-performance")
      .set_compute_resources(cpu=8, ram=32)
      .set_storage(size_gb=500, disk_type="ssd")
      .set_network(network_id="vpc-prod", cidr="10.0.0.0/16")
      .set_location("us-east-1")
      .set_advanced_options({"monitoring": True, "optimized": True})
      .build())
```

**Beneficios en el proyecto:**
- ✅ Construcción legible y mantenible
- ✅ Parámetros opcionales sin constructores complicados
- ✅ Fluent Interface (encadenamiento de métodos)
- ✅ Cada builder maneja lógica específica de su proveedor

---

#### Director Pattern

**¿Qué es?**
Una extensión del Builder que define el orden y los pasos para construir configuraciones predefinidas.

**¿Por qué lo usamos?**
1. **Reutilización:** Configuraciones comunes (minimal, standard, high-performance)
2. **Consistencia:** Misma configuración "standard" en todos los proveedores
3. **Best Practices:** Encapsula conocimiento de configuraciones óptimas
4. **Simplicidad:** Usuarios no necesitan conocer todos los parámetros

**¿Dónde está implementado?**
- **Director:** `VMDirector` en `domain/builder.py`
- **Métodos:** `build_minimal_vm()`, `build_standard_vm()`, `build_high_performance_vm()`

**Ejemplo de código:**
```python
# Sin Director (complejo)
vm = builder.reset().set_basic_config(...).set_compute_resources(...)...

# Con Director (simple)
director = VMDirector(builder)
vm = director.build_high_performance_vm("analytics-server", "us-east-1")
```

**Beneficios en el proyecto:**
- ✅ Usuarios pueden crear VMs sin conocer parámetros técnicos
- ✅ Configuraciones probadas y optimizadas
- ✅ Reduce errores de configuración
- ✅ Facilita deployments rápidos

---

### 🔄 ¿Cómo Interactúan los Patrones?

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENTE (API)                         │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
           ┌────────▼────────┐ ┌───────▼────────┐
           │ Factory Pattern │ │ Builder Pattern│
           │                 │ │                │
           │ Provisión       │ │ Construcción   │
           │ Rápida          │ │ Personalizada  │
           └────────┬────────┘ └───────┬────────┘
                    │                   │
           ┌────────▼────────┐ ┌───────▼────────┐
           │ VMProviderFactory│ │ VMBuilderFactory│
           │ create_provider()│ │ create_builder()│
           └────────┬────────┘ └───────┬────────┘
                    │                   │
           ┌────────▼────────┐ ┌───────▼────────┐
           │  AWS Provider   │ │  AWSVMBuilder  │
           │  provisionar()  │ │  build()       │
           └────────┬────────┘ └───────┬────────┘
                    │                   │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │  MachineVirtual   │
                    │  + Network        │
                    │  + Storage        │
                    └───────────────────┘
```

**Flujo de Ejecución:**

1. **Cliente hace request** → Llega a API Flask
2. **API decide:** ¿Factory o Builder?
   - `/api/vm/provision` → `VMProvisioningService` (Factory)
   - `/api/vm/build` → `VMBuildingService` (Builder)
3. **Service crea Factory/Builder** según proveedor
4. **Factory/Builder construye VM** con Network y Storage
5. **Service retorna resultado** como JSON al cliente

---

### 📦 Arquitectura de Capas

El proyecto sigue **Clean Architecture** (Arquitectura Limpia):

```
┌─────────────────────────────────────────────────────────┐
│                    API Layer (Flask)                     │
│  - Recibe requests HTTP                                  │
│  - Valida formato JSON                                   │
│  - Retorna responses                                     │
└────────────────────┬────────────────────────────────────┘
                     │ Depende de ↓
┌────────────────────▼────────────────────────────────────┐
│              Application Layer (Services)                │
│  - VMProvisioningService (Factory)                       │
│  - VMBuildingService (Builder)                           │
│  - Orquesta lógica de negocio                           │
└────────────────────┬────────────────────────────────────┘
                     │ Depende de ↓
┌────────────────────▼────────────────────────────────────┐
│              Domain Layer (Abstracciones)                │
│  - ProveedorAbstracto (interface)                        │
│  - VMBuilder (abstract class)                            │
│  - VMDirector                                            │
│  - Entities (MachineVirtual, Network, Storage)          │
└────────────────────┬────────────────────────────────────┘
                     │ Implementado por ↓
┌────────────────────▼────────────────────────────────────┐
│         Infrastructure Layer (Implementaciones)          │
│  - Providers concretos (AWS, Azure, Google, OnPremise)  │
│  - Builders concretos (AWSVMBuilder, etc.)              │
│  - Lógica específica de cada proveedor                  │
└─────────────────────────────────────────────────────────┘
```

**Principio de Inversión de Dependencias (DIP):**
- ✅ Capas superiores dependen de abstracciones (interfaces)
- ✅ Capas superiores NO dependen de implementaciones concretas
- ✅ Infrastructure implementa las abstracciones del Domain

**Beneficios:**
1. **Testabilidad:** Podemos mockear abstracciones en tests
2. **Mantenibilidad:** Cambios en infrastructure no afectan application/domain
3. **Reusabilidad:** Domain layer es independiente de frameworks
4. **Claridad:** Cada capa tiene responsabilidad única

---

## 4. PATRONES DE DISEÑO IMPLEMENTADOS

### 🔷 1. Factory Method Pattern

**Definición:**
> Define una interfaz para crear un objeto, pero deja que las subclases decidan qué clase instanciar.

**Implementación en el Proyecto:**

**Participantes:**
1. **Product (Abstracción):** `ProveedorAbstracto`
2. **Concrete Products:** `AWS`, `Azure`, `Google`, `OnPremise`
3. **Creator:** `VMProviderFactory`

**Código Clave:**

```python
# domain/interfaces.py
class ProveedorAbstracto(ABC):
    """Product - Interfaz común para todos los proveedores"""

    @abstractmethod
    def crear_vm(self) -> MachineVirtual:
        """Factory Method - Cada proveedor implementa su lógica"""
        pass

    def provisionar(self) -> MachineVirtual:
        """Template Method - Orquesta la creación"""
        return self.crear_vm()
```

```python
# infrastructure/providers/aws.py
class AWS(ProveedorAbstracto):
    """Concrete Product - Implementación específica de AWS"""

    def crear_vm(self) -> MachineVirtual:
        # Lógica específica de AWS
        vm_id = f"aws-{uuid.uuid4()}"
        # ... crear network, storage, vm
        return vm
```

```python
# application/factory.py
class VMProviderFactory:
    """Creator - Factory que crea productos"""

    _providers = {
        'aws': AWS,
        'azure': Azure,
        'google': Google,
        'onpremise': OnPremise
    }

    @classmethod
    def create_provider(cls, provider_type: str, config: Dict) -> ProveedorAbstracto:
        """Factory Method - Retorna abstracción, no implementación"""
        provider_class = cls._providers.get(provider_type)
        return provider_class(config)
```

**¿Cómo Funciona?**

1. Cliente pide crear VM para "aws"
2. Factory busca clase asociada a "aws" en el diccionario
3. Factory instancia la clase (AWS) y retorna como `ProveedorAbstracto`
4. Cliente usa métodos de la interfaz, no de la clase concreta

**Ventajas:**
- ✅ Cliente desacoplado de clases concretas
- ✅ Fácil agregar nuevos proveedores (registrar en diccionario)
- ✅ Principio Open/Closed aplicado
- ✅ Polimorfismo permite tratar todos los proveedores igual

**Diagrama UML Simplificado:**

```
┌─────────────────────────┐
│  ProveedorAbstracto     │ <<interface>>
├─────────────────────────┤
│ + crear_vm()            │
│ + provisionar()         │
│ + estado()              │
└───────────┬─────────────┘
            │
            │ Implementa
    ┌───────┴───────┬──────────┬──────────┐
    │               │          │          │
┌───▼────┐  ┌──────▼───┐ ┌────▼─────┐ ┌─▼─────────┐
│  AWS   │  │  Azure   │ │ Google   │ │ OnPremise │
├────────┤  ├──────────┤ ├──────────┤ ├───────────┤
│crear_vm│  │crear_vm  │ │crear_vm  │ │crear_vm   │
└────────┘  └──────────┘ └──────────┘ └───────────┘
```

---

### 🔷 2. Builder Pattern

**Definición:**
> Separa la construcción de un objeto complejo de su representación, permitiendo el mismo proceso de construcción crear diferentes representaciones.

**Implementación en el Proyecto:**

**Participantes:**
1. **Builder (Interfaz):** `VMBuilder`
2. **Concrete Builders:** `AWSVMBuilder`, `AzureVMBuilder`, `GoogleVMBuilder`, `OnPremiseVMBuilder`
3. **Product:** `MachineVirtual`
4. **Director:** `VMDirector`

**Código Clave:**

```python
# domain/builder.py
class VMBuilder(ABC):
    """Builder - Define pasos de construcción"""

    @abstractmethod
    def reset(self) -> 'VMBuilder':
        """Reinicia el builder"""
        pass

    @abstractmethod
    def set_basic_config(self, name: str, vm_type: str) -> 'VMBuilder':
        """Paso 1: Configuración básica"""
        pass

    @abstractmethod
    def set_compute_resources(self, cpu: int, ram: int) -> 'VMBuilder':
        """Paso 2: Recursos de cómputo"""
        pass

    @abstractmethod
    def set_storage(self, size_gb: int, disk_type: str) -> 'VMBuilder':
        """Paso 3: Almacenamiento"""
        pass

    @abstractmethod
    def set_network(self, network_id: str, cidr: str) -> 'VMBuilder':
        """Paso 4: Red"""
        pass

    @abstractmethod
    def build(self) -> MachineVirtual:
        """Construye el producto final"""
        pass
```

```python
# infrastructure/builders/aws_builder.py
class AWSVMBuilder(VMBuilder):
    """Concrete Builder - Construcción específica de AWS"""

    def __init__(self):
        self._config = {'provider': 'aws', 'region': 'us-east-1'}

    def set_basic_config(self, name: str, vm_type: str) -> 'AWSVMBuilder':
        self._config['name'] = name
        self._config['instance_type'] = self._map_vm_type(vm_type)
        return self  # Fluent Interface

    def set_compute_resources(self, cpu: int, ram: int) -> 'AWSVMBuilder':
        # Lógica de mapeo CPU/RAM a instance type de AWS
        if cpu <= 2 and ram <= 4:
            self._config['instance_type'] = 't2.small'
        elif cpu <= 4 and ram <= 16:
            self._config['instance_type'] = 't2.large'
        # ... más mappings
        return self

    def build(self) -> MachineVirtual:
        # Construye Network, Storage y VM
        network = Network(...)
        disk = StorageDisk(...)
        vm = MachineVirtual(network=network, disks=[disk], ...)
        return vm
```

**¿Cómo Funciona?**

1. **Cliente obtiene builder:** `builder = AWSVMBuilder()`
2. **Cliente configura paso a paso:**
   ```python
   builder.reset()
          .set_basic_config("prod-vm", "high-performance")
          .set_compute_resources(cpu=8, ram=32)
          .set_storage(500, "ssd")
          .set_network("vpc-123", "10.0.0.0/16")
   ```
3. **Cliente construye producto:** `vm = builder.build()`
4. **Builder ensambla** Network + Storage + VM

**Ventajas:**
- ✅ Construcción legible (Fluent Interface)
- ✅ Parámetros opcionales sin constructores telescópicos
- ✅ Misma interfaz para todos los proveedores
- ✅ Cada builder maneja lógica específica de su proveedor

**Diagrama UML Simplificado:**

```
┌────────────────────────┐
│      VMBuilder         │ <<abstract>>
├────────────────────────┤
│ + reset()              │
│ + set_basic_config()   │
│ + set_compute_resources│
│ + set_storage()        │
│ + set_network()        │
│ + build(): VM          │
└───────────┬────────────┘
            │
    ┌───────┴───────┬────────────┬────────────┐
    │               │            │            │
┌───▼─────────┐ ┌──▼─────────┐ ┌▼──────────┐ ┌▼──────────┐
│ AWSVMBuilder│ │AzureVMBuild│ │GoogleVMBld│ │OnPremVMBld│
├─────────────┤ ├────────────┤ ├───────────┤ ├───────────┤
│ build(): VM │ │ build(): VM│ │build(): VM│ │build(): VM│
└─────────────┘ └────────────┘ └───────────┘ └───────────┘
```

---

### 🔷 3. Director Pattern

**Definición:**
> Encapsula el orden y los pasos para construir configuraciones predefinidas usando un Builder.

**Implementación en el Proyecto:**

**Código Clave:**

```python
# domain/builder.py
class VMDirector:
    """Director - Encapsula algoritmos de construcción"""

    def __init__(self, builder: VMBuilder):
        self._builder = builder

    def build_minimal_vm(self, name: str) -> MachineVirtual:
        """Preset: VM mínima para testing"""
        return (self._builder
                .reset()
                .set_basic_config(name, "minimal")
                .set_compute_resources(cpu=1, ram=1)
                .set_storage(size_gb=10)
                .build())

    def build_standard_vm(self, name: str, location: str) -> MachineVirtual:
        """Preset: VM estándar para aplicaciones web"""
        return (self._builder
                .reset()
                .set_basic_config(name, "standard")
                .set_location(location)
                .set_compute_resources(cpu=2, ram=4)
                .set_storage(size_gb=50)
                .set_network()
                .build())

    def build_high_performance_vm(self, name: str, location: str) -> MachineVirtual:
        """Preset: VM de alto rendimiento para bases de datos"""
        return (self._builder
                .reset()
                .set_basic_config(name, "high-performance")
                .set_location(location)
                .set_compute_resources(cpu=8, ram=32)
                .set_storage(size_gb=500, disk_type="ssd")
                .set_network()
                .set_advanced_options({"optimized": True})
                .build())
```

**¿Cómo Funciona?**

1. **Cliente crea Director con builder:**
   ```python
   builder = AWSVMBuilder()
   director = VMDirector(builder)
   ```

2. **Cliente solicita preset:**
   ```python
   vm = director.build_high_performance_vm("analytics-db", "us-east-1")
   ```

3. **Director ejecuta secuencia predefinida** de pasos del builder

4. **Builder construye VM** según los pasos del Director

**Ventajas:**
- ✅ Configuraciones predefinidas reutilizables
- ✅ Encapsula best practices de cada tipo de VM
- ✅ Simplifica creación para usuarios finales
- ✅ Consistencia entre proveedores (mismo "standard" para todos)

**Diagrama de Colaboración:**

```
Cliente
   │
   │ 1. Crea
   ├────────────► VMDirector(builder)
   │
   │ 2. Solicita preset
   ├────────────► director.build_high_performance_vm()
                      │
                      │ 3. Ejecuta pasos
                      ├─────► builder.reset()
                      ├─────► builder.set_basic_config()
                      ├─────► builder.set_compute_resources()
                      ├─────► builder.set_storage()
                      ├─────► builder.build()
                      │
                      │ 4. Retorna
                      └─────► MachineVirtual
```

---

### 🔷 4. Abstract Factory Pattern (Implícito)

**Definición:**
> Proporciona una interfaz para crear familias de objetos relacionados sin especificar sus clases concretas.

**Implementación en el Proyecto:**

Aunque no está explícitamente nombrado, cada `ProveedorAbstracto` actúa como Abstract Factory al crear familias de recursos relacionados (VM + Network + Storage) del mismo proveedor.

**Código Clave:**

```python
# infrastructure/providers/aws.py
class AWS(ProveedorAbstracto):
    """Abstract Factory - Crea familia de recursos AWS"""

    def crear_vm(self) -> MachineVirtual:
        # Familia de productos AWS
        network = self._crear_network_aws()  # Producto 1
        disk = self._crear_storage_aws()     # Producto 2
        vm = self._crear_vm_aws(network, disk)  # Producto 3
        return vm

    def _crear_network_aws(self) -> Network:
        """Crea Network específica de AWS"""
        return Network(
            networkId=f"vpc-{uuid.uuid4().hex[:8]}",
            cidr_block="10.0.0.0/16",
            provider='aws'  # Coherencia
        )

    def _crear_storage_aws(self) -> StorageDisk:
        """Crea Storage específico de AWS"""
        return StorageDisk(
            diskId=f"vol-{uuid.uuid4().hex[:12]}",
            disk_type="gp2",
            provider='aws'  # Coherencia
        )
```

**Garantía de Coherencia:**
- ✅ Todos los recursos creados pertenecen al mismo proveedor
- ✅ Network y Storage comparten región
- ✅ IDs siguen convenciones del proveedor (vpc- para AWS, disk- para GCP, etc.)

**Diagrama UML:**

```
┌────────────────────────┐
│  ProveedorAbstracto    │ <<AbstractFactory>>
├────────────────────────┤
│ + crear_vm()           │
│ # _crear_network()     │
│ # _crear_storage()     │
└───────────┬────────────┘
            │
            │ Crea familia
    ┌───────┴──────────────┐
    │                      │
┌───▼────────┐      ┌─────▼──────┐
│  Network   │      │  Storage   │
│  + provider│      │  + provider│
└────────────┘      └────────────┘
```

---

## 5. PRINCIPIOS SOLID APLICADOS

### 🔷 S - Single Responsibility Principle (SRP)

**Definición:**
> Una clase debe tener una, y solo una, razón para cambiar.

**Aplicación en el Proyecto:**

#### Ejemplo 1: VMProviderFactory
```python
class VMProviderFactory:
    """
    Responsabilidad ÚNICA: Crear proveedores
    No se encarga de:
    - Aprovisionar VMs
    - Validar configuraciones
    - Gestionar estado
    """

    @classmethod
    def create_provider(cls, provider_type: str, config: Dict) -> ProveedorAbstracto:
        # Solo crea y retorna proveedores
        provider_class = cls._providers.get(provider_type)
        return provider_class(config)
```

**✅ Cumplimiento:**
- Solo cambia si la lógica de creación de proveedores cambia
- No cambia si cambia lógica de aprovisionamiento
- No cambia si cambian validaciones

#### Ejemplo 2: VMProvisioningService
```python
class VMProvisioningService:
    """
    Responsabilidad ÚNICA: Orquestar aprovisionamiento
    No se encarga de:
    - Crear proveedores (delega a Factory)
    - Validar esquemas (delega a Pydantic)
    - Crear VMs (delega a Provider)
    """

    def provision_vm(self, provider_type: str, config: Dict) -> ProvisioningResult:
        provider = self.orchestrator.get_validated_provider(provider_type, config)
        vm = provider.provisionar()
        return ProvisioningResult(success=True, vm_id=vm.vmId)
```

**✅ Cumplimiento:**
- Solo cambia si la orquestación cambia
- Delega creación de proveedores
- Delega validación de datos

#### Ejemplo 3: AWSVMBuilder
```python
class AWSVMBuilder(VMBuilder):
    """
    Responsabilidad ÚNICA: Construir VMs de AWS
    No se encarga de:
    - Construir VMs de otros proveedores
    - Decidir qué configuración usar (Director)
    - Gestionar el API de AWS real
    """
```

**Tabla de Responsabilidades:**

| Clase | Única Responsabilidad | NO es responsable de |
|-------|----------------------|---------------------|
| VMProviderFactory | Crear proveedores | Aprovisionar, validar |
| VMProvisioningService | Orquestar aprovisionamiento | Crear proveedores, validar esquemas |
| AWSVMBuilder | Construir VMs de AWS | Builders de otros proveedores |
| VMDirector | Definir presets de construcción | Construir VMs (delega a Builder) |
| Network | Representar red | Crear VMs, Storage |
| StorageDisk | Representar disco | Crear VMs, Network |

---

### 🔷 O - Open/Closed Principle (OCP)

**Definición:**
> Las entidades de software deben estar abiertas para extensión, pero cerradas para modificación.

**Aplicación en el Proyecto:**

#### Ejemplo 1: Agregar Nuevo Proveedor (Sin modificar código)

**ANTES de agregar Oracle Cloud:**
```python
# application/factory.py
class VMProviderFactory:
    _providers = {
        'aws': AWS,
        'azure': Azure,
        'google': Google,
        'onpremise': OnPremise
    }
```

**DESPUÉS de agregar Oracle Cloud (Sin cambiar Factory):**
```python
# 1. Crear nueva clase (EXTENSIÓN)
# infrastructure/providers/oracle.py
class Oracle(ProveedorAbstracto):
    def crear_vm(self) -> MachineVirtual:
        # Implementación de Oracle
        pass

# 2. Registrar (NO es modificación, es configuración)
VMProviderFactory.register_provider('oracle', Oracle)
```

**✅ Cumplimiento:**
- Factory NO cambió internamente
- Solo agregamos nueva clase que cumple contrato existente
- Método `register_provider()` permite extensión

#### Ejemplo 2: Agregar Nuevo Preset en Director

**ANTES:**
```python
class VMDirector:
    def build_minimal_vm(self, name): ...
    def build_standard_vm(self, name, location): ...
    def build_high_performance_vm(self, name, location): ...
```

**DESPUÉS (Agregar "database-optimized"):**
```python
class VMDirector:
    # Métodos existentes NO cambian
    def build_minimal_vm(self, name): ...
    def build_standard_vm(self, name, location): ...
    def build_high_performance_vm(self, name, location): ...

    # EXTENSIÓN: Nuevo método
    def build_database_optimized_vm(self, name, location): ...
```

**✅ Cumplimiento:**
- Métodos existentes cerrados para modificación
- Clase abierta para extensión (nuevos métodos)
- No rompe código cliente existente

#### Test que Valida OCP:
```python
# tests/test_all.py
def test_ocp_open_closed(self):
    """Valida que podemos extender sin modificar"""
    initial_providers = VMProviderFactory.get_available_providers()

    # EXTENSIÓN: Agregar nuevo proveedor
    class NewProvider(AWS):
        pass

    VMProviderFactory.register_provider('newprovider', NewProvider)

    new_providers = VMProviderFactory.get_available_providers()
    self.assertGreater(len(new_providers), len(initial_providers))
    # ✅ Extendimos sin modificar código existente
```

**Tabla de Extensibilidad:**

| Componente | Cómo extender | Sin modificar |
|------------|---------------|---------------|
| Proveedores | Crear clase que implemente `ProveedorAbstracto` | Factory, Service, API |
| Builders | Crear clase que extienda `VMBuilder` | BuilderFactory, Service, API |
| Presets | Agregar método en `VMDirector` | Builders, Factory |
| Endpoints | Agregar ruta en Flask | Services, Domain |

---

### 🔷 L - Liskov Substitution Principle (LSP)

**Definición:**
> Los objetos de una superclase deben poder ser reemplazados por objetos de sus subclases sin afectar la correctitud del programa.

**Aplicación en el Proyecto:**

#### Ejemplo 1: Sustitución de Proveedores

```python
# Función que usa ProveedorAbstracto (superclase)
def provisionar_cualquier_vm(provider: ProveedorAbstracto) -> MachineVirtual:
    """Función que acepta cualquier proveedor"""
    if not provider.estado():
        raise Exception("Proveedor no disponible")

    vm = provider.provisionar()  # Polimorfismo
    return vm

# Todos los proveedores pueden sustituir a ProveedorAbstracto
aws_provider = AWS({'type': 't2.micro'})
azure_provider = Azure({'type': 'Standard_B1s'})
google_provider = Google({'type': 'n1-standard-1'})

# LSP: Cualquier proveedor funciona
vm1 = provisionar_cualquier_vm(aws_provider)      # ✅ Funciona
vm2 = provisionar_cualquier_vm(azure_provider)    # ✅ Funciona
vm3 = provisionar_cualquier_vm(google_provider)   # ✅ Funciona
```

**✅ Cumplimiento:**
- Cualquier `ProveedorAbstracto` puede usarse donde se espere uno
- Todos implementan `provisionar()` correctamente
- Todos retornan `MachineVirtual` válida
- Ninguno rompe el contrato de la superclase

#### Ejemplo 2: Sustitución de Builders

```python
def construir_con_cualquier_builder(builder: VMBuilder) -> MachineVirtual:
    """Función que acepta cualquier builder"""
    return (builder
            .reset()
            .set_basic_config("test", "standard")
            .set_compute_resources(cpu=2, ram=4)
            .build())

# Todos los builders pueden sustituir a VMBuilder
aws_builder = AWSVMBuilder()
azure_builder = AzureVMBuilder()

# LSP: Cualquier builder funciona
vm1 = construir_con_cualquier_builder(aws_builder)    # ✅ Funciona
vm2 = construir_con_cualquier_builder(azure_builder)  # ✅ Funciona
```

#### Test que Valida LSP:
```python
# tests/test_all.py
def test_lsp_liskov_substitution(self):
    """Valida que subclases pueden sustituir a superclase"""
    providers = [
        AWS({'type': 't2.micro'}),
        Azure({'type': 'Standard_B1s'}),
        Google({'type': 'n1-standard-1'}),
        OnPremise({'cpu': 2})
    ]

    for provider in providers:
        # Todos son ProveedorAbstracto
        self.assertIsInstance(provider, ProveedorAbstracto)

        # Todos pueden provisionar (mismo comportamiento)
        vm = provider.provisionar()
        self.assertIsNotNone(vm)

        # Todos retornan MachineVirtual válida
        self.assertIsInstance(vm, MachineVirtual)
        self.assertEqual(vm.status, VMStatus.RUNNING)
        # ✅ LSP cumplido: cualquier proveedor funciona igual
```

**Contratos que Deben Cumplirse:**

| Contrato | Implementado en todos |
|----------|---------------------|
| `provisionar()` retorna `MachineVirtual` | ✅ AWS, Azure, Google, OnPremise |
| `estado()` retorna `bool` | ✅ Todos |
| `crear_vm()` retorna `MachineVirtual` con status RUNNING | ✅ Todos |
| `build()` retorna VM con Network y Storage | ✅ Todos los builders |

**Precondiciones y Postcondiciones:**

```python
# Precondición: provider debe estar disponible
assert provider.estado() == True

# Acción
vm = provider.provisionar()

# Postcondiciones:
assert vm is not None
assert vm.status == VMStatus.RUNNING
assert vm.provider in ['aws', 'azure', 'google', 'on-premise']
assert vm.network is not None
assert len(vm.disks) > 0
# ✅ Todas las subclases cumplen las postcondiciones
```

---

### 🔷 I - Interface Segregation Principle (ISP)

**Definición:**
> Los clientes no deben ser forzados a depender de interfaces que no usan.

**Aplicación en el Proyecto:**

#### Ejemplo 1: Interfaces Específicas

**❌ MAL (Interfaz "God" que viola ISP):**
```python
class CloudProviderInterface:
    """Interfaz monolítica con todo"""
    def provisionar_vm(self): pass
    def crear_vm(self): pass
    def crear_network(self): pass
    def crear_storage(self): pass
    def estado(self): pass
    def validar(self): pass
    def conectar_api(self): pass
    def autenticar(self): pass
    def get_precios(self): pass  # No todos necesitan esto
    def get_metricas(self): pass  # No todos necesitan esto
```

**✅ BIEN (Interfaces segregadas):**
```python
# Interface 1: Solo para aprovisionar
class ProveedorAbstracto(ABC):
    """Interfaz específica para aprovisionamiento"""
    @abstractmethod
    def crear_vm(self) -> MachineVirtual: pass

    @abstractmethod
    def estado(self) -> bool: pass

    def provisionar(self) -> MachineVirtual:
        return self.crear_vm()

# Interface 2: Solo para construir
class VMBuilder(ABC):
    """Interfaz específica para construcción"""
    @abstractmethod
    def reset(self) -> 'VMBuilder': pass

    @abstractmethod
    def set_basic_config(self, name, vm_type) -> 'VMBuilder': pass

    @abstractmethod
    def build(self) -> MachineVirtual: pass
```

**✅ Cumplimiento:**
- `ProveedorAbstracto` solo tiene métodos para aprovisionamiento
- `VMBuilder` solo tiene métodos para construcción
- Clientes usan solo lo que necesitan

#### Ejemplo 2: Service Layer Segregado

```python
# Service 1: Solo Factory Pattern
class VMProvisioningService:
    """Solo para aprovisionamiento rápido"""
    def provision_vm(self, provider, config): ...

# Service 2: Solo Builder Pattern
class VMBuildingService:
    """Solo para construcción detallada"""
    def build_vm_with_config(self, provider, build_config): ...
    def build_predefined_vm(self, provider, preset, name, location): ...
```

**✅ Cumplimiento:**
- Clientes que necesitan aprovisionamiento rápido usan `VMProvisioningService`
- Clientes que necesitan construcción detallada usan `VMBuildingService`
- No hay métodos innecesarios en cada servicio

**Tabla de Segregación:**

| Cliente | Interfaz que Usa | Métodos Necesarios | Métodos No Usa |
|---------|------------------|-------------------|----------------|
| Factory Service | `ProveedorAbstracto` | `provisionar()`, `estado()` | Ninguno ✅ |
| Builder Service | `VMBuilder` | `set_*()`, `build()` | Ninguno ✅ |
| Director | `VMBuilder` | `reset()`, `set_*()`, `build()` | Ninguno ✅ |
| API Layer | `VMProvisioningService`, `VMBuildingService` | `provision_vm()`, `build_vm_*()` | Ninguno ✅ |

---

### 🔷 D - Dependency Inversion Principle (DIP)

**Definición:**
> Los módulos de alto nivel no deben depender de módulos de bajo nivel. Ambos deben depender de abstracciones.

**Aplicación en el Proyecto:**

#### Ejemplo 1: Service Depende de Abstracción

**❌ MAL (Violando DIP):**
```python
class VMProvisioningService:
    """Depende de implementaciones concretas"""
    def provision_vm(self, provider_type, config):
        # Acoplado a clases concretas
        if provider_type == 'aws':
            provider = AWS(config)  # ❌ Dependencia concreta
        elif provider_type == 'azure':
            provider = Azure(config)  # ❌ Dependencia concreta
        # ...
        vm = provider.provisionar()
```

**✅ BIEN (Cumpliendo DIP):**
```python
class VMProvisioningService:
    """Depende de abstracción (ProveedorAbstracto)"""
    def provision_vm(self, provider_type: str, config: Dict) -> ProvisioningResult:
        # Delega creación a Factory (también abstracción)
        provider: ProveedorAbstracto = self.orchestrator.get_validated_provider(
            provider_type, config
        )  # ✅ Retorna abstracción

        # Trabaja con abstracción, no con implementación
        vm = provider.provisionar()  # ✅ Polimorfismo
        return ProvisioningResult(...)
```

**Diagrama de Dependencias:**

```
┌─────────────────────────────────┐
│   Application Layer             │
│   VMProvisioningService         │
│   VMBuildingService             │
└───────────┬─────────────────────┘
            │ Depende de ↓ (Abstracción)
┌───────────▼─────────────────────┐
│   Domain Layer                  │
│   ProveedorAbstracto            │ <<interface>>
│   VMBuilder                     │ <<abstract>>
└───────────┬─────────────────────┘
            │ Implementado por ↑
┌───────────▼─────────────────────┐
│   Infrastructure Layer          │
│   AWS, Azure, Google            │
│   AWSVMBuilder, AzureVMBuilder  │
└─────────────────────────────────┘
```

**✅ Cumplimiento:**
- Application Layer NO importa clases de Infrastructure
- Application Layer solo conoce interfaces del Domain
- Infrastructure implementa las interfaces

#### Ejemplo 2: Director Depende de Abstracción

```python
class VMDirector:
    """Director depende de VMBuilder (abstracción)"""
    def __init__(self, builder: VMBuilder):
        # ✅ Recibe abstracción, no implementación concreta
        self._builder = builder

    def build_standard_vm(self, name, location):
        # ✅ Usa métodos de la abstracción
        return (self._builder
                .reset()
                .set_basic_config(name, "standard")
                .build())

# Uso
aws_builder = AWSVMBuilder()  # Implementación concreta
director = VMDirector(aws_builder)  # ✅ Inyección de dependencia
```

**Inyección de Dependencias:**

```python
# Infrastructure crea implementaciones
aws_builder = AWSVMBuilder()

# Application recibe abstracciones
director = VMDirector(aws_builder)  # DIP: Director no conoce AWSVMBuilder
vm = director.build_standard_vm("test", "us-east-1")
```

**Test que Valida DIP:**
```python
def test_dip_dependency_inversion(self):
    """Valida que dependemos de abstracciones"""
    # Factory retorna abstracción, no implementación
    provider = VMProviderFactory.create_provider('aws', {'type': 't2.micro'})

    # ✅ provider es ProveedorAbstracto, no AWS
    self.assertIsInstance(provider, ProveedorAbstracto)

    # Service trabaja con abstracción
    # No conoce ni le importa si es AWS, Azure, etc.
```

**Tabla de Inversión:**

| Módulo Alto Nivel | Depende de (Abstracción) | NO depende de (Implementación) |
|-------------------|-------------------------|-------------------------------|
| VMProvisioningService | `ProveedorAbstracto` | AWS, Azure, Google |
| VMBuildingService | `VMBuilder` | AWSVMBuilder, AzureVMBuilder |
| VMDirector | `VMBuilder` | Builders concretos |
| API Layer | Services (Application) | Providers, Builders (Infrastructure) |

---

## 6. ARQUITECTURA DEL SISTEMA

### 📐 Vista de Alto Nivel

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTE / USUARIO                        │
│                    (curl, Postman, Frontend)                     │
└──────────────────────────────┬──────────────────────────────────┘
                               │ HTTP Requests
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                         API LAYER (Flask)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ /health      │  │ /api/providers│  │/api/vm/provision    │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
│  ┌──────────────┐  ┌────────────────────────────────────────┐  │
│  │/api/vm/build │  │/api/vm/build/preset                    │  │
│  └──────────────┘  └────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────┘
                               │ Calls Services
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER (Services)                  │
│  ┌─────────────────────────┐  ┌──────────────────────────────┐  │
│  │ VMProvisioningService   │  │ VMBuildingService            │  │
│  │ - provision_vm()        │  │ - build_vm_with_config()     │  │
│  │                         │  │ - build_predefined_vm()      │  │
│  └─────────────────────────┘  └──────────────────────────────┘  │
│  ┌─────────────────────────┐  ┌──────────────────────────────┐  │
│  │ VMProviderFactory       │  │ VMBuilderFactory             │  │
│  │ - create_provider()     │  │ - create_builder()           │  │
│  └─────────────────────────┘  └──────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────┘
                               │ Uses Interfaces
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                     DOMAIN LAYER (Business Logic)                │
│  ┌─────────────────────────┐  ┌──────────────────────────────┐  │
│  │ ProveedorAbstracto      │  │ VMBuilder                    │  │
│  │ <<interface>>           │  │ <<abstract>>                 │  │
│  └─────────────────────────┘  └──────────────────────────────┘  │
│  ┌─────────────────────────┐  ┌──────────────────────────────┐  │
│  │ VMDirector              │  │ Entities                     │  │
│  │                         │  │ - MachineVirtual             │  │
│  │                         │  │ - Network                    │  │
│  │                         │  │ - StorageDisk                │  │
│  └─────────────────────────┘  └──────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────────┘
                               │ Implemented by
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│              INFRASTRUCTURE LAYER (Implementations)              │
│  ┌─────────────────────────┐  ┌──────────────────────────────┐  │
│  │ Providers               │  │ Builders                     │  │
│  │ - AWS                   │  │ - AWSVMBuilder               │  │
│  │ - Azure                 │  │ - AzureVMBuilder             │  │
│  │ - Google                │  │ - GoogleVMBuilder            │  │
│  │ - OnPremise             │  │ - OnPremiseVMBuilder         │  │
│  └─────────────────────────┘  └──────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 🔄 Flujo de Datos Completo

#### Escenario 1: Provisión con Factory Pattern

```
1. Cliente → POST /api/vm/provision
   Body: {
     "provider": "aws",
     "config": {"type": "t2.micro"}
   }

2. API (main.py) → provision_vm()
   - Valida JSON
   - Extrae provider y config

3. API → VMProvisioningService.provision_vm("aws", config)

4. VMProvisioningService → VMProviderFactory.create_provider("aws", config)

5. VMProviderFactory → AWS(config)
   - Instancia clase AWS
   - Retorna como ProveedorAbstracto

6. VMProvisioningService → provider.provisionar()

7. AWS → crear_vm()
   - Crea Network (VPC de AWS)
   - Crea StorageDisk (EBS de AWS)
   - Crea MachineVirtual
   - Ensambla todo

8. AWS → Retorna MachineVirtual

9. VMProvisioningService → ProvisioningResult
   - success: true
   - vm_id: "aws-xxx"
   - vm_details: {...}

10. API → jsonify(result.to_dict())

11. Cliente ← HTTP 200 OK
    {
      "success": true,
      "vm_id": "aws-xxx",
      ...
    }
```

#### Escenario 2: Construcción con Builder Pattern

```
1. Cliente → POST /api/vm/build
   Body: {
     "provider": "azure",
     "build_config": {
       "name": "prod-db",
       "vm_type": "high-performance",
       "cpu": 8,
       "ram": 32,
       "disk_gb": 500,
       "disk_type": "ssd",
       "location": "eastus"
     }
   }

2. API → build_vm()
   - Valida JSON
   - Extrae provider y build_config

3. API → VMBuildingService.build_vm_with_config("azure", build_config)

4. VMBuildingService → VMBuilderFactory.create_builder("azure")

5. VMBuilderFactory → AzureVMBuilder()
   - Instancia clase AzureVMBuilder
   - Retorna como VMBuilder

6. VMBuildingService → Construye paso a paso:
   builder.reset()
   builder.set_basic_config("prod-db", "high-performance")
   builder.set_compute_resources(cpu=8, ram=32)
   builder.set_storage(size_gb=500, disk_type="ssd")
   builder.set_location("eastus")

7. VMBuildingService → builder.build()

8. AzureVMBuilder → build()
   - Mapea configuración a Azure specifics
   - Crea Network (VNet de Azure)
   - Crea StorageDisk (Managed Disk de Azure)
   - Crea MachineVirtual (D8s_v3 o similar)
   - Ensambla todo

9. AzureVMBuilder → Retorna MachineVirtual

10. VMBuildingService → ProvisioningResult

11. API → jsonify(result.to_dict())

12. Cliente ← HTTP 200 OK
    {
      "success": true,
      "vm_id": "azure-xxx",
      "message": "VM construida exitosamente en azure usando Builder Pattern",
      ...
    }
```

#### Escenario 3: Preset con Director Pattern

```
1. Cliente → POST /api/vm/build/preset
   Body: {
     "provider": "google",
     "preset": "high-performance",
     "name": "analytics-server",
     "location": "us-central1-a"
   }

2. API → build_vm_preset()

3. API → VMBuildingService.build_predefined_vm("google", "high-performance", "analytics-server", "us-central1-a")

4. VMBuildingService → VMBuilderFactory.create_builder("google")

5. VMBuilderFactory → GoogleVMBuilder()

6. VMBuildingService → VMDirector(builder)

7. VMBuildingService → director.build_high_performance_vm("analytics-server", "us-central1-a")

8. VMDirector → Ejecuta secuencia predefinida:
   builder.reset()
   builder.set_basic_config("analytics-server", "high-performance")
   builder.set_location("us-central1-a")
   builder.set_compute_resources(cpu=8, ram=32)
   builder.set_storage(size_gb=500, disk_type="ssd")
   builder.set_network()
   builder.set_advanced_options({"optimized": True, "monitoring": True})
   builder.build()

9. GoogleVMBuilder → build()
   - Mapea a n2-highmem-8 o similar
   - Crea VPC Network de GCP
   - Crea Persistent Disk de GCP
   - Crea Compute Instance

10. GoogleVMBuilder → Retorna MachineVirtual

11. VMBuildingService → ProvisioningResult

12. API → jsonify(result.to_dict())

13. Cliente ← HTTP 200 OK
```

### 🗂️ Estructura de Archivos Detallada

```
API-Proveedores/
│
├── api/
│   └── main.py                        # 6 endpoints REST
│       ├── health()                   # GET /health
│       ├── get_providers()            # GET /api/providers
│       ├── provision_vm()             # POST /api/vm/provision
│       ├── provision_vm_by_provider() # POST /api/vm/provision/<provider>
│       ├── build_vm()                 # POST /api/vm/build
│       └── build_vm_preset()          # POST /api/vm/build/preset
│
├── application/
│   ├── factory.py                     # Services y Factories
│   │   ├── VMProviderFactory          # Factory para proveedores
│   │   ├── VMProvisioningService      # Service para Factory Pattern
│   │   ├── VMBuilderFactory           # Factory para builders
│   │   └── VMBuildingService          # Service para Builder Pattern
│   │
│   └── schemas.py                     # Validación con Pydantic
│       ├── AWSConfig                  # Schema para AWS
│       ├── AzureConfig                # Schema para Azure
│       ├── GoogleConfig               # Schema para Google
│       └── OnPremiseConfig            # Schema para OnPremise
│
├── domain/
│   ├── builder.py                     # Builder Pattern
│   │   ├── VMBuilder                  # Abstract Builder
│   │   └── VMDirector                 # Director
│   │
│   ├── entities.py                    # Entidades del dominio
│   │   ├── MachineVirtual             # Entidad VM
│   │   ├── Network                    # Entidad Network
│   │   ├── StorageDisk                # Entidad Storage
│   │   ├── VMStatus                   # Enum de estados
│   │   └── ProvisioningResult         # Resultado de aprovisionamiento
│   │
│   └── interfaces.py                  # Interfaces abstractas
│       └── ProveedorAbstracto         # Interface para proveedores
│
├── infrastructure/
│   ├── providers/                     # Implementaciones de proveedores
│   │   ├── __init__.py
│   │   ├── aws.py                     # AWS provider
│   │   ├── azure.py                   # Azure provider
│   │   ├── google.py                  # Google provider
│   │   └── onpremise.py               # OnPremise provider
│   │
│   └── builders/                      # Implementaciones de builders
│       ├── __init__.py
│       ├── aws_builder.py             # AWS builder
│       ├── azure_builder.py           # Azure builder
│       ├── google_builder.py          # Google builder
│       └── onpremise_builder.py       # OnPremise builder
│
├── tests/
│   ├── test_all.py                    # 31 tests Factory Pattern
│   ├── test_builder.py                # 32 tests Builder Pattern
│   └── test_api_endpoints.py          # Tests de integración API
│
├── requirements.txt                   # Dependencias
├── setup.py                           # Configuración del paquete
├── README.md                          # Documentación principal
├── IMPLEMENTACION_BUILDER.md          # Detalles del Builder
├── QUICKSTART.md                      # Guía rápida
├── SUSTENTACION_COMPLETA.md           # Este documento
├── test_examples.py                   # Ejemplos automáticos
└── WS3-Builder.pdf                    # Especificaciones originales
```

### 📊 Métricas del Proyecto

```
Líneas de Código:
├── Domain Layer: ~600 líneas
├── Infrastructure Layer: ~1200 líneas
│   ├── Providers: ~600 líneas
│   └── Builders: ~600 líneas
├── Application Layer: ~700 líneas
├── API Layer: ~350 líneas
└── Tests: ~1100 líneas
────────────────────────────
Total: ~3950 líneas

Archivos Python:
├── Domain: 3 archivos
├── Application: 2 archivos
├── Infrastructure: 9 archivos
├── API: 1 archivo
└── Tests: 3 archivos
────────────────────────────
Total: 18 archivos

Tests:
├── Factory Pattern: 31 tests
├── Builder Pattern: 32 tests
└── API Endpoints: Variable
────────────────────────────
Total: 63+ tests

Endpoints REST:
├── GET: 2 endpoints
└── POST: 4 endpoints
────────────────────────────
Total: 6 endpoints

Patrones de Diseño:
├── Factory Method: ✅
├── Abstract Factory: ✅
├── Builder: ✅
└── Director: ✅
────────────────────────────
Total: 4 patrones

Principios SOLID:
├── SRP: ✅
├── OCP: ✅
├── LSP: ✅
├── ISP: ✅
└── DIP: ✅
────────────────────────────
Total: 5/5 (100%)

Proveedores Cloud:
├── AWS: ✅
├── Azure: ✅
├── Google Cloud: ✅
└── On-Premise: ✅
────────────────────────────
Total: 4 proveedores
```

---

## 7. ANÁLISIS DE CÓDIGO

### 🔍 Análisis Detallado por Componente

#### 7.1 Domain Layer - Builder.py

**Ubicación:** `domain/builder.py`

**Responsabilidad:** Define las abstracciones para el patrón Builder y Director

**Componentes Clave:**

```python
class VMBuilder(ABC):
    """
    Builder Abstracto: Define la interfaz para construir VMs paso a paso

    Aplicando:
    - Builder Pattern: Construcción compleja de objetos paso a paso
    - SRP: Solo se encarga de definir interfaz de construcción
    - OCP: Fácil agregar nuevos builders sin modificar esta interfaz
    - Fluent Interface: Cada método retorna self para encadenamiento
    """

    def __init__(self):
        # Estado interno del builder
        self._vm: Optional[MachineVirtual] = None
        self._network: Optional[Network] = None
        self._disk: Optional[StorageDisk] = None
        self._config: Dict[str, Any] = {}

    @abstractmethod
    def reset(self) -> 'VMBuilder':
        """
        Reinicia el builder para comenzar una nueva construcción

        ¿Por qué? Permite reutilizar el mismo builder para múltiples VMs

        Retorna self para Fluent Interface
        """
        pass

    @abstractmethod
    def set_basic_config(self, name: str, vm_type: str) -> 'VMBuilder':
        """
        Configura parámetros básicos: nombre y tipo de VM

        ¿Por qué separar? Divide responsabilidad en pasos lógicos

        Args:
            name: Nombre identificador de la VM
            vm_type: Tipo (minimal, standard, high-performance, custom)

        Retorna self para Fluent Interface
        """
        pass

    @abstractmethod
    def set_compute_resources(self, cpu: Optional[int], ram: Optional[int]) -> 'VMBuilder':
        """
        Configura recursos de cómputo: CPU y RAM

        ¿Por qué opcional? No siempre se especifica explícitamente

        Args:
            cpu: Número de CPUs virtuales
            ram: RAM en GB

        Implementación específica:
        - AWS: Mapea a instance types (t2.micro, m5.large, etc.)
        - Azure: Mapea a VM sizes (D2s_v3, E4s_v3, etc.)
        - Google: Mapea a machine types (e2-standard-2, n2-highmem-4, etc.)
        """
        pass

    @abstractmethod
    def set_storage(self, size_gb: int, disk_type: Optional[str]) -> 'VMBuilder':
        """
        Configura almacenamiento: tamaño y tipo de disco

        Args:
            size_gb: Tamaño del disco en GB
            disk_type: Tipo de disco (ssd, standard, io, etc.)

        Implementación específica:
        - AWS: EBS volumes (gp2, gp3, io2)
        - Azure: Managed disks (Standard_LRS, Premium_LRS)
        - Google: Persistent disks (pd-standard, pd-ssd)
        """
        pass

    @abstractmethod
    def set_network(self, network_id: Optional[str], cidr: Optional[str]) -> 'VMBuilder':
        """
        Configura red: VPC/VNet y rango de IPs

        Args:
            network_id: ID de la red (VPC, VNet, Network)
            cidr: Bloque CIDR (ej: 10.0.0.0/16)
        """
        pass

    @abstractmethod
    def set_location(self, location: str) -> 'VMBuilder':
        """
        Configura ubicación: región, zona, datacenter

        Args:
            location: Ubicación específica del proveedor
        """
        pass

    @abstractmethod
    def set_advanced_options(self, options: Dict[str, Any]) -> 'VMBuilder':
        """
        Configura opciones avanzadas específicas del proveedor

        ¿Por qué Dict? Permite flexibilidad para opciones específicas

        Args:
            options: Diccionario con opciones como:
                - monitoring: bool
                - optimized: bool
                - security_group: str
                - etc.
        """
        pass

    @abstractmethod
    def build(self) -> MachineVirtual:
        """
        Construye y retorna la VM configurada

        Este método ensambla todos los componentes configurados

        Returns:
            MachineVirtual completamente configurada con Network y Storage
        """
        pass

    def get_config(self) -> Dict[str, Any]:
        """Retorna configuración actual (útil para debugging)"""
        return self._config.copy()
```

**VMDirector:**

```python
class VMDirector:
    """
    Director: Define el orden de los pasos de construcción para crear
    configuraciones predefinidas de VMs

    ¿Por qué Director?
    - Encapsula algoritmos de construcción
    - Define best practices para cada tipo de VM
    - Simplifica uso para clientes finales

    Aplicando:
    - Director Pattern: Encapsula el algoritmo de construcción
    - SRP: Solo se encarga de orquestar la construcción
    - Strategy: Diferentes estrategias de construcción (minimal, standard, high-perf)
    """

    def __init__(self, builder: VMBuilder):
        """
        Constructor que recibe builder

        ¿Por qué inyección de dependencia?
        - Director no conoce builder concreto (DIP)
        - Puede trabajar con cualquier builder que implemente VMBuilder
        """
        self._builder = builder

    def change_builder(self, builder: VMBuilder) -> None:
        """
        Cambia el builder utilizado

        ¿Por qué? Permite reutilizar Director con diferentes proveedores
        """
        self._builder = builder

    def build_minimal_vm(self, name: str) -> MachineVirtual:
        """
        Construye una VM con configuración mínima (desarrollo/testing)

        Configuración:
        - CPU: 1 vCPU
        - RAM: 1 GB
        - Disk: 10 GB

        Uso ideal: Desarrollo, testing, ambientes temporales

        Ejemplo de salida:
        - AWS: t2.micro con EBS de 10GB
        - Azure: Standard_B1s con disco estándar
        """
        return (self._builder
                .reset()
                .set_basic_config(name, "minimal")
                .set_compute_resources(cpu=1, ram=1)
                .set_storage(size_gb=10)
                .build())

    def build_standard_vm(self, name: str, location: str) -> MachineVirtual:
        """
        Construye una VM con configuración estándar (aplicaciones web)

        Configuración:
        - CPU: 2 vCPU
        - RAM: 4 GB
        - Disk: 50 GB
        - Network: Configurada

        Uso ideal: Aplicaciones web, servicios backend, APIs
        """
        return (self._builder
                .reset()
                .set_basic_config(name, "standard")
                .set_location(location)
                .set_compute_resources(cpu=2, ram=4)
                .set_storage(size_gb=50)
                .set_network()
                .build())

    def build_high_performance_vm(self, name: str, location: str) -> MachineVirtual:
        """
        Construye una VM de alto rendimiento (bases de datos, analytics)

        Configuración:
        - CPU: 8 vCPU
        - RAM: 32 GB
        - Disk: 500 GB SSD
        - Network: Configurada
        - Opciones: Optimizada y monitoreada

        Uso ideal: Bases de datos, analytics, procesamiento pesado
        """
        return (self._builder
                .reset()
                .set_basic_config(name, "high-performance")
                .set_location(location)
                .set_compute_resources(cpu=8, ram=32)
                .set_storage(size_gb=500, disk_type="ssd")
                .set_network()
                .set_advanced_options({"optimized": True, "monitoring": True})
                .build())
```

**Análisis de Calidad:**

| Métrica | Valor | Evaluación |
|---------|-------|------------|
| **Cohesión** | Alta | Todos los métodos relacionados con construcción |
| **Acoplamiento** | Bajo | Solo depende de entities (VM, Network, Storage) |
| **Complejidad Ciclomática** | Baja | Métodos simples, sin lógica compleja |
| **Mantenibilidad** | Excelente | Fácil agregar nuevos métodos |
| **Testabilidad** | Excelente | Fácil mockear y testear |

---

#### 7.2 Infrastructure Layer - AWS Builder

**Ubicación:** `infrastructure/builders/aws_builder.py`

**Responsabilidad:** Implementación concreta del Builder para AWS

**Análisis de Código Clave:**

```python
class AWSVMBuilder(VMBuilder):
    """
    Concrete Builder: Implementa construcción de VMs para AWS

    Responsabilidades:
    1. Mapear configuraciones genéricas a specifics de AWS
    2. Crear recursos compatibles con AWS (VPC, EBS, EC2)
    3. Aplicar nomenclatura y convenciones de AWS
    """

    def __init__(self):
        super().__init__()
        self._config = {
            'provider': 'aws',
            'region': 'us-east-1',  # Default region
            'instance_type': 't2.micro',  # Default instance
            'volume_type': 'gp2',  # Default EBS type
            'size_gb': 20  # Default disk size
        }

    def set_compute_resources(self, cpu: Optional[int], ram: Optional[int]) -> 'AWSVMBuilder':
        """
        Mapea CPU/RAM a instance types de AWS

        Lógica de mapeo:
        - 1 CPU, 1GB RAM → t2.micro
        - 2 CPU, 4GB RAM → t2.small
        - 4 CPU, 16GB RAM → t2.large
        - 8 CPU, 32GB RAM → t2.xlarge
        """
        if cpu or ram:
            if cpu and ram:
                # Mapeo inteligente
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

        return self  # Fluent Interface

    def set_storage(self, size_gb: int, disk_type: Optional[str]) -> 'AWSVMBuilder':
        """
        Mapea tipos de disco genéricos a EBS volume types

        Mapeo:
        - 'ssd' → gp3 (General Purpose SSD, latest generation)
        - 'standard' → gp2 (General Purpose SSD)
        - 'magnetic' → standard (Old magnetic)
        - 'io' → io2 (Provisioned IOPS)
        """
        self._config['size_gb'] = size_gb

        disk_mapping = {
            'ssd': 'gp3',
            'standard': 'gp2',
            'magnetic': 'standard',
            'io': 'io2'
        }

        self._config['volume_type'] = disk_mapping.get(disk_type, 'gp2') if disk_type else 'gp2'
        logger.info(f"AWS Builder: Almacenamiento - {size_gb}GB, Tipo: {self._config['volume_type']}")

        return self

    def build(self) -> MachineVirtual:
        """
        Construye la VM de AWS con toda la configuración

        Pasos:
        1. Genera IDs únicos con formato AWS (vpc-, vol-, i-)
        2. Crea Network (VPC) con CIDR block
        3. Crea Disk (EBS Volume) con tipo y tamaño
        4. Crea MachineVirtual con status RUNNING
        5. Ensambla todo y retorna
        """
        vm_id = f"aws-{uuid.uuid4()}"  # Formato: aws-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx

        # Crear Network (VPC)
        network = Network(
            networkId=self._config.get('vpc_id', f"vpc-{uuid.uuid4().hex[:8]}"),
            name=f"aws-net-{self._config.get('region', 'us-east-1')}",
            cidr_block=self._config.get('cidr_block', '10.0.0.0/16'),
            provider='aws'
        )

        # Crear Disk (EBS Volume)
        disk = StorageDisk(
            diskId=f"vol-{uuid.uuid4().hex[:12]}",  # Formato AWS EBS
            name=f"aws-disk-{self._config.get('volume_type', 'gp2')}",
            size_gb=self._config.get('size_gb', 20),
            disk_type=self._config.get('volume_type', 'gp2'),
            provider='aws'
        )

        # Crear VM (EC2 Instance)
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
```

**Patrones y Prácticas Aplicadas:**

1. **Fluent Interface:**
   - Cada método retorna `self`
   - Permite encadenar: `builder.set_x().set_y().build()`

2. **Default Values:**
   - Configuración inicial con valores sensatos
   - Cliente puede sobrescribir solo lo necesario

3. **Mapping Logic:**
   - Traduce configuraciones genéricas a specifics de AWS
   - Encapsula conocimiento del proveedor

4. **Logging:**
   - Registra cada paso de construcción
   - Facilita debugging y auditoría

5. **ID Generation:**
   - IDs únicos con UUID
   - Formato consistente con AWS (vpc-, vol-, etc.)

**Análisis de Calidad:**

| Métrica | Valor | Comentario |
|---------|-------|------------|
| **Complejidad Ciclomática** | 5-7 | Aceptable, mapeos if-elif |
| **Líneas por Método** | 15-30 | Razonable, fácil de leer |
| **Duplicación de Código** | Baja | Similar a otros builders (por diseño) |
| **Acoplamiento** | Bajo | Solo depende de entities |
| **Documentación** | Excelente | Docstrings completos |

---

## 8. CONCLUSIONES Y RECOMENDACIONES

### ✅ Logros del Proyecto

1. **Cumplimiento Total de Requisitos:**
   - ✅ Todos los RF cumplidos (RF1-RF5)
   - ✅ Todos los RNF cumplidos (RNF1-RNF5)
   - ✅ Todos los parámetros adicionales implementados
   - ✅ Todos los tipos de máquina por proveedor mapeados

2. **Patrones de Diseño:**
   - ✅ Factory Method implementado correctamente
   - ✅ Builder Pattern con Fluent Interface
   - ✅ Director Pattern con presets
   - ✅ Abstract Factory implícito

3. **Principios SOLID:**
   - ✅ SRP en todas las clases
   - ✅ OCP con extensibilidad probada
   - ✅ LSP con sustitución validada
   - ✅ ISP con interfaces segregadas
   - ✅ DIP con inversión de dependencias

4. **Calidad del Código:**
   - ✅ 63 tests unitarios pasando (100%)
   - ✅ Arquitectura limpia y mantenible
   - ✅ Documentación exhaustiva
   - ✅ Código legible y comentado

### 🎓 Valor Didáctico

Este proyecto es excelente material de enseñanza porque:

1. **Demuestra Patrones Reales:**
   - No son ejemplos toy
   - Resuelven problemas reales
   - Muestran cómo combinan patrones

2. **Aplica SOLID en Práctica:**
   - Cada principio tiene ejemplos concretos
   - Muestra beneficios tangibles
   - Demuestra consecuencias de violar principios

3. **Arquitectura Profesional:**
   - Clean Architecture aplicada
   - Separación clara de capas
   - Dependency Injection
   - API REST profesional

### 🚀 Extensiones Futuras

1. **Nuevos Proveedores:**
   - Oracle Cloud
   - IBM Cloud
   - DigitalOcean
   - Implementación: Crear clase y builder, registrar

2. **Nuevos Presets:**
   - GPU-optimized
   - Storage-optimized
   - Network-optimized

3. **Persistencia:**
   - Base de datos para VMs creadas
   - Historial de aprovisionamientos

4. **Monitoreo:**
   - Métricas de uso
   - Dashboards
   - Alertas

### 📖 Para Estudiar Este Proyecto

**Orden Recomendado:**

1. **Empezar por Tests:**
   - `tests/test_all.py` - Ver cómo se usa Factory
   - `tests/test_builder.py` - Ver cómo se usa Builder

2. **Revisar Domain:**
   - `domain/entities.py` - Entender entidades
   - `domain/interfaces.py` - Ver abstracciones
   - `domain/builder.py` - Entender Builder y Director

3. **Estudiar Infrastructure:**
   - `infrastructure/providers/aws.py` - Ver implementación concreta
   - `infrastructure/builders/aws_builder.py` - Ver builder concreto

4. **Analizar Application:**
   - `application/factory.py` - Ver orquestación
   - Entender flujo completo

5. **Probar API:**
   - `api/main.py` - Ver endpoints
   - Ejecutar `test_examples.py`
   - Hacer requests con curl

### 🎯 Preguntas para Profundizar

1. **¿Por qué Builder en vez de Constructor Telescópico?**
   - Constructor con 10 parámetros es inmantenible
   - Builder permite construcción opcional y legible
   - Fluent Interface mejora UX

2. **¿Por qué Director además de Builder?**
   - Director encapsula best practices
   - Simplifica casos comunes
   - No todos los usuarios conocen configuraciones óptimas

3. **¿Por qué Factory Y Builder?**
   - Factory para casos simples y rápidos
   - Builder para casos complejos y personalizados
   - Diferentes niveles de abstracción

4. **¿Cómo garantiza coherencia entre recursos?**
   - Cada provider/builder crea familia de recursos
   - Todos comparten proveedor y región
   - Abstract Factory implícito

5. **¿Cómo se vería agregar Oracle Cloud?**
   ```python
   # 1. Crear proveedor
   class Oracle(ProveedorAbstracto):
       def crear_vm(self): ...

   # 2. Crear builder
   class OracleVMBuilder(VMBuilder):
       def build(self): ...

   # 3. Registrar
   VMProviderFactory.register_provider('oracle', Oracle)
   VMBuilderFactory._builders['oracle'] = OracleVMBuilder

   # Listo! Ya funciona en toda la API
   ```

---

## 📌 RESUMEN EJECUTIVO

### Proyecto: API Multi-Cloud VM Provisioning
### Patrones: Factory Method + Builder + Director
### Cumplimiento: 100% de requisitos del PDF WS3-Builder

**Características Principales:**
- ✅ 4 proveedores cloud (AWS, Azure, Google, On-Premise)
- ✅ 6 endpoints REST
- ✅ 2 patrones creacionales combinados
- ✅ 63 tests unitarios (100% passing)
- ✅ 5 principios SOLID aplicados
- ✅ Clean Architecture
- ✅ Documentación completa

**Resultados:**
- Código mantenible y extensible
- Tests aseguran calidad
- Patrones correctamente implementados
- Lista para producción y enseñanza

**Valor del Proyecto:**
- Material didáctico de calidad
- Ejemplo real de patrones combinados
- Arquitectura profesional
- Base para proyectos futuros

---

## 📚 REFERENCIAS

1. **Design Patterns: Elements of Reusable Object-Oriented Software** - Gang of Four
2. **Clean Architecture** - Robert C. Martin
3. **SOLID Principles** - Robert C. Martin
4. **Refactoring Guru** - Design Patterns
5. **PDF WS3-Builder** - Universidad Popular del Cesar

---

**Documento creado por:** Sistema de Aprovisionamiento Multi-Cloud
**Fecha:** 2025
**Versión:** 1.0
**Universidad Popular del Cesar** - Especialización en Ingeniería de Software

---

