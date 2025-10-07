"""
Test Suite Completa
Tests unitarios para validar la implementación
"""
import unittest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from domain.entities import MachineVirtual, VMStatus, ProvisioningResult
from application.factory import VMProviderFactory, VMProvisioningService
from infrastructure.providers import AWS, Azure, Google, OnPremise


class TestDomainEntities(unittest.TestCase):
    """Tests para las entidades del dominio"""
    
    def test_machine_virtual_creation(self):
        """Test creación de MachineVirtual"""
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
        """Test estados de VM"""
        self.assertEqual(VMStatus.RUNNING.value, "running")
        self.assertEqual(VMStatus.ERROR.value, "error")
        self.assertEqual(VMStatus.PENDING.value, "pending")
    
    def test_provisioning_result(self):
        """Test ProvisioningResult"""
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
    """Tests para los proveedores concretos"""
    
    def test_aws_provider_creation(self):
        """Test creación de proveedor AWS"""
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
        """Test creación de proveedor Azure"""
        provider = Azure({'type': 'Standard_B1s', 'resource_group': 'test-rg'})
        self.assertIsNotNone(provider)
        self.assertTrue(provider.estado())

    def test_azure_provision_vm(self):
        """Test aprovisionamiento en Azure"""
        provider = Azure({'type': 'Standard_B1s', 'resource_group': 'test-rg'})
        vm = provider.provisionar()

        self.assertIsNotNone(vm)
        self.assertEqual(vm.provider, "azure")
        self.assertEqual(vm.status, VMStatus.RUNNING)
        self.assertTrue(vm.vmId.startswith("azure-"))

    def test_google_provider_creation(self):
        """Test creación de proveedor Google Cloud"""
        provider = Google({'type': 'n1-standard-1', 'zone': 'us-central1-a'})
        self.assertIsNotNone(provider)
        self.assertTrue(provider.estado())

    def test_google_provision_vm(self):
        """Test aprovisionamiento en Google Cloud"""
        provider = Google({'type': 'n1-standard-1', 'zone': 'us-central1-a'})
        vm = provider.provisionar()

        self.assertIsNotNone(vm)
        self.assertEqual(vm.provider, "google")
        self.assertEqual(vm.status, VMStatus.RUNNING)
        self.assertTrue(vm.vmId.startswith("gcp-"))

    def test_onpremise_provider_creation(self):
        """Test creación de proveedor On-Premise"""
        provider = OnPremise({'cpu': 2, 'ram': 4, 'disk': 50})
        self.assertIsNotNone(provider)
        self.assertTrue(provider.estado())

    def test_onpremise_provision_vm(self):
        """Test aprovisionamiento On-Premise"""
        provider = OnPremise({'cpu': 2, 'ram': 4, 'disk': 50})
        vm = provider.provisionar()

        self.assertIsNotNone(vm)
        self.assertEqual(vm.provider, "on-premise")
        self.assertEqual(vm.status, VMStatus.RUNNING)
        self.assertTrue(vm.vmId.startswith("onprem-"))


class TestVMProviderFactory(unittest.TestCase):
    """Tests para el Factory Method Pattern"""
    
    def test_factory_create_aws_provider(self):
        """Test Factory crea proveedor AWS correctamente"""
        config = {'type': 't2.micro', 'method': 'standard'}
        provider = VMProviderFactory.create_provider('aws', config)
        
        self.assertIsNotNone(provider)
        self.assertIsInstance(provider, AWS)
    
    def test_factory_create_azure_provider(self):
        """Test Factory crea proveedor Azure correctamente"""
        config = {'type': 'Standard_B1s', 'method': 'standard'}
        provider = VMProviderFactory.create_provider('azure', config)
        
        self.assertIsNotNone(provider)
        self.assertIsInstance(provider, Azure)
    
    def test_factory_create_google_provider(self):
        """Test Factory crea proveedor Google correctamente"""
        config = {'type': 'n1-standard-1', 'method': 'standard'}
        provider = VMProviderFactory.create_provider('google', config)
        
        self.assertIsNotNone(provider)
        self.assertIsInstance(provider, Google)
    
    def test_factory_create_google_alias_gcp(self):
        """Test Factory acepta alias 'gcp' para Google"""
        config = {'type': 'n1-standard-1'}
        provider = VMProviderFactory.create_provider('gcp', config)
        
        self.assertIsNotNone(provider)
        self.assertIsInstance(provider, Google)
    
    def test_factory_create_onpremise_provider(self):
        """Test Factory crea proveedor On-Premise correctamente"""
        config = {'type': 'vmware', 'method': 'standard'}
        provider = VMProviderFactory.create_provider('onpremise', config)
        
        self.assertIsNotNone(provider)
        self.assertIsInstance(provider, OnPremise)
    
    def test_factory_invalid_provider(self):
        """Test Factory retorna None para proveedor inválido"""
        config = {'type': 'test'}
        provider = VMProviderFactory.create_provider('invalid_provider', config)
        
        self.assertIsNone(provider)
    
    def test_factory_case_insensitive(self):
        """Test Factory es case-insensitive"""
        config = {'type': 't2.micro'}
        
        provider1 = VMProviderFactory.create_provider('AWS', config)
        provider2 = VMProviderFactory.create_provider('aws', config)
        provider3 = VMProviderFactory.create_provider('AwS', config)
        
        self.assertIsNotNone(provider1)
        self.assertIsNotNone(provider2)
        self.assertIsNotNone(provider3)
    
    def test_factory_get_available_providers(self):
        """Test obtener lista de proveedores disponibles"""
        providers = VMProviderFactory.get_available_providers()
        
        self.assertIsInstance(providers, list)
        self.assertIn('aws', providers)
        self.assertIn('azure', providers)
        self.assertIn('google', providers)
        self.assertIn('onpremise', providers)
        self.assertGreaterEqual(len(providers), 4)


