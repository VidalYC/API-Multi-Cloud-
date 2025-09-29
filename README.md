# API Multi-Cloud VM Provisioning

## 📋 Descripción

API REST para el aprovisionamiento de máquinas virtuales en múltiples proveedores cloud (AWS, Azure, Google Cloud, On-Premise) implementando el **patrón Factory Method** y siguiendo principios **SOLID** y **Arquitectura Limpia**.

## 🏗️ Arquitectura

### Capas del Sistema

```
proyecto/
├── domain/                 # Capa de Dominio
│   ├── entities.py        # Entidades de negocio
│   └── interfaces.py      # Interfaces/Abstracciones
├── infrastructure/        # Capa de Infraestructura
│   └── providers.py       # Implementaciones concretas
├── application/           # Capa de Aplicación
│   └── factory.py         # Lógica de negocio y Factory
├── api/                   # Capa de Presentación
│   └── main.py           # API REST con Flask
├── tests/                # Tests unitarios
├── requirements.txt      # Dependencias
└── README.md            # Documentación
```

### Principios SOLID Aplicados

1. **SRP (Single Responsibility Principle)**
   - Cada clase tiene una única responsabilidad
   - `VMProviderFactory`: Solo crea proveedores
   - `VMProvisioningService`: Solo orquesta aprovisionamiento
   - Cada proveedor: Solo maneja su cloud específico

2. **OCP (Open/Closed Principle)**
   - Abierto para extensión: Nuevos proveedores se añaden sin modificar código existente
   - Cerrado para modificación: El core no cambia al agregar proveedores

3. **LSP (Liskov Substitution Principle)**
   - Todos los proveedores pueden sustituir a `ProveedorAbstracto`
   - El cliente usa la abstracción sin conocer la implementación

4. **ISP (Interface Segregation Principle)**
   - Interfaces específicas y cohesivas
   - Los clientes no dependen de métodos que no usan

5. **DIP (Dependency Inversion Principle)**
   - Módulos de alto nivel dependen de abstracciones
   - `VMProvisioningService` depende de `ProveedorAbstracto`, no de clases concretas

### Patrón Factory Method

```
ProveedorAbstracto (Creator)
    ├── AWS (Concrete Creator)
    ├── Azure (Concrete Creator)
    ├── Google (Concrete Creator)
    └── OnPremise (Concrete Creator)

VMProviderFactory
    └── create_provider() → Retorna ProveedorAbstracto
```

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd vm-provisioning-api
```

2. **Crear entorno virtual**
```bash
python -m venv venv
```

3. **Activar entorno virtual**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

5. **Ejecutar la aplicación**
```bash
python api/main.py
```

La API estará disponible en: `http://localhost:5000`

## 📡 Endpoints de la API

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

### 2. Listar Proveedores Disponibles
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

### 3. Aprovisionar VM (Método 1)
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
    "vpc": "vpc-12345",
    "ami": "ami-abc123"
  }
}
```

**Respuesta Exitosa:**
```json
{
  "success": true,
  "vm_id": "aws-a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "VM creada exitosamente en aws",
  "error_detail": null,
  "provider": "aws"
}
```

**Respuesta con Error:**
```json
{
  "success": false,
  "vm_id": null,
  "message": "Proveedor 'invalid' no soportado",
  "error_detail": "Proveedores disponibles: aws, azure, google, onpremise",
  "provider": "invalid"
}
```

### 4. Aprovisionar VM (Método 2 - Provider en URL)
```http
POST /api/vm/provision/azure
Content-Type: application/json
```

**Request Body:**
```json
{
  "config": {
    "type": "Standard_B1s",
    "resource_group": "myResourceGroup",
    "imagen": "UbuntuServer",
    "red_virtual": "myVNet"
  }
}
```

## 📝 Ejemplos de Uso

### Ejemplo 1: Aprovisionar en AWS

```bash
curl -X POST http://localhost:5000/api/vm/provision \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "aws",
    "config": {
      "type": "t2.micro",
      "region": "us-east-1"
    }
  }'
```

### Ejemplo 2: Aprovisionar en Azure

```bash
curl -X POST http://localhost:5000/api/vm/provision/azure \
  -H "Content-Type: application/json" \
  -d '{
    "config": {
      "type": "Standard_B1s",
      "resource_group": "prod-rg"
    }
  }'
```

### Ejemplo 3: Aprovisionar en Google Cloud

```bash
curl -X POST http://localhost:5000/api/vm/provision \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "google",
    "config": {
      "type": "n1-standard-1",
      "zone": "us-central1-a",
      "project": "my-project-123"
    }
  }'
```

### Ejemplo 4: Aprovisionar On-Premise

```bash
curl -X POST http://localhost:5000/api/vm/provision \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "onpremise",
    "config": {
      "type": "vmware",
      "cpu": 4,
      "ram": 8,
      "disk": 100
    }
  }'
