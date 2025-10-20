import requests
import json

# URL base de la API
BASE_URL = "http://localhost:5000"


def print_response(title, response):
    
    print(f"\n{'='*70}")
    print(f"{title}")
    print(f"{'='*70}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))


def test_health_check():
    
    response = requests.get(f"{BASE_URL}/health")
    print_response("TEST 1: Health Check", response)


def test_get_providers():
    
    response = requests.get(f"{BASE_URL}/api/providers")
    print_response("TEST 2: Listar Proveedores", response)


def test_provision_aws():
    
    payload = {
        "provider": "aws",
        "config": {
            "type": "t2.small",
            "region": "us-east-1",
            "sizeGB": 50,
            "volumeType": "gp3"
        }
    }
    response = requests.post(
        f"{BASE_URL}/api/vm/provision",
        json=payload
    )
    print_response("TEST 3: Provisionar VM en AWS (Factory)", response)


def test_build_custom_azure():
    
    payload = {
        "provider": "azure",
        "build_config": {
            "name": "database-prod-server",
            "vm_type": "high-performance",
            "cpu": 8,
            "ram": 32,
            "disk_gb": 1000,
            "disk_type": "ssd",
            "location": "eastus",
            "advanced_options": {
                "monitoring": True,
                "resource_group": "production",
                "optimized": True
            }
        }
    }
    response = requests.post(
        f"{BASE_URL}/api/vm/build",
        json=payload
    )
    print_response("TEST 4: Construir VM Personalizada en Azure (Builder)", response)


def test_build_preset_minimal():
    
    payload = {
        "provider": "google",
        "preset": "minimal",
        "name": "test-vm-dev",
        "location": "us-central1-a"
    }
    response = requests.post(
        f"{BASE_URL}/api/vm/build/preset",
        json=payload
    )
    print_response("TEST 5: VM Predefinida 'minimal' en Google (Director)", response)


def test_build_preset_high_performance():
    
    payload = {
        "provider": "onpremise",
        "preset": "high-performance",
        "name": "analytics-server",
        "location": "datacenter-1"
    }
    response = requests.post(
        f"{BASE_URL}/api/vm/build/preset",
        json=payload
    )
    print_response("TEST 6: VM Predefinida 'high-performance' OnPremise (Director)", response)


def test_provision_invalid_provider():
    
    payload = {
        "provider": "invalid_cloud",
        "config": {
            "type": "test"
        }
    }
    response = requests.post(
        f"{BASE_URL}/api/vm/provision",
        json=payload
    )
    print_response("TEST 7: Error - Proveedor Inválido", response)


def run_all_tests():
    
    print("\n" + "="*70)
    print("EJEMPLOS DE USO DE LA API MULTI-CLOUD VM PROVISIONING")
    print("Patrones: Factory Method + Builder + Director")
    print("="*70)

    try:
        test_health_check()
        test_get_providers()
        test_provision_aws()
        test_build_custom_azure()
        test_build_preset_minimal()
        test_build_preset_high_performance()
        test_provision_invalid_provider()

        print("\n" + "="*70)
        print("✅ TODOS LOS TESTS COMPLETADOS")
        print("="*70)

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se pudo conectar a la API")
        print("Asegúrate de que el servidor esté ejecutándose:")
        print("  python api/main.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")


if __name__ == "__main__":
    print("\n🚀 Iniciando tests de la API...")
    print("Asegúrate de que el servidor esté corriendo en http://localhost:5000\n")

    input("Presiona ENTER para continuar...")

    run_all_tests()