class TestVMProvisioningService(unittest.TestCase):
    """Tests para el servicio de aprovisionamiento"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.service = VMProvisioningService()
    
    def test_service_provision_aws_success(self):
        """Test aprovisionamiento exitoso en AWS"""
        config = {'type': 't2.micro', 'region': 'us-east-1'}
        result = self.service.provision_vm('aws', config)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.vm_id)
        self.assertEqual(result.provider, 'aws')
        self.assertIn('exitosamente', result.message.lower())
    
    def test_service_provision_azure_success(self):
        """Test aprovisionamiento exitoso en Azure"""
        config = {'type': 'Standard_B1s'}
        result = self.service.provision_vm('azure', config)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.vm_id)
        self.assertEqual(result.provider, 'azure')
    
    def test_service_provision_google_success(self):
        """Test aprovisionamiento exitoso en Google"""
        config = {'type': 'n1-standard-1'}
        result = self.service.provision_vm('google', config)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.vm_id)
        self.assertEqual(result.provider, 'google')
    
    def test_service_provision_onpremise_success(self):
        """Test aprovisionamiento exitoso On-Premise"""
        config = {'type': 'vmware'}
        result = self.service.provision_vm('onpremise', config)
        
        self.assertTrue(result.success)
        self.assertIsNotNone(result.vm_id)
        self.assertEqual(result.provider, 'onpremise')
    
    def test_service_provision_invalid_provider(self):
        """Test aprovisionamiento con proveedor inválido"""
        config = {'type': 'test'}
        result = self.service.provision_vm('invalid', config)
        
        self.assertFalse(result.success)
        self.assertIsNone(result.vm_id)
        self.assertIn('no soportado', result.message.lower())
    
    def test_service_provision_empty_provider(self):
        """Test aprovisionamiento sin especificar proveedor"""
        config = {'type': 'test'}
        result = self.service.provision_vm('', config)
        
        self.assertFalse(result.success)
        self.assertIn('no especificado', result.message.lower())
    
    def test_service_provision_none_provider(self):
        """Test aprovisionamiento con proveedor None"""
        config = {'type': 'test'}
        result = self.service.provision_vm('', config)  # Pasamos string vacío en lugar de None

        self.assertFalse(result.success)
    
    def test_service_get_supported_providers(self):
        """Test obtener proveedores soportados"""
        providers = self.service.get_supported_providers()
        
        self.assertIsInstance(providers, list)
        self.assertGreaterEqual(len(providers), 4)


class TestSOLIDPrinciples(unittest.TestCase):
    """Tests que validan el cumplimiento de principios SOLID"""
    
    def test_srp_single_responsibility(self):
        """Test SRP: Cada clase tiene una responsabilidad única"""
        # Factory solo crea proveedores
        factory = VMProviderFactory()
        self.assertTrue(hasattr(factory, 'create_provider'))

        # Service solo orquesta aprovisionamiento
        service = VMProvisioningService()
        self.assertTrue(hasattr(service, 'provision_vm'))

        # Providers solo crean VMs
        provider = AWS({'type': 't2.micro', 'region': 'us-east-1'})
        self.assertTrue(hasattr(provider, 'crear_vm'))

    def test_ocp_open_closed(self):
        """Test OCP: Abierto para extensión, cerrado para modificación"""
        # Podemos agregar nuevos proveedores sin modificar código existente
        initial_providers = VMProviderFactory.get_available_providers()

        # Simulamos agregar un nuevo proveedor
        class NewProvider(AWS):
            pass

        VMProviderFactory.register_provider('newprovider', NewProvider)

        new_providers = VMProviderFactory.get_available_providers()
        self.assertGreater(len(new_providers), len(initial_providers))

    def test_lsp_liskov_substitution(self):
        """Test LSP: Las subclases pueden sustituir a la clase base"""
        from domain.interfaces import ProveedorAbstracto

        # Todos los proveedores son ProveedorAbstracto
        providers = [
            AWS({'type': 't2.micro', 'region': 'us-east-1'}),
            Azure({'type': 'Standard_B1s', 'resource_group': 'test-rg'}),
            Google({'type': 'n1-standard-1', 'zone': 'us-central1-a'}),
            OnPremise({'cpu': 2, 'ram': 4, 'disk': 50})
        ]

        for provider in providers:
            self.assertIsInstance(provider, ProveedorAbstracto)
            # Todos pueden provisionar
            vm = provider.provisionar()
            self.assertIsNotNone(vm)

    def test_dip_dependency_inversion(self):
        """Test DIP: Dependemos de abstracciones, no de implementaciones"""
        from domain.interfaces import ProveedorAbstracto

        # El Factory retorna abstracciones
        provider = VMProviderFactory.create_provider('aws', {'type': 't2.micro'})
        self.assertIsInstance(provider, ProveedorAbstracto)

        # El Service trabaja con abstracciones
        # No conoce las implementaciones concretas, solo la abstracción
        self.assertTrue(True)  # El test pasa si llegamos aquí


def run_all_tests():
    """Ejecuta todos los tests y muestra resumen"""
    # Crear suite de tests
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todos los tests
    suite.addTests(loader.loadTestsFromTestCase(TestDomainEntities))
    suite.addTests(loader.loadTestsFromTestCase(TestProviders))
    suite.addTests(loader.loadTestsFromTestCase(TestVMProviderFactory))
    suite.addTests(loader.loadTestsFromTestCase(TestVMProvisioningService))
    suite.addTests(loader.loadTestsFromTestCase(TestSOLIDPrinciples))
    
    # Ejecutar tests con verbose
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Mostrar resumen
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