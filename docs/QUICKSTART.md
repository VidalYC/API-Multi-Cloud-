# 🚀 Quick Start - API Multi-Cloud VM Provisioning

## ✅ Proyecto Completado

Tu proyecto ha sido **exitosamente escalado** con el patrón Builder.

### 📊 Estadísticas Finales

```
✅ 63 Tests Pasando
   ├── 31 tests Factory Pattern
   └── 32 tests Builder Pattern

✅ 2 Patrones Creacionales
   ├── Factory Method + Abstract Factory
   └── Builder + Director

✅ 4 Proveedores Cloud
   ├── AWS
   ├── Azure
   ├── Google Cloud
   └── On-Premise

✅ 6 Endpoints REST
   ├── GET /health
   ├── GET /api/providers
   ├── POST /api/vm/provision
   ├── POST /api/vm/provision/<provider>
   ├── POST /api/vm/build (Nuevo)
   └── POST /api/vm/build/preset (Nuevo)
```

---

## 🏃 Ejecutar el Proyecto

### 1. Verificar Tests (Recomendado)

```bash
# Tests del Factory Pattern (31 tests)
python tests/test_all.py

# Tests del Builder Pattern (32 tests)
python tests/test_builder.py

# Tests de endpoints API
python tests/test_api_endpoints.py
```

**Resultado Esperado:** Todos los tests deben pasar ✅

---

### 2. Iniciar el Servidor API

```bash
python api/main.py
```

**Salida esperada:**
```
INFO:werkzeug:WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
 * Running on http://0.0.0.0:5000
```

---

### 3. Probar los Endpoints

#### Opción A: Usando curl

```bash
# 1. Health Check
curl http://localhost:5000/health

# 2. Listar proveedores
curl http://localhost:5000/api/providers

# 3. Provisionar VM rápida (Factory Pattern)
curl -X POST http://localhost:5000/api/vm/provision \
  -H "Content-Type: application/json" \
  -d '{"provider":"aws","config":{"type":"t2.micro","region":"us-east-1"}}'

# 4. Construir VM personalizada (Builder Pattern)
curl -X POST http://localhost:5000/api/vm/build \
  -H "Content-Type: application/json" \
  -d '{"provider":"azure","build_config":{"name":"test-vm","vm_type":"standard","cpu":4,"ram":16,"disk_gb":100,"location":"eastus"}}'

# 5. Crear VM predefinida (Director Pattern)
curl -X POST http://localhost:5000/api/vm/build/preset \
  -H "Content-Type: application/json" \
  -d '{"provider":"google","preset":"high-performance","name":"db-server","location":"us-central1-a"}'
```

#### Opción B: Usando el Script de Ejemplos

En otra terminal (con el servidor corriendo):

```bash
python test_examples.py
```

Este script ejecutará automáticamente ejemplos de todos los endpoints.

---

## 📚 Documentación

### Archivos Clave

- **[README.md](README.md)** - Documentación completa del proyecto
- **[IMPLEMENTACION_BUILDER.md](IMPLEMENTACION_BUILDER.md)** - Detalles de la implementación del Builder
- **[WS3-Builder.pdf](WS3-Builder.pdf)** - Especificaciones originales

### Estructura del Código

```
API-Proveedores/
├── api/main.py                 # 6 Endpoints REST
├── application/factory.py       # Factory + Builder Services
├── domain/
│   ├── builder.py              # Builder Interface + Director
│   ├── entities.py             # Entities (VM, Network, Disk)
│   └── interfaces.py           # Abstract Interfaces
├── infrastructure/
│   ├── builders/               # 4 Concrete Builders
│   └── providers/              # 4 Concrete Providers
└── tests/
    ├── test_all.py             # 31 Factory tests
    ├── test_builder.py         # 32 Builder tests
    └── test_api_endpoints.py   # API integration tests
```

---

## 🎯 Casos de Uso

### Caso 1: VM Rápida para Testing (Factory)
```bash
POST /api/vm/provision
{
  "provider": "aws",
  "config": {"type": "t2.micro"}
}
```
**Tiempo:** ⚡ Instantáneo
**Uso:** Testing, desarrollo, prototipos

### Caso 2: VM de Producción Personalizada (Builder)
```bash
POST /api/vm/build
{
  "provider": "azure",
  "build_config": {
    "name": "prod-server",
    "vm_type": "high-performance",
    "cpu": 8,
    "ram": 32,
    "disk_gb": 500,
    "disk_type": "ssd",
    "location": "eastus",
    "advanced_options": {
      "monitoring": true,
      "resource_group": "production"
    }
  }
}
```
**Tiempo:** 🔧 Detallado
**Uso:** Producción, configuraciones específicas

### Caso 3: VM Predefinida (Director)
```bash
POST /api/vm/build/preset
{
  "provider": "google",
  "preset": "standard",
  "name": "web-server",
  "location": "us-central1-a"
}
```
**Tiempo:** ⚡ Rápido con configuración robusta
**Uso:** Despliegues estándar, best practices

---

## 🔍 Verificación Rápida

### ¿Todo funcionando?

Ejecuta este comando para verificar rápidamente:

```bash
python tests/test_all.py && python tests/test_builder.py && echo "✅ PROYECTO COMPLETAMENTE FUNCIONAL"
```

Si ves "✅ PROYECTO COMPLETAMENTE FUNCIONAL", todo está perfecto.

---

## 💡 Próximos Pasos

1. **Revisar** [README.md](README.md) para documentación completa
2. **Explorar** [IMPLEMENTACION_BUILDER.md](IMPLEMENTACION_BUILDER.md) para entender la arquitectura
3. **Ejecutar** el servidor y probar los endpoints
4. **Experimentar** con diferentes configuraciones de VMs

---

## 🎓 Para la Presentación

### Demostración Sugerida

1. **Mostrar tests pasando** (todos 63 ✅)
2. **Ejecutar servidor**
3. **Demostrar Factory Pattern** (provisión rápida)
4. **Demostrar Builder Pattern** (construcción detallada)
5. **Demostrar Director Pattern** (presets predefinidos)
6. **Explicar principios SOLID** aplicados
7. **Mostrar extensibilidad** (cómo agregar nuevo proveedor)

### Puntos Clave a Destacar

- ✅ **2 patrones creacionales** trabajando juntos
- ✅ **63 tests** asegurando calidad
- ✅ **SOLID compliant** en toda la arquitectura
- ✅ **Extensible** sin modificar código existente
- ✅ **API REST** profesional y documentada
- ✅ **Multi-cloud** agnóstico de proveedor

---

## ❓ Solución de Problemas

### El servidor no inicia
```bash
# Reinstalar dependencias
pip install -r requirements.txt
```

### Tests fallan
```bash
# Verificar que estás en el directorio correcto
cd "API-Proveedores"

# Ejecutar tests individualmente
python tests/test_all.py
python tests/test_builder.py
```

### Error "ModuleNotFoundError"
```bash
# Asegúrate de tener todas las dependencias
pip install flask flask-cors pydantic python-dotenv requests
```

---

## 🏆 ¡Éxito!

Tu proyecto está **100% funcional** y listo para presentación.

Tienes:
- ✅ Código limpio y bien estructurado
- ✅ Tests exhaustivos
- ✅ Documentación completa
- ✅ Patrones de diseño correctamente implementados
- ✅ Principios SOLID aplicados

**¡Felicitaciones!** 🎉
