"""
API Layer - REST API Implementation
Implementación de la API REST usando Flask
Aplicando RNF4 (Stateless), RNF5 (JSON), RF1-RF5
"""
import sys
import os

# Agregar el directorio raíz al path para importaciones
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from typing import Dict, Any

from application.factory import VMProvisioningService

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Crear aplicación Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS

# Service (DIP: Inyección de dependencia)
provisioning_service = VMProvisioningService()


@app.route('/health', methods=['GET'])
def health_check():
    """
    Endpoint de health check
    """
    return jsonify({
        'status': 'healthy',
        'service': 'VM Provisioning API',
        'version': '1.0.0'
    }), 200


@app.route('/api/providers', methods=['GET'])
def get_providers():
    """
    RF5: Endpoint para listar proveedores disponibles
    
    Returns:
        JSON con lista de proveedores soportados
    """
    try:
        providers = provisioning_service.get_supported_providers()
        
        return jsonify({
            'success': True,
            'providers': providers,
            'count': len(providers)
        }), 200
        
    except Exception as e:
        logger.error(f"Error obteniendo proveedores: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@app.route('/api/vm/provision', methods=['POST'])
def provision_vm():
    """
    RF1: Endpoint principal para aprovisionar VMs
    RF2: Invoca la lógica correspondiente según el proveedor
    RF3: Devuelve estado del aprovisionamiento
    RF4: Registra logs (sin información sensible)
    
    Request Body (JSON):
    {
        "provider": "aws|azure|google|onpremise",
        "config": {
            "type": "instance_type",
            "region": "us-east-1",
            ... (parámetros específicos del proveedor)
        }
    }
    
    Returns:
        JSON con resultado del aprovisionamiento
    """
    try:
        # RNF5: Validar que el request es JSON
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type debe ser application/json'
            }), 400
        
        # Obtener datos del request
        data: Dict[str, Any] = request.get_json()
        
        # Validar parámetros requeridos
        if 'provider' not in data:
            return jsonify({
                'success': False,
                'error': 'Parámetro "provider" es requerido',
                'example': {
                    'provider': 'aws',
                    'config': {
                        'type': 't2.micro',
                        'region': 'us-east-1'
                    }
                }
            }), 400
        
        provider = str(data.get('provider', ''))
        config = data.get('config', {})
        
        # RNF3: Log sin información sensible
        logger.info(f"Solicitud de aprovisionamiento - Proveedor: {provider}")
        
        # Llamar al servicio de aprovisionamiento
        result = provisioning_service.provision_vm(provider, config)
        
        # RF3: Preparar respuesta con estado
        response = result.to_dict()
        
        # Determinar código de estado HTTP
        status_code = 200 if result.success else 400
        
        return jsonify(response), status_code
        
    except Exception as e:
        logger.error(f"Error en endpoint de aprovisionamiento: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'detail': str(e)
        }), 500


@app.route('/api/vm/provision/<provider>', methods=['POST'])
def provision_vm_by_provider(provider: str):
    """
    RF1: Endpoint alternativo con proveedor en la URL
    
    Ejemplo: POST /api/vm/provision/aws
    
    Request Body (JSON):
    {
        "config": {
            "type": "t2.micro",
            "region": "us-east-1"
        }
    }
    """
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type debe ser application/json'
            }), 400
        
        data: Dict[str, Any] = request.get_json()
        config = data.get('config', {})
        
        logger.info(f"Solicitud de aprovisionamiento - Proveedor: {provider}")
        
        result = provisioning_service.provision_vm(provider, config)
        response = result.to_dict()
        status_code = 200 if result.success else 400
        
        return jsonify(response), status_code
        
    except Exception as e:
        logger.error(f"Error en aprovisionamiento: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Manejador de rutas no encontradas"""
    return jsonify({
        'success': False,
        'error': 'Endpoint no encontrado',
        'available_endpoints': [
            'GET /health',
            'GET /api/providers',
            'POST /api/vm/provision',
            'POST /api/vm/provision/<provider>'
        ]
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Manejador de errores internos"""
    logger.error(f"Error 500: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor'
    }), 500


if __name__ == '__main__':
    # RNF4: API Stateless para escalabilidad
    logger.info("Iniciando VM Provisioning API...")
    logger.info(f"Proveedores disponibles: {provisioning_service.get_supported_providers()}")
    
    # Modo debug solo para desarrollo
    app.run(host='0.0.0.0', port=5000, debug=True)