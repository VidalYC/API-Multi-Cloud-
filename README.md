# 🚀 API Multi-Cloud VM Provisioning

API REST para aprovisionar y clonar máquinas virtuales en múltiples nubes (AWS, Azure, Google Cloud y On‑Premise). Implementa patrones creacionales y de construcción (Factory, Abstract Factory, Builder, Director y Prototype) y sigue principios SOLID.

## ✨ Qué hace
- Provisionamiento rápido con configuraciones estándar (Factory)  
- Construcción detallada paso a paso (Builder + Director)  
- Clonación de VMs/prototipos existentes (Prototype)  
- Familias coherentes de recursos (VM + Network + Disk) (Abstract Factory)  
- Validación con Pydantic

## 📁 Estructura (resumen)
- api/ — Entradas de la API (api/main.py)  
- application/ — Servicios y esquemas (factory, clone_service, schemas)  
- domain/ — Entidades, interfaces y builders  
- infrastructure/ — Providers y builders concretos  
- frontend/ — UI (si está presente)  
- docs/ — Documentación extendida  
- tests/ — Tests (pytest compatible)

## ⚙️ Requisitos e instalación
Requisitos: Python 3.8+, pip

```bash
git clone https://github.com/VidalYC/API-Multi-Cloud-.git
cd API-Multi-Cloud-
pip install -r requirements.txt
# (opcional) pip install -e .
```

## ▶️ Ejecutar (local)
```bash
python api/main.py
```
Por defecto la doc sugiere `http://localhost:5000` — verifica `api/main.py` si usa otro puerto (p. ej. uvicorn para FastAPI).

## 🔌 Endpoints principales (resumen)
- GET /health — Health check  
- GET /api/providers — Lista proveedores  
- POST /api/vm/provision — Provisionar VM (Factory)  
- POST /api/vm/provision/<provider> — Provisionar por proveedor  
- POST /api/vm/build — Construir VM (Builder)  
- POST /api/vm/build/preset — Construir con preset (Director)  
- POST /api/vm/clone — Clonar desde prototipo (Prototype)  
- GET /api/prototypes — Listar prototipos  
- GET /api/prototypes/<name> — Detalle prototipo

Ejemplo rápido de clonación:
```bash
curl -X POST http://localhost:5000/api/vm/clone \
  -H "Content-Type: application/json" \
  -d '{
    "prototype_name":"aws-web-server",
    "new_vm_name":"web-prod-01",
    "customizations":{"vcpus":4,"memoryGB":8,"region":"us-west-2"}
  }'
```

## ✅ Validaciones
- Pydantic para payloads (application/schemas.py)  
- Reglas típicas: sizeGB > 0, cpu/ram > 0, coherencia de región (red + discos), nombres válidos.

## 🧪 Tests
Ejecutar tests:
```bash
pytest -q
# o archivos concretos
python tests/test_all.py
python tests/test_builder.py
python tests/test_prototype.py
```

## ➕ Agregar un proveedor (rápido)
1. Crear clase en `infrastructure/providers/` que implemente `ProveedorAbstracto` (domain/interfaces.py).  
2. (Opcional) Crear builder en `infrastructure/builders/`.  
3. Registrar en la fábrica:  
```python
VMProviderFactory.register_provider('digitalocean', DigitalOcean)
```
4. Añadir tests.

## 🔐 Seguridad
- No guardar credenciales en el repo.  
- Usar variables de entorno o gestor de secretos.  
- Filtrar datos sensibles en logs.

## 📚 Referencias
- docs/PATRON_PROTOTYPE.md — Prototype (clonación, endpoints y ejemplos)  
- docs/PATRONES_Y_UML.md — Patrones principales y diagramas UML  
- application/schemas.py — Esquemas Pydantic  
- api/main.py — Punto de entrada API
