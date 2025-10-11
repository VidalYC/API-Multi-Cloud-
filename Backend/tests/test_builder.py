"""
Test Suite para Builder Pattern
Tests para validar la implementación del patrón Builder
"""
import unittest
import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from domain.builder import VMBuilder, VMDirector
from domain.entities import MachineVirtual, VMStatus
from infrastructure.builders import AWSVMBuilder, AzureVMBuilder, GoogleVMBuilder, OnPremiseVMBuilder
from application.factory import VMBuilderFactory, VMBuildingService


class TestVMBuilders(unittest.TestCase):
    """Tests para los builders concretos"""

    def test_aws_builder_basic(self):
        """Test construcción básica con AWS Builder"""
        builder = AWSVMBuilder()

        vm = (builder
              .reset()
              .set_basic_config("test-vm", "standard")
              .set_compute_resources(cpu=2, ram=4)
              .set_storage(size_gb=50)
              .build())

        self.assertIsNotNone(vm)
        self.assertIsInstance(vm, MachineVirtual)
        self.assertEqual(vm.status, VMStatus.RUNNING)
        self.assertEqual(vm.provider, 'aws')
        self.assertIsNotNone(vm.network)
        self.assertIsNotNone(vm.disks)
        self.assertGreater(len(vm.disks), 0)

    def test_azure_builder_basic(self):
        """Test construcción básica con Azure Builder"""
        builder = AzureVMBuilder()

        vm = (builder
              .reset()
              .set_basic_config("test-vm", "standard")
              .set_compute_resources(cpu=2, ram=4)
              .set_storage(size_gb=50)
              .build())

        self.assertIsNotNone(vm)
        self.assertEqual(vm.provider, 'azure')
        self.assertEqual(vm.status, VMStatus.RUNNING)

    def test_google_builder_basic(self):
        """Test construcción básica con Google Builder"""
        builder = GoogleVMBuilder()

        vm = (builder
              .reset()
              .set_basic_config("test-vm", "standard")
              .set_compute_resources(cpu=2, ram=4)
              .set_storage(size_gb=50)
              .build())

        self.assertIsNotNone(vm)
        self.assertEqual(vm.provider, 'google')
        self.assertEqual(vm.status, VMStatus.RUNNING)

    def test_onpremise_builder_basic(self):
        """Test construcción básica con OnPremise Builder"""
        builder = OnPremiseVMBuilder()

        vm = (builder
              .reset()
              .set_basic_config("test-vm", "standard")
              .set_compute_resources(cpu=2, ram=4)
              .set_storage(size_gb=50)
              .build())

        self.assertIsNotNone(vm)
        self.assertEqual(vm.provider, 'on-premise')
        self.assertEqual(vm.status, VMStatus.RUNNING)

    def test_aws_builder_full_config(self):
        """Test construcción completa con todas las opciones"""
        builder = AWSVMBuilder()

        vm = (builder
              .reset()
              .set_basic_config("production-vm", "high-performance")
              .set_compute_resources(cpu=8, ram=32)
              .set_storage(size_gb=500, disk_type="ssd")
              .set_network(network_id="vpc-custom", cidr="10.5.0.0/16")
              .set_location("us-west-2")
              .set_advanced_options({"monitoring": True, "optimized": True})
              .build())

        self.assertIsNotNone(vm)
        self.assertEqual(vm.provider, 'aws')
        self.assertIsNotNone(vm.network)
        self.assertEqual(vm.network.cidr_block, "10.5.0.0/16")
        self.assertGreater(vm.disks[0].size_gb, 100)

    def test_builder_fluent_interface(self):
        """Test que el builder retorna self para encadenar llamadas"""
        builder = AWSVMBuilder()

        result1 = builder.reset()
        self.assertIsInstance(result1, AWSVMBuilder)

        result2 = builder.set_basic_config("test", "standard")
        self.assertIsInstance(result2, AWSVMBuilder)

        result3 = builder.set_compute_resources(cpu=2, ram=4)
        self.assertIsInstance(result3, AWSVMBuilder)

    def test_builder_reset(self):
        """Test que reset reinicia el builder correctamente"""
        builder = AWSVMBuilder()

        # Primera construcción
        vm1 = (builder
               .set_basic_config("vm1", "standard")
               .set_compute_resources(cpu=2, ram=4)
               .build())

        # Reset y segunda construcción
        vm2 = (builder
               .reset()
               .set_basic_config("vm2", "minimal")
               .set_compute_resources(cpu=1, ram=1)
               .build())

        self.assertNotEqual(vm1.vmId, vm2.vmId)
        self.assertNotEqual(vm1.name, vm2.name)


