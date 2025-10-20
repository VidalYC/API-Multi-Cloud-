import unittest
import json
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.main import app


class TestAPIEndpoints(unittest.TestCase):
    
    
    @classmethod
    def setUpClass(cls):
        
        app.config['TESTING'] = True
        cls.client = app.test_client()
    
    def test_health_endpoint(self):
        
        response = self.client.get('/health')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'VM Provisioning API')
        self.assertIn('version', data)
    
    def test_get_providers_endpoint(self):
        
        response = self.client.get('/api/providers')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('providers', data)
        self.assertIn('aws', data['providers'])
        self.assertIn('azure', data['providers'])
        self.assertIn('google', data['providers'])
        self.assertIn('onpremise', data['providers'])
        self.assertGreater(data['count'], 0)
    
    def test_provision_vm_aws_success(self):
        
        payload = {
            "provider": "aws",
            "config": {
                "type": "t2.micro",
                "region": "us-east-1"
            }
        }
        
        response = self.client.post(
            '/api/vm/provision',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['vm_id'])
        self.assertIn('aws', data['vm_id'])
        self.assertEqual(data['provider'], 'aws')
        self.assertIn('exitosamente', data['message'].lower())
    
    def test_provision_vm_azure_success(self):
        
        payload = {
            "provider": "azure",
            "config": {
                "type": "Standard_B1s",
                "resource_group": "test-rg"
            }
        }
        
        response = self.client.post(
            '/api/vm/provision',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['vm_id'])
        self.assertIn('azure', data['vm_id'])
        self.assertEqual(data['provider'], 'azure')
    
    def test_provision_vm_google_success(self):
        
        payload = {
            "provider": "google",
            "config": {
                "type": "n1-standard-1",
                "zone": "us-central1-a"
            }
        }
        
        response = self.client.post(
            '/api/vm/provision',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['vm_id'])
        self.assertIn('gcp', data['vm_id'])
        self.assertEqual(data['provider'], 'google')
    
    def test_provision_vm_onpremise_success(self):
        
        payload = {
            "provider": "onpremise",
            "config": {
                "type": "vmware",
                "cpu": 4,
                "ram": 8
            }
        }
        
        response = self.client.post(
            '/api/vm/provision',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['vm_id'])
        self.assertIn('onprem', data['vm_id'])
    
    def test_provision_vm_with_url_provider(self):
        
        payload = {
            "config": {
                "type": "t2.micro",
                "region": "us-west-2"
            }
        }
        
        response = self.client.post(
            '/api/vm/provision/aws',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIsNotNone(data['vm_id'])
    
    def test_provision_vm_missing_provider(self):
        
        payload = {
            "config": {
                "type": "t2.micro"
            }
        }
        
        response = self.client.post(
            '/api/vm/provision',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('requerido', data['error'].lower())
    
    def test_provision_vm_invalid_provider(self):
        
        payload = {
            "provider": "invalid_cloud",
            "config": {
                "type": "test"
            }
        }
        
        response = self.client.post(
            '/api/vm/provision',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('no soportado', data['message'].lower())
    
    def test_provision_vm_invalid_content_type(self):
        
        payload = "provider=aws&type=t2.micro"
        
        response = self.client.post(
            '/api/vm/provision',
            data=payload,
            content_type='application/x-www-form-urlencoded'
        )
        
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('json', data['error'].lower())
    
    def test_provision_vm_case_insensitive_provider(self):
        
        payload = {
            "provider": "AWS",  
            "config": {
                "type": "t2.micro"
            }
        }
        
        response = self.client.post(
            '/api/vm/provision',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_not_found_endpoint(self):
        
        response = self.client.get('/api/nonexistent')
        
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertFalse(data['success'])
        self.assertIn('available_endpoints', data)
    
    def test_provision_multiple_vms_sequential(self):
        
        providers = ['aws', 'azure', 'google', 'onpremise']
        
        for provider in providers:
            payload = {
                "provider": provider,
                "config": {
                    "type": "test-type"
                }
            }
            
            response = self.client.post(
                '/api/vm/provision',
                data=json.dumps(payload),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertTrue(data['success'], f"Failed for provider: {provider}")
            self.assertIsNotNone(data['vm_id'])


class TestAPIResponseFormat(unittest.TestCase):
    
    
    @classmethod
    def setUpClass(cls):
        
        app.config['TESTING'] = True
        cls.client = app.test_client()
    
    def test_success_response_structure(self):
        
        payload = {
            "provider": "aws",
            "config": {"type": "t2.micro"}
        }
        
        response = self.client.post(
            '/api/vm/provision',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        
        self.assertIn('success', data)
        self.assertIn('vm_id', data)
        self.assertIn('message', data)
        self.assertIn('provider', data)
        self.assertIn('error_detail', data)
    
    def test_error_response_structure(self):
        
        payload = {
            "provider": "invalid",
            "config": {}
        }
        
        response = self.client.post(
            '/api/vm/provision',
            data=json.dumps(payload),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        
        
        self.assertIn('success', data)
        self.assertFalse(data['success'])
        self.assertIn('message', data)
    
    def test_providers_response_structure(self):
        
        response = self.client.get('/api/providers')
        data = json.loads(response.data)
        
        self.assertIn('success', data)
        self.assertIn('providers', data)
        self.assertIn('count', data)
        self.assertIsInstance(data['providers'], list)
        self.assertIsInstance(data['count'], int)


def run_api_tests():
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    
    suite.addTests(loader.loadTestsFromTestCase(TestAPIEndpoints))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIResponseFormat))
    
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    
    print("\n" + "="*70)
    print("RESUMEN DE TESTS DE API")
    print("="*70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallidos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_api_tests()
    sys.exit(0 if success else 1)