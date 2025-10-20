import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from typing import Dict, Any

from application.factory import VMProvisioningService, VMBuildingService
from application.clone_service import VMCloneService


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


app = Flask(__name__)
CORS(app)  


provisioning_service = VMProvisioningService()
building_service = VMBuildingService()
clone_service = VMCloneService()


@app.route('/health', methods=['GET'])
def health_check():
    
    return jsonify({
        'status': 'healthy',
        'service': 'VM Provisioning API',
        'version': '2.0.0'
    }), 200


@app.route('/api/providers', methods=['GET'])
def get_providers():
    
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


@app.route('/api/vm/types', methods=['GET'])
def get_vm_types():
    
    try:
        vm_types = {
            'standard': {
                'name': 'Standard VM',
                'description': 'Máquina virtual de propósito general (General Purpose)',
                'characteristics': {
                    'memoryOptimization': False,
                    'diskOptimization': False,
                    'use_cases': ['Aplicaciones web', 'Servidores de aplicación', 'Desarrollo y testing']
                },
                'aws_types': ['t3.medium', 'm5.large', 'm5.xlarge'],
                'azure_types': ['D2s_v3', 'D4s_v3', 'D8s_v3'],
                'gcp_types': ['e2-standard-2', 'e2-standard-4', 'e2-standard-8'],
                'onpremise_types': ['onprem-std1', 'onprem-std2', 'onprem-std3']
            },
            'memory-optimized': {
                'name': 'VM Optimizada en Memoria',
                'description': 'Máquina virtual optimizada para cargas con alta demanda de memoria',
                'characteristics': {
                    'memoryOptimization': True,
                    'diskOptimization': False,
                    'use_cases': ['Bases de datos en memoria', 'Caché distribuido', 'Análisis big data']
                },
                'aws_types': ['r5.large', 'r5.xlarge', 'r5.2xlarge'],
                'azure_types': ['E2s_v3', 'E4s_v3', 'E8s_v3'],
                'gcp_types': ['n2-highmem-2', 'n2-highmem-4', 'n2-highmem-8'],
                'onpremise_types': ['onprem-mem1', 'onprem-mem2', 'onprem-mem3']
            },
            'disk-optimized': {
                'name': 'VM Optimizada en Disco',
                'description': 'Máquina virtual optimizada para operaciones intensivas de CPU y disco',
                'characteristics': {
                    'memoryOptimization': False,
                    'diskOptimization': True,
                    'use_cases': ['Procesamiento batch', 'Codificación de video', 'Machine learning training']
                },
                'aws_types': ['c5.large', 'c5.xlarge', 'c5.2xlarge'],
                'azure_types': ['F2s_v2', 'F4s_v2', 'F8s_v2'],
                'gcp_types': ['n2-highcpu-2', 'n2-highcpu-4', 'n2-highcpu-8'],
                'onpremise_types': ['onprem-cpu1', 'onprem-cpu2', 'onprem-cpu3']
            }
        }

        return jsonify({
            'success': True,
            'vm_types': vm_types,
            'count': len(vm_types)
        }), 200

    except Exception as e:
        logger.error(f"Error obteniendo tipos de VM: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@app.route('/api/vm/provision', methods=['POST'])
def provision_vm():
    
    try:
        
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type debe ser application/json'
            }), 400
        
        
        data: Dict[str, Any] = request.get_json()
        
        
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
        
        
        logger.info(f"Solicitud de aprovisionamiento - Proveedor: {provider}")
        
        
        result = provisioning_service.provision_vm(provider, config)
        
        
        response = result.to_dict()
        
        
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