class TestVMDirector(unittest.TestCase):
    """Tests para el Director"""

    def test_director_minimal_vm(self):
        """Test construcción de VM mínima con Director"""
        builder = AWSVMBuilder()
        director = VMDirector(builder)

        vm = director.build_minimal_vm("test-minimal")

        self.assertIsNotNone(vm)
        self.assertEqual(vm.status, VMStatus.RUNNING)
        self.assertEqual(vm.provider, 'aws')

    def test_director_standard_vm(self):
        """Test construcción de VM estándar con Director"""
        builder = AWSVMBuilder()
        director = VMDirector(builder)

        vm = director.build_standard_vm("test-standard", "us-east-1")

        self.assertIsNotNone(vm)
        self.assertEqual(vm.status, VMStatus.RUNNING)

    def test_director_high_performance_vm(self):
        """Test construcción de VM de alto rendimiento con Director"""
        builder = AWSVMBuilder()
        director = VMDirector(builder)

        vm = director.build_high_performance_vm("test-hp", "us-east-1")

        self.assertIsNotNone(vm)
        self.assertEqual(vm.status, VMStatus.RUNNING)
        self.assertIsNotNone(vm.network)
        self.assertIsNotNone(vm.disks)

    def test_director_custom_vm(self):
        """Test construcción de VM personalizada con Director"""
        builder = AWSVMBuilder()
        director = VMDirector(builder)

        vm = director.build_custom_vm("test-custom", cpu=4, ram=8, disk_gb=200, location="us-west-2")

        self.assertIsNotNone(vm)
        self.assertEqual(vm.status, VMStatus.RUNNING)

    def test_director_change_builder(self):
        """Test cambio de builder en el Director"""
        aws_builder = AWSVMBuilder()
        azure_builder = AzureVMBuilder()
        director = VMDirector(aws_builder)

        vm1 = director.build_minimal_vm("test1")
        self.assertEqual(vm1.provider, 'aws')

        director.change_builder(azure_builder)
        vm2 = director.build_minimal_vm("test2")
        self.assertEqual(vm2.provider, 'azure')

    def test_director_with_different_providers(self):
        """Test Director con diferentes proveedores"""
        builders = [
            AWSVMBuilder(),
            AzureVMBuilder(),
            GoogleVMBuilder(),
            OnPremiseVMBuilder()
        ]

        expected_providers = ['aws', 'azure', 'google', 'on-premise']

        for builder, expected_provider in zip(builders, expected_providers):
            director = VMDirector(builder)
            vm = director.build_standard_vm("test-vm", "test-location")
            self.assertEqual(vm.provider, expected_provider)


class TestVMBuilderFactory(unittest.TestCase):
    """Tests para el VMBuilderFactory"""

    def test_create_aws_builder(self):
        """Test creación de AWS Builder"""
        builder = VMBuilderFactory.create_builder('aws')

        self.assertIsNotNone(builder)
        self.assertIsInstance(builder, AWSVMBuilder)

    def test_create_azure_builder(self):
        """Test creación de Azure Builder"""
        builder = VMBuilderFactory.create_builder('azure')

        self.assertIsNotNone(builder)
        self.assertIsInstance(builder, AzureVMBuilder)

    def test_create_google_builder(self):
        """Test creación de Google Builder"""
        builder = VMBuilderFactory.create_builder('google')

        self.assertIsNotNone(builder)
        self.assertIsInstance(builder, GoogleVMBuilder)

    def test_create_google_alias_gcp(self):
        """Test alias 'gcp' para Google Builder"""
        builder = VMBuilderFactory.create_builder('gcp')

        self.assertIsNotNone(builder)
        self.assertIsInstance(builder, GoogleVMBuilder)

    def test_create_onpremise_builder(self):
        """Test creación de OnPremise Builder"""
        builder = VMBuilderFactory.create_builder('onpremise')

        self.assertIsNotNone(builder)
        self.assertIsInstance(builder, OnPremiseVMBuilder)

    def test_create_invalid_builder(self):
        """Test creación de builder inválido"""
        builder = VMBuilderFactory.create_builder('invalid')

        self.assertIsNone(builder)

    def test_case_insensitive(self):
        """Test que el factory es case-insensitive"""
        builder1 = VMBuilderFactory.create_builder('AWS')
        builder2 = VMBuilderFactory.create_builder('aws')
        builder3 = VMBuilderFactory.create_builder('AwS')

        self.assertIsNotNone(builder1)
        self.assertIsNotNone(builder2)
        self.assertIsNotNone(builder3)

    def test_get_available_builders(self):
        """Test obtener lista de builders disponibles"""
        builders = VMBuilderFactory.get_available_builders()

        self.assertIsInstance(builders, list)
        self.assertIn('aws', builders)
        self.assertIn('azure', builders)
        self.assertIn('google', builders)
        self.assertIn('onpremise', builders)


