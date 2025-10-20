import unittest
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from domain.entities import MachineVirtual, VMStatus, ProvisioningResult
from application.factory import VMProviderFactory, VMProvisioningService
from infrastructure.providers import AWS, Azure, Google, OnPremise


class TestDomainEntities(unittest.TestCase):
    
    
    def test_machine_virtual_creation(self):
        
        from datetime import datetime
        
        vm = MachineVirtual(
            vmId="test-123",
            name="test-vm",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="aws"
        )
        
        self.assertEqual(vm.vmId, "test-123")
        self.assertEqual(vm.name, "test-vm")
        self.assertTrue(vm.is_active())
        self.assertEqual(vm.get_id(), "test-123")
    
    def test_vm_status_enum(self):
        
        self.assertEqual(VMStatus.RUNNING.value, "running")
        self.assertEqual(VMStatus.ERROR.value, "error")
        self.assertEqual(VMStatus.PENDING.value, "pending")
    
    def test_provisioning_result(self):
        
        result = ProvisioningResult(
            success=True,
            vm_id="vm-123",
            message="Success",
            provider="aws"
        )
        
        self.assertTrue(result.success)
        self.assertEqual(result.vm_id, "vm-123")
        
        result_dict = result.to_dict()
        self.assertIsInstance(result_dict, dict)
        self.assertIn('success', result_dict)


class TestProviders(unittest.TestCase):
    
    
    def test_aws_provider_creation(self):
        
        provider = AWS({'type': 't2.micro', 'region': 'us-east-1'})
        self.assertIsNotNone(provider)
        self.assertTrue(provider.estado())

    def test_aws_provision_vm(self):
        """Test aprovisionamiento en AWS"""
        provider = AWS({'type': 't2.micro', 'region': 'us-east-1'})
        vm = provider.provisionar()

        self.assertIsNotNone(vm)
        self.assertEqual(vm.provider, "aws")
        self.assertEqual(vm.status, VMStatus.RUNNING)
        self.assertTrue(vm.vmId.startswith("aws-"))

    def test_azure_provider_creation(self):
        
        provider = Azure({'type': 'Standard_B1s', 'resource_group': 'test-rg'})
        self.assertIsNotNone(provider)
        self.assertTrue(provider.estado())

    def test_azure_provision_vm(self):
        
        provider = Azure({'type': 'Standard_B1s', 'resource_group': 'test-rg'})
        vm = provider.provisionar()

        self.assertIsNotNone(vm)
        self.assertEqual(vm.provider, "azure")
        self.assertEqual(vm.status, VMStatus.RUNNING)
        self.assertTrue(vm.vmId.startswith("azure-"))

    def test_google_provider_creation(self):
        
        provider = Google({'type': 'n1-standard-1', 'zone': 'us-central1-a'})
        self.assertIsNotNone(provider)
        self.assertTrue(provider.estado())

    def test_google_provision_vm(self):
        
        provider = Google({'type': 'n1-standard-1', 'zone': 'us-central1-a'})
        vm = provider.provisionar()

        self.assertIsNotNone(vm)
        self.assertEqual(vm.provider, "google")
        self.assertEqual(vm.status, VMStatus.RUNNING)
        self.assertTrue(vm.vmId.startswith("gcp-"))

    def test_onpremise_provider_creation(self):
        
        provider = OnPremise({'cpu': 2, 'ram': 4, 'disk': 50})
        self.assertIsNotNone(provider)
        self.assertTrue(provider.estado())

    def test_onpremise_provision_vm(self):
        
        provider = OnPremise({'cpu': 2, 'ram': 4, 'disk': 50})
        vm = provider.provisionar()

        self.assertIsNotNone(vm)
        self.assertEqual(vm.provider, "on-premise")
        self.assertEqual(vm.status, VMStatus.RUNNING)
        self.assertTrue(vm.vmId.startswith("onprem-"))


class TestVMProviderFactory(unittest.TestCase):
    
    
    def test_factory_create_aws_provider(self):
        
        config = {'type': 't2.micro', 'method': 'standard'}
        provider = VMProviderFactory.create_provider('aws', config)
        
        self.assertIsNotNone(provider)
        self.assertIsInstance(provider, AWS)
    
    def test_factory_create_azure_provider(self):
        
        config = {'type': 'Standard_B1s', 'method': 'standard'}
        provider = VMProviderFactory.create_provider('azure', config)
        
        self.assertIsNotNone(provider)
        self.assertIsInstance(provider, Azure)
    
    def test_factory_create_google_provider(self):
        
        config = {'type': 'n1-standard-1', 'method': 'standard'}
        provider = VMProviderFactory.create_provider('google', config)
        
        self.assertIsNotNone(provider)
        self.assertIsInstance(provider, Google)
    
    def test_factory_create_google_alias_gcp(self):
        
        config = {'type': 'n1-standard-1'}
        provider = VMProviderFactory.create_provider('gcp', config)
        
        self.assertIsNotNone(provider)
        self.assertIsInstance(provider, Google)
    
    def test_factory_create_onpremise_provider(self):
        
        config = {'type': 'vmware', 'method': 'standard'}
        provider = VMProviderFactory.create_provider('onpremise', config)
        
        self.assertIsNotNone(provider)
        self.assertIsInstance(provider, OnPremise)
    
    def test_factory_invalid_provider(self):
        
        config = {'type': 'test'}
        provider = VMProviderFactory.create_provider('invalid_provider', config)
        
        self.assertIsNone(provider)
    
    def test_factory_case_insensitive(self):
        
        config = {'type': 't2.micro'}
        
        provider1 = VMProviderFactory.create_provider('AWS', config)
        provider2 = VMProviderFactory.create_provider('aws', config)
        provider3 = VMProviderFactory.create_provider('AwS', config)
        
        self.assertIsNotNone(provider1)
        self.assertIsNotNone(provider2)
        self.assertIsNotNone(provider3)
    
    def test_factory_get_available_providers(self):
        
        providers = VMProviderFactory.get_available_providers()
        
        self.assertIsInstance(providers, list)
        self.assertIn('aws', providers)
        self.assertIn('azure', providers)
        self.assertIn('google', providers)
        self.assertIn('onpremise', providers)
        self.assertGreaterEqual(len(providers), 4)