```

## 🔧 Extender con Nuevos Proveedores

Para agregar un nuevo proveedor (ej: Oracle Cloud), sigue estos pasos:

### 1. Crear Clase del Proveedor

En `infrastructure/providers.py`:

```python
class OracleCloud(ProveedorAbstracto):
    """Implementación para Oracle Cloud"""
    
    def __init__(self, field_type: str, method_type: str):
        super().__init__()
        self.field = field_type
        self.method = method_type
    
    def crear_vm(self) -> MachineVirtual:
        """Factory Method para Oracle Cloud"""
        vm_id = f"oracle-{uuid.uuid4()}"
        
        logger.info(f"Creando VM en Oracle Cloud - ID: {vm_id}")
        
        vm = MachineVirtual(
            vmId=vm_id,
            name=f"oracle-instance-{vm_id[:8]}",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="oracle"
        )
        
        return vm
```

### 2. Registrar el Proveedor

En `application/factory.py`, agregar al diccionario:

```python
_providers = {
    'aws': AWS,
    'azure': Azure,
    'google': Google,
    'onpremise': OnPremise,
    'oracle': OracleCloud,  # Nuevo proveedor
}
```

**¡Listo! No se necesita modificar ningún otro código.**

## 🧪 Testing

### Estructura de Tests

```python
# tests/test_factory.py
import unittest
from application.factory import VMProviderFactory, VMProvisioningService

class TestVMProviderFactory(unittest.TestCase):
    
    def test_create_aws_provider(self):
        """Test creación de proveedor AWS"""
        provider = VMProviderFactory.create_provider('aws', {'type': 't2.micro'})
        self.assertIsNotNone(provider)
        self.assertEqual(provider.__class__.__name__, 'AWS')
    
    def test_invalid_provider(self):
        """Test proveedor inválido"""
        provider = VMProviderFactory.create_provider('invalid', {})
        self.assertIsNone(provider)
    
    def test_provision_success(self):
        """Test aprovisionamiento exitoso"""
        service = VMProvisioningService()
        result = service.provision_vm('aws', {'type': 't2.micro'})
        self.assertTrue(result.success)
        self.assertIsNotNone(result.vm_id)

if __name__ == '__main__':
    unittest.main()
```

### Ejecutar Tests

```bash
python -m pytest tests/
```

## 📊 Requerimientos Cumplidos

### Requerimientos Funcionales (RF)

✅ **RF1**: API con endpoint único para múltiples proveedores  
✅ **RF2**: Lógica específica por proveedor usando Factory Method  
✅ **RF3**: Respuesta con estado de aprovisionamiento (éxito/error)  
✅ **RF4**: Logging de solicitudes sin información sensible  
✅ **RF5**: Extensibilidad sin modificar código central (OCP)  

### Requerimientos No Funcionales (RNF)

✅ **RNF1 - Extensibilidad**: Nuevos proveedores se agregan fácilmente  
✅ **RNF2 - Mantenibilidad**: SOLID aplicado, especialmente DIP  
✅ **RNF3 - Seguridad**: Logs sin credenciales o tokens  
✅ **RNF4 - Escalabilidad**: API stateless, lista para escalar  
✅ **RNF5 - Compatibilidad**: Acepta JSON para todos los proveedores  

## 🎯 Principios de Diseño Aplicados

### Arquitectura Limpia

**Independencia de frameworks**: La lógica de negocio no depende de Flask  
**Testeable**: Lógica de negocio separada de infraestructura  
**Independencia de UI**: La API puede cambiar sin afectar el dominio  
**Independencia de BD**: No hay acoplamiento a bases de datos específicas  

### Separación de Responsabilidades

- **Domain Layer**: Entidades e interfaces del negocio
- **Application Layer**: Casos de uso y lógica de aplicación
- **Infrastructure Layer**: Implementaciones técnicas específicas
- **API Layer**: Capa de presentación REST

## 📚 Recursos Adicionales

### Documentación de Patrones

- [Factory Method Pattern - Refactoring Guru](https://refactoring.guru/design-patterns/factory-method)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Clean Architecture - Robert C. Martin](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

### Herramientas UML Utilizadas

- StarUML
- Draw.io
- PlantUML

## 👥 Autor

**Universidad Popular del Cesar**  
Especialización en Ingeniería de Software  
Asignatura: Patrones de Diseño de Software

## 📄 Licencia

Este proyecto es parte de un ejercicio académico.

---

## 🎓 Notas para Sustentación

### Puntos Clave a Destacar

1. **Factory Method Pattern**
   - Encapsula la creación de objetos
   - Permite extensión sin modificación
   - Desacopla cliente de implementaciones concretas

2. **SOLID Compliance**
   - Cada principio aplicado con ejemplos concretos
   - DIP especialmente importante para flexibilidad

3. **Arquitectura Limpia**
   - Separación clara de capas
   - Dependencias apuntan hacia el dominio
   - Fácil de testear y mantener

4. **Extensibilidad**
   - Demostrar cómo agregar Oracle Cloud en vivo
   - Sin modificar código existente
   - Solo agregar nueva clase y registrarla

5. **Escalabilidad**
   - API stateless
   - Sin sesiones ni estado compartido
   - Lista para balanceo de carga