@app.route('/api/vm/build', methods=['POST'])
def build_vm():
    
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type debe ser application/json'
            }), 400

        data: Dict[str, Any] = request.get_json()

        
        if 'provider' not in data:
            return jsonify({
                'success': False,
                'error': 'Parámetro "provider" es requerido',
                'example': {
                    'provider': 'aws',
                    'build_config': {
                        'name': 'my-vm',
                        'vm_type': 'standard',
                        'cpu': 4,
                        'ram': 16,
                        'disk_gb': 100,
                        'location': 'us-east-1'
                    }
                }
            }), 400

        if 'build_config' not in data:
            return jsonify({
                'success': False,
                'error': 'Parámetro "build_config" es requerido'
            }), 400

        provider = str(data.get('provider', ''))
        build_config = data.get('build_config', {})

        logger.info(f"Solicitud de construcción (Builder) - Proveedor: {provider}")

        
        result = building_service.build_vm_with_config(provider, build_config)

        response = result.to_dict()
        status_code = 200 if result.success else 400

        return jsonify(response), status_code

    except Exception as e:
        logger.error(f"Error en endpoint de construcción: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'detail': str(e)
        }), 500


@app.route('/api/vm/build/preset', methods=['POST'])
def build_vm_preset():
    
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type debe ser application/json'
            }), 400

        data: Dict[str, Any] = request.get_json()

        
        required_params = ['provider', 'preset', 'name']
        for param in required_params:
            if param not in data:
                return jsonify({
                    'success': False,
                    'error': f'Parámetro "{param}" es requerido',
                    'example': {
                        'provider': 'aws',
                        'preset': 'standard',
                        'name': 'my-vm',
                        'location': 'us-east-1'
                    }
                }), 400

        provider = str(data.get('provider', ''))
        preset = str(data.get('preset', ''))
        name = str(data.get('name', ''))
        location = str(data.get('location', 'us-east-1'))

        logger.info(f"Solicitud de construcción predefinida - Proveedor: {provider}, Preset: {preset}")

        
        result = building_service.build_predefined_vm(provider, preset, name, location)

        response = result.to_dict()
        status_code = 200 if result.success else 400

        return jsonify(response), status_code

    except Exception as e:
        logger.error(f"Error en endpoint de preset: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'detail': str(e)
        }), 500


@app.route('/api/vm/build/standard', methods=['POST'])
def build_standard_vm():
    
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type debe ser application/json'
            }), 400

        data: Dict[str, Any] = request.get_json()

        
        required_params = ['provider', 'name', 'location']
        for param in required_params:
            if param not in data:
                return jsonify({
                    'success': False,
                    'error': f'Parámetro "{param}" es requerido',
                    'example': {
                        'provider': 'aws',
                        'name': 'web-server-prod',
                        'location': 'us-east-1',
                        'size': 'medium'
                    }
                }), 400

        provider = str(data.get('provider', ''))
        name = str(data.get('name', ''))
        location = str(data.get('location', ''))
        size = str(data.get('size', 'medium'))

        logger.info(f"Solicitud Standard VM - Proveedor: {provider}, Nombre: {name}")

        
        result = building_service.build_vm_type(provider, 'standard', name, location, size)

        response = result.to_dict()
        status_code = 200 if result.success else 400

        return jsonify(response), status_code

    except Exception as e:
        logger.error(f"Error en endpoint Standard VM: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'detail': str(e)
        }), 500


@app.route('/api/vm/build/memory-optimized', methods=['POST'])
def build_memory_optimized_vm():
    
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type debe ser application/json'
            }), 400

        data: Dict[str, Any] = request.get_json()

        required_params = ['provider', 'name', 'location']
        for param in required_params:
            if param not in data:
                return jsonify({
                    'success': False,
                    'error': f'Parámetro "{param}" es requerido'
                }), 400

        provider = str(data.get('provider', ''))
        name = str(data.get('name', ''))
        location = str(data.get('location', ''))
        size = str(data.get('size', 'medium'))

        logger.info(f"Solicitud Memory-Optimized VM - Proveedor: {provider}")

        result = building_service.build_vm_type(provider, 'memory-optimized', name, location, size)

        response = result.to_dict()
        status_code = 200 if result.success else 400

        return jsonify(response), status_code

    except Exception as e:
        logger.error(f"Error en endpoint Memory-Optimized VM: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'detail': str(e)
        }), 500