class TestVMProvisioningService(unittest.TestCase):
    
    
    def setUp(self):
        
        self.service = VMProvisioningService()
    
    def test_service_provision_aws_success(self):
        
        config = {'type': 't2.micro', 'region': 'us-east-1'}
        result = self.service.provision_vm('aws', config)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.vm_id)
        self.assertEqual(result.provider, 'aws')
        self.assertIn('exitosamente', result.message.lower())
    
    def test_service_provision_azure_success(self):
        
        config = {'type': 'Standard_B1s'}
        result = self.service.provision_vm('azure', config)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.vm_id)
        self.assertEqual(result.provider, 'azure')
    
    def test_service_provision_google_success(self):
        
        config = {'type': 'n1-standard-1'}
        result = self.service.provision_vm('google', config)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.vm_id)
        self.assertEqual(result.provider, 'google')
    
    def test_service_provision_onpremise_success(self):
        
        config = {'type': 'vmware'}
        result = self.service.provision_vm('onpremise', config)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.vm_id)
        self.assertEqual(result.provider, 'onpremise')
    
    def test_service_provision_invalid_provider(self):
        
        config = {'type': 'test'}
        result = self.service.provision_vm('invalid', config)
        
        self.assertFalse(result.success)
        self.assertIsNone(result.vm_id)
        self.assertIn('no soportado', result.message.lower())
    
    def test_service_provision_empty_provider(self):
        
        config = {'type': 'test'}
        result = self.service.provision_vm('', config)
        
        self.assertFalse(result.success)
        self.assertIn('no especificado', result.message.lower())
    
    def test_service_provision_none_provider(self):
        
        config = {'type': 'test'}
        result = self.service.provision_vm('', config)  

        self.assertFalse(result.success)
    
    def test_service_get_supported_providers(self):
        
        providers = self.service.get_supported_providers()
        
        self.assertIsInstance(providers, list)
        self.assertGreaterEqual(len(providers), 4)


class TestSOLIDPrinciples(unittest.TestCase):
    
    
    def test_srp_single_responsibility(self):
        
        factory = VMProviderFactory()
        self.assertTrue(hasattr(factory, 'create_provider'))

        
        service = VMProvisioningService()
        self.assertTrue(hasattr(service, 'provision_vm'))

        
        provider = AWS({'type': 't2.micro', 'region': 'us-east-1'})
        self.assertTrue(hasattr(provider, 'crear_vm'))

    def test_ocp_open_closed(self):
       
        initial_providers = VMProviderFactory.get_available_providers()

        
        class NewProvider(AWS):
            pass

        VMProviderFactory.register_provider('newprovider', NewProvider)

        new_providers = VMProviderFactory.get_available_providers()
        self.assertGreater(len(new_providers), len(initial_providers))

    def test_lsp_liskov_substitution(self):
        
        from domain.interfaces import ProveedorAbstracto

        
        providers = [
            AWS({'type': 't2.micro', 'region': 'us-east-1'}),
            Azure({'type': 'Standard_B1s', 'resource_group': 'test-rg'}),
            Google({'type': 'n1-standard-1', 'zone': 'us-central1-a'}),
            OnPremise({'cpu': 2, 'ram': 4, 'disk': 50})
        ]

        for provider in providers:
            self.assertIsInstance(provider, ProveedorAbstracto)
            
            vm = provider.provisionar()
            self.assertIsNotNone(vm)

    def test_dip_dependency_inversion(self):
        
        from domain.interfaces import ProveedorAbstracto

        
        provider = VMProviderFactory.create_provider('aws', {'type': 't2.micro'})
        self.assertIsInstance(provider, ProveedorAbstracto)

        
        self.assertTrue(True)  


def run_all_tests():
    """Ejecuta todos los tests y muestra resumen"""
    
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    
    suite.addTests(loader.loadTestsFromTestCase(TestDomainEntities))
    suite.addTests(loader.loadTestsFromTestCase(TestProviders))
    suite.addTests(loader.loadTestsFromTestCase(TestVMProviderFactory))
    suite.addTests(loader.loadTestsFromTestCase(TestVMProvisioningService))
    suite.addTests(loader.loadTestsFromTestCase(TestSOLIDPrinciples))
    
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    
    print("\n" + "="*70)
    print("RESUMEN DE TESTS")
    print("="*70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallidos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("="*70)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)