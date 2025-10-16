"""
Tests para el Patrón Prototype
Valida la funcionalidad de clonación de VMs y gestión de prototipos
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from datetime import datetime
from domain.entities import MachineVirtual, Network, StorageDisk, VMStatus
from domain.prototype_registry import VMPrototypeRegistry
from application.clone_service import VMCloneService


class TestPrototypePattern(unittest.TestCase):
    """Tests para el patrón Prototype"""

    def setUp(self):
        """Configuración inicial para cada test"""
        self.registry = VMPrototypeRegistry()
        self.clone_service = VMCloneService()

    def test_registry_is_singleton(self):
        """Test: El registro es Singleton (única instancia)"""
        registry1 = VMPrototypeRegistry()
        registry2 = VMPrototypeRegistry()

        self.assertIs(registry1, registry2, "El registro debe ser Singleton")

    def test_default_prototypes_loaded(self):
        """Test: Los prototipos predefinidos se cargan al inicializar"""
        prototypes = self.registry.list_prototypes()

        self.assertGreater(len(prototypes), 0, "Debe haber prototipos predefinidos")

        # Verificar que existen los 4 prototipos predefinidos
        prototype_names = [p['name'] for p in prototypes]
        self.assertIn('aws-web-server', prototype_names)
        self.assertIn('azure-database', prototype_names)
        self.assertIn('gcp-data-processing', prototype_names)
        self.assertIn('onpremise-dev', prototype_names)

    def test_clone_vm_basic(self):
        """Test: Clonar VM básica genera nueva instancia con ID diferente"""
        # Crear VM original
        original_vm = MachineVirtual(
            vmId="original-vm-123",
            name="original-server",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="aws",
            vcpus=2,
            memoryGB=4,
            instance_type="t3.medium"
        )

        # Clonar VM
        cloned_vm = original_vm.clone(new_name="cloned-server")

        # Verificaciones
        self.assertNotEqual(original_vm.vmId, cloned_vm.vmId, "IDs deben ser diferentes")
        self.assertEqual(cloned_vm.name, "cloned-server", "Nombre debe ser el especificado")
        self.assertEqual(cloned_vm.vcpus, original_vm.vcpus, "vCPUs deben ser iguales")
        self.assertEqual(cloned_vm.memoryGB, original_vm.memoryGB, "Memoria debe ser igual")
        self.assertEqual(cloned_vm.provider, original_vm.provider, "Proveedor debe ser igual")
        self.assertEqual(cloned_vm.status, VMStatus.PENDING, "Status debe resetearse a PENDING")

    def test_clone_vm_with_customizations(self):
        """Test: Clonar VM con customizaciones aplica los cambios"""
        # Crear VM original
        original_vm = MachineVirtual(
            vmId="original-vm-456",
            name="original-server",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="azure",
            vcpus=2,
            memoryGB=8,
            instance_type="D2s_v3"
        )

        # Clonar con customizaciones
        cloned_vm = original_vm.clone(
            new_name="custom-cloned-server",
            vcpus=4,
            memoryGB=16
        )

        # Verificaciones
        self.assertEqual(cloned_vm.vcpus, 4, "vCPUs deben cambiar a 4")
        self.assertEqual(cloned_vm.memoryGB, 16, "Memoria debe cambiar a 16GB")
        self.assertEqual(cloned_vm.name, "custom-cloned-server")

    def test_clone_vm_with_network(self):
        """Test: Clonar VM con red clona también la red"""
        # Crear red
        network = Network(
            networkId="net-original",
            name="original-network",
            cidr_block="10.0.0.0/16",
            provider="aws",
            region="us-east-1",
            firewallRules=["allow-ssh"],
            publicIP=True
        )

        # Crear VM con red
        original_vm = MachineVirtual(
            vmId="vm-with-net",
            name="server-with-network",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="aws",
            vcpus=2,
            memoryGB=4,
            network=network
        )

        # Clonar VM
        cloned_vm = original_vm.clone(new_name="cloned-with-network")

        # Verificaciones
        self.assertIsNotNone(cloned_vm.network, "Red debe clonarse")
        self.assertNotEqual(cloned_vm.network.networkId, network.networkId, "ID de red debe ser diferente")
        self.assertEqual(cloned_vm.network.cidr_block, network.cidr_block, "CIDR debe ser igual")
        self.assertEqual(cloned_vm.network.region, network.region, "Región debe ser igual")

    def test_clone_vm_with_disks(self):
        """Test: Clonar VM con discos clona también los discos"""
        # Crear disco
        disk = StorageDisk(
            diskId="disk-original",
            name="original-disk",
            size_gb=100,
            disk_type="gp3",
            provider="aws",
            region="us-east-1",
            iops=3000
        )

        # Crear VM con disco
        original_vm = MachineVirtual(
            vmId="vm-with-disk",
            name="server-with-disk",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="aws",
            vcpus=2,
            memoryGB=4,
            disks=[disk]
        )

        # Clonar VM
        cloned_vm = original_vm.clone(new_name="cloned-with-disk")

        # Verificaciones
        self.assertIsNotNone(cloned_vm.disks, "Discos deben clonarse")
        self.assertEqual(len(cloned_vm.disks), 1, "Debe haber 1 disco")
        self.assertNotEqual(cloned_vm.disks[0].diskId, disk.diskId, "ID de disco debe ser diferente")
        self.assertEqual(cloned_vm.disks[0].size_gb, disk.size_gb, "Tamaño debe ser igual")
        self.assertEqual(cloned_vm.disks[0].disk_type, disk.disk_type, "Tipo debe ser igual")

    def test_clone_with_region_change(self):
        """Test: Cambiar región al clonar actualiza red y discos"""
        # Crear red y disco
        network = Network(
            networkId="net-1",
            name="network-1",
            cidr_block="10.0.0.0/16",
            provider="aws",
            region="us-east-1",
            publicIP=True
        )
        disk = StorageDisk(
            diskId="disk-1",
            name="disk-1",
            size_gb=50,
            disk_type="gp3",
            provider="aws",
            region="us-east-1"
        )

        # Crear VM
        original_vm = MachineVirtual(
            vmId="vm-1",
            name="server-1",
            status=VMStatus.RUNNING,
            createdAt=datetime.now(),
            provider="aws",
            vcpus=2,
            memoryGB=4,
            network=network,
            disks=[disk]
        )

        # Clonar con cambio de región
        cloned_vm = original_vm.clone(new_name="server-west", region="us-west-2")

        # Verificaciones
        self.assertEqual(cloned_vm.network.region, "us-west-2", "Región de red debe cambiar")
        self.assertEqual(cloned_vm.disks[0].region, "us-west-2", "Región de disco debe cambiar")

    def test_clone_from_prototype_success(self):
        """Test: Clonar desde prototipo del registro funciona correctamente"""
        result = self.clone_service.clone_from_prototype(
            prototype_name="aws-web-server",
            new_vm_name="production-web-server"
        )

        # Verificaciones
        self.assertTrue(result.success, "Clonación debe ser exitosa")
        self.assertIsNotNone(result.vm_id, "Debe tener VM ID")
        self.assertEqual(result.provider, "aws", "Proveedor debe ser AWS")
        self.assertIn("production-web-server", result.message)

    def test_clone_from_prototype_with_customizations(self):
        """Test: Clonar prototipo con customizaciones aplica los cambios"""
        result = self.clone_service.clone_from_prototype(
            prototype_name="azure-database",
            new_vm_name="custom-database",
            customizations={
                "vcpus": 8,
                "memoryGB": 64
            }
        )

        # Verificaciones
        self.assertTrue(result.success, "Clonación debe ser exitosa")
        vm_details = result.vm_details
        self.assertEqual(vm_details['vcpus'], 8, "vCPUs deben ser 8")
        self.assertEqual(vm_details['memoryGB'], 64, "Memoria debe ser 64GB")

    def test_clone_from_nonexistent_prototype(self):
        """Test: Clonar desde prototipo inexistente falla apropiadamente"""
        result = self.clone_service.clone_from_prototype(
            prototype_name="nonexistent-prototype",
            new_vm_name="should-fail"
        )

        # Verificaciones
        self.assertFalse(result.success, "Debe fallar")
        self.assertIn("no encontrado", result.message.lower())

    def test_list_prototypes(self):
        """Test: Listar prototipos retorna información correcta"""
        result = self.clone_service.list_available_prototypes()

        # Verificaciones
        self.assertTrue(result['success'])
        self.assertGreater(result['count'], 0)
        self.assertIsInstance(result['prototypes'], list)

        # Verificar estructura de cada prototipo
        for proto in result['prototypes']:
            self.assertIn('name', proto)
            self.assertIn('provider', proto)
            self.assertIn('vcpus', proto)
            self.assertIn('memoryGB', proto)
            self.assertIn('description', proto)

    def test_get_prototype_details(self):
        """Test: Obtener detalles de prototipo específico"""
        result = self.clone_service.get_prototype_details("aws-web-server")

        # Verificaciones
        self.assertTrue(result['success'])
        self.assertIn('prototype', result)

        prototype = result['prototype']
        self.assertEqual(prototype['provider'], 'aws')
        self.assertIn('vcpus', prototype)
        self.assertIn('memoryGB', prototype)
        self.assertIn('network', prototype)
        self.assertIn('disks', prototype)

    def test_network_clone_method(self):
        """Test: Método clone() de Network funciona correctamente"""
        original_network = Network(
            networkId="net-original",
            name="original-network",
            cidr_block="10.0.0.0/16",
            provider="google",
            region="us-central1",
            firewallRules=["allow-http"],
            publicIP=True
        )

        cloned_network = original_network.clone(new_name="cloned-network")

        # Verificaciones
        self.assertNotEqual(cloned_network.networkId, original_network.networkId)
        self.assertEqual(cloned_network.name, "cloned-network")
        self.assertEqual(cloned_network.cidr_block, original_network.cidr_block)
        self.assertEqual(cloned_network.provider, original_network.provider)
        self.assertEqual(cloned_network.region, original_network.region)
        self.assertEqual(cloned_network.firewallRules, original_network.firewallRules)

    def test_disk_clone_method(self):
        """Test: Método clone() de StorageDisk funciona correctamente"""
        original_disk = StorageDisk(
            diskId="disk-original",
            name="original-disk",
            size_gb=100,
            disk_type="Premium_LRS",
            provider="azure",
            region="eastus",
            iops=5000
        )

        cloned_disk = original_disk.clone(new_name="cloned-disk", new_size=200)

        # Verificaciones
        self.assertNotEqual(cloned_disk.diskId, original_disk.diskId)
        self.assertEqual(cloned_disk.name, "cloned-disk")
        self.assertEqual(cloned_disk.size_gb, 200, "Tamaño debe cambiar a 200GB")
        self.assertEqual(cloned_disk.disk_type, original_disk.disk_type)
        self.assertEqual(cloned_disk.iops, original_disk.iops)

    def test_region_consistency_validation(self):
        """Test: Validación de consistencia de región (RNF1)"""
        # Crear VM con red y disco en regiones diferentes (debería fallar)
        network = Network(
            networkId="net-1",
            name="network-1",
            cidr_block="10.0.0.0/16",
            provider="aws",
            region="us-east-1",
            publicIP=True
        )
        disk = StorageDisk(
            diskId="disk-1",
            name="disk-1",
            size_gb=50,
            disk_type="gp3",
            provider="aws",
            region="us-west-2"  # Región diferente
        )

        vm = MachineVirtual(
            vmId="vm-inconsistent",
            name="inconsistent-vm",
            status=VMStatus.PENDING,
            createdAt=datetime.now(),
            provider="aws",
            vcpus=2,
            memoryGB=4,
            network=network,
            disks=[disk]
        )

        # Intentar clonar (el servicio debe validar consistencia)
        result = self.clone_service.clone_existing_vm(
            source_vm=vm,
            new_vm_name="should-fail-consistency"
        )

        # Verificaciones
        self.assertFalse(result.success, "Debe fallar por inconsistencia de región")
        self.assertIn("región", result.message.lower())


def run_tests():
    """Ejecuta los tests y muestra resultados"""
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPrototypePattern)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "="*70)
    print("RESUMEN DE TESTS DEL PATRÓN PROTOTYPE")
    print("="*70)
    print(f"Tests ejecutados: {result.testsRun}")
    print(f"Exitosos: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Fallidos: {len(result.failures)}")
    print(f"Errores: {len(result.errors)}")
    print("="*70)

    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