class TestVMBuildingService(unittest.TestCase):
    """Tests para el servicio de construcción"""

    def setUp(self):
        """Configuración inicial"""
        self.service = VMBuildingService()

    def test_build_vm_with_config_aws(self):
        """Test construcción con configuración personalizada en AWS"""
        build_config = {
            'name': 'test-vm',
            'vm_type': 'standard',
            'cpu': 4,
            'ram': 16,
            'disk_gb': 100,
            'disk_type': 'ssd',
            'location': 'us-east-1'
        }

        result = self.service.build_vm_with_config('aws', build_config)

        self.assertTrue(result.success)
        self.assertIsNotNone(result.vm_id)
        self.assertEqual(result.provider, 'aws')
        self.assertIn('Builder Pattern', result.message)

    def test_build_vm_with_config_azure(self):
        """Test construcción con configuración personalizada en Azure"""
        build_config = {
            'name': 'azure-test',
            'vm_type': 'standard',
            'cpu': 2,
            'ram': 8,
            'disk_gb': 50
        }

        result = self.service.build_vm_with_config('azure', build_config)

        self.assertTrue(result.success)
        self.assertEqual(result.provider, 'azure')

    def test_build_vm_invalid_provider(self):
        """Test construcción con proveedor inválido"""
        build_config = {
            'name': 'test',
            'vm_type': 'standard',
            'cpu': 2,
            'ram': 4,
            'disk_gb': 50
        }

        result = self.service.build_vm_with_config('invalid', build_config)

        self.assertFalse(result.success)
        self.assertIn('no soportado', result.message.lower())

    def test_build_predefined_minimal(self):
        """Test construcción de VM minimal predefinida"""
        result = self.service.build_predefined_vm('aws', 'minimal', 'test-minimal')

        self.assertTrue(result.success)
        self.assertIsNotNone(result.vm_id)
        self.assertIn('minimal', result.message.lower())

    def test_build_predefined_standard(self):
        """Test construcción de VM standard predefinida"""
        result = self.service.build_predefined_vm('azure', 'standard', 'test-standard', 'eastus')

        self.assertTrue(result.success)
        self.assertIsNotNone(result.vm_id)

    def test_build_predefined_high_performance(self):
        """Test construcción de VM high-performance predefinida"""
        result = self.service.build_predefined_vm('google', 'high-performance', 'test-hp', 'us-central1-a')

        self.assertTrue(result.success)
        self.assertIsNotNone(result.vm_id)

    def test_build_predefined_invalid_preset(self):
        """Test construcción con preset inválido"""
        result = self.service.build_predefined_vm('aws', 'invalid-preset', 'test')

        self.assertFalse(result.success)
        self.assertIn('no soportado', result.message.lower())

    def test_build_all_providers(self):
        """Test construcción en todos los proveedores"""
        providers = ['aws', 'azure', 'google', 'onpremise']

        for provider in providers:
            result = self.service.build_predefined_vm(provider, 'standard', f'test-{provider}', 'test-location')
            self.assertTrue(result.success, f"Failed for provider: {provider}")


class TestBuilderPattern(unittest.TestCase):
    """Tests que validan el cumplimiento del patrón Builder"""

    def test_builder_encapsulates_construction(self):
        """Test que el Builder encapsula la construcción compleja"""
        builder = AWSVMBuilder()

        # Sin builder, sería necesario crear manualmente Network, Disk, VM
        # Con builder, todo está encapsulado
        vm = builder.set_basic_config("test", "standard").build()

        self.assertIsNotNone(vm)
        self.assertIsNotNone(vm.network)
        self.assertIsNotNone(vm.disks)

    def test_builder_allows_step_by_step_construction(self):
        """Test que el Builder permite construcción paso a paso"""
        builder = AWSVMBuilder()

        # Cada paso es independiente y se puede ejecutar en el orden deseado
        builder.reset()
        builder.set_basic_config("test", "standard")
        builder.set_storage(100)
        builder.set_compute_resources(cpu=4, ram=16)
        builder.set_network()
        vm = builder.build()

        self.assertIsNotNone(vm)

    def test_director_encapsulates_construction_algorithm(self):
        """Test que el Director encapsula algoritmos de construcción"""
        builder = AWSVMBuilder()
        director = VMDirector(builder)

        # El Director sabe cómo construir diferentes tipos de VMs
        vm1 = director.build_minimal_vm("test1")
        vm2 = director.build_standard_vm("test2", "us-east-1")
        vm3 = director.build_high_performance_vm("test3", "us-east-1")

        self.assertIsNotNone(vm1)
        self.assertIsNotNone(vm2)
        self.assertIsNotNone(vm3)


def run_builder_tests():
    """Ejecuta todos los tests de Builder"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Agregar tests
    suite.addTests(loader.loadTestsFromTestCase(TestVMBuilders))
    suite.addTests(loader.loadTestsFromTestCase(TestVMDirector))
    suite.addTests(loader.loadTestsFromTestCase(TestVMBuilderFactory))
    suite.addTests(loader.loadTestsFromTestCase(TestVMBuildingService))
    suite.addTests(loader.loadTestsFromTestCase(TestBuilderPattern))

    # Ejecutar tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Resumen
    print("\n" + "="*70)
    print("RESUMEN DE TESTS DE BUILDER PATTERN")
    print("="*70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallidos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("="*70)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_builder_tests()
    sys.exit(0 if success else 1)