@app.route('/api/vm/build/disk-optimized', methods=['POST'])
def build_disk_optimized_vm():
    
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type debe ser application/json'
            }), 400

        data: Dict[str, Any] = request.get_json()

        required_params = ['provider', 'name', 'location']
        for param in required_params:
            if param not in data:
                return jsonify({
                    'success': False,
                    'error': f'Parámetro "{param}" es requerido'
                }), 400

        provider = str(data.get('provider', ''))
        name = str(data.get('name', ''))
        location = str(data.get('location', ''))
        size = str(data.get('size', 'medium'))

        logger.info(f"Solicitud Disk-Optimized VM - Proveedor: {provider}")

        result = building_service.build_vm_type(provider, 'disk-optimized', name, location, size)

        response = result.to_dict()
        status_code = 200 if result.success else 400

        return jsonify(response), status_code

    except Exception as e:
        logger.error(f"Error en endpoint Disk-Optimized VM: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'detail': str(e)
        }), 500


@app.route('/api/vm/clone', methods=['POST'])
def clone_vm():
    
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type debe ser application/json'
            }), 400

        data: Dict[str, Any] = request.get_json()

        
        if 'prototype_name' not in data:
            return jsonify({
                'success': False,
                'error': 'Parámetro "prototype_name" es requerido',
                'example': {
                    'prototype_name': 'aws-web-server',
                    'new_vm_name': 'my-cloned-vm',
                    'customizations': {
                        'vcpus': 4,
                        'memoryGB': 8
                    }
                }
            }), 400

        if 'new_vm_name' not in data:
            return jsonify({
                'success': False,
                'error': 'Parámetro "new_vm_name" es requerido'
            }), 400

        prototype_name = str(data.get('prototype_name', ''))
        new_vm_name = str(data.get('new_vm_name', ''))
        customizations = data.get('customizations', {})

        logger.info(f"Solicitud de clonación - Prototipo: {prototype_name}, Nuevo nombre: {new_vm_name}")

        
        result = clone_service.clone_from_prototype(
            prototype_name=prototype_name,
            new_vm_name=new_vm_name,
            customizations=customizations
        )

        response = result.to_dict()
        status_code = 200 if result.success else 400

        return jsonify(response), status_code

    except Exception as e:
        logger.error(f"Error en endpoint de clonación: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'detail': str(e)
        }), 500


@app.route('/api/prototypes', methods=['GET'])
def list_prototypes():
    
    try:
        result = clone_service.list_available_prototypes()
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error al listar prototipos: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'detail': str(e)
        }), 500


@app.route('/api/prototypes/<name>', methods=['GET'])
def get_prototype_details(name: str):
    
    try:
        result = clone_service.get_prototype_details(name)
        status_code = 200 if result.get('success', False) else 404
        return jsonify(result), status_code

    except Exception as e:
        logger.error(f"Error al obtener detalles del prototipo: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor',
            'detail': str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    
    return jsonify({
        'success': False,
        'error': 'Endpoint no encontrado',
        'available_endpoints': [
            'GET /health',
            'GET /api/providers',
            'GET /api/vm/types',
            'POST /api/vm/provision',
            'POST /api/vm/provision/<provider>',
            'POST /api/vm/build',
            'POST /api/vm/build/preset',
            'POST /api/vm/build/standard',
            'POST /api/vm/build/memory-optimized',
            'POST /api/vm/build/disk-optimized',
            'POST /api/vm/clone',
            'GET /api/prototypes',
            'GET /api/prototypes/<name>'
        ]
    }), 404


@app.errorhandler(500)
def internal_error(error):
    
    logger.error(f"Error 500: {str(error)}")
    return jsonify({
        'success': False,
        'error': 'Error interno del servidor'
    }), 500


if __name__ == '__main__':
    
    logger.info("Iniciando VM Provisioning API...")
    logger.info(f"Proveedores disponibles: {provisioning_service.get_supported_providers()}")
    
    
    app.run(host='0.0.0.0', port=5000, debug=True)