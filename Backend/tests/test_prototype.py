import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from datetime import datetime
from domain.entities import MachineVirtual, Network, StorageDisk, VMStatus
from domain.prototype_registry import VMPrototypeRegistry
from application.clone_service import VMCloneService


class TestPrototypePattern(unittest.TestCase):
    
    def setUp(self):
        
        self.registry = VMPrototypeRegistry()
        self.clone_service = VMCloneService()

    def test_registry_is_singleton(self):
        
        registry1 = VMPrototypeRegistry()
        registry2 = VMPrototypeRegistry()

        self.assertIs(registry1, registry2, "El registro debe ser Singleton")

    def test_default_prototypes_loaded(self):
        
        prototypes = self.registry.list_prototypes()

        self.assertGreater(len(prototypes), 0, "Debe haber prototipos predefinidos")

        
        prototype_names = [p['name'] for p in prototypes]
        self.assertIn('aws-web-server', prototype_names)
        self.assertIn('azure-database', prototype_names)
        self.assertIn('gcp-data-processing', prototype_names)
        self.assertIn('onpremise-dev', prototype_names)

    def test_clone_vm_basic(self):
        
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

        
        cloned_vm = original_vm.clone(new_name="cloned-server")

        
        self.assertNotEqual(original_vm.vmId, cloned_vm.vmId, "IDs deben ser diferentes")
        self.assertEqual(cloned_vm.name, "cloned-server", "Nombre debe ser el especificado")
        self.assertEqual(cloned_vm.vcpus, original_vm.vcpus, "vCPUs deben ser iguales")
        self.assertEqual(cloned_vm.memoryGB, original_vm.memoryGB, "Memoria debe ser igual")
        self.assertEqual(cloned_vm.provider, original_vm.provider, "Proveedor debe ser igual")
        self.assertEqual(cloned_vm.status, VMStatus.PENDING, "Status debe resetearse a PENDING")

    def test_clone_vm_with_customizations(self):
        
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

       
        cloned_vm = original_vm.clone(
            new_name="custom-cloned-server",
            vcpus=4,
            memoryGB=16
        )

        
        self.assertEqual(cloned_vm.vcpus, 4, "vCPUs deben cambiar a 4")
        self.assertEqual(cloned_vm.memoryGB, 16, "Memoria debe cambiar a 16GB")
        self.assertEqual(cloned_vm.name, "custom-cloned-server")

    def test_clone_vm_with_network(self):
        
        network = Network(
            networkId="net-original",
            name="original-network",
            cidr_block="10.0.0.0/16",
            provider="aws",
            region="us-east-1",
            firewallRules=["allow-ssh"],
            publicIP=True
        )

        
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

        
        cloned_vm = original_vm.clone(new_name="cloned-with-network")

        
        self.assertIsNotNone(cloned_vm.network, "Red debe clonarse")
        assert cloned_vm.network is not None  
        self.assertNotEqual(cloned_vm.network.networkId, network.networkId, "ID de red debe ser diferente")
        self.assertEqual(cloned_vm.network.cidr_block, network.cidr_block, "CIDR debe ser igual")
        self.assertEqual(cloned_vm.network.region, network.region, "Región debe ser igual")

    def test_clone_vm_with_disks(self):
       
        disk = StorageDisk(
            diskId="disk-original",
            name="original-disk",
            size_gb=100,
            disk_type="gp3",
            provider="aws",
            region="us-east-1",
            iops=3000
        )

        
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

        
        cloned_vm = original_vm.clone(new_name="cloned-with-disk")

        
        self.assertIsNotNone(cloned_vm.disks, "Discos deben clonarse")
        assert cloned_vm.disks is not None  
        self.assertEqual(len(cloned_vm.disks), 1, "Debe haber 1 disco")
        self.assertNotEqual(cloned_vm.disks[0].diskId, disk.diskId, "ID de disco debe ser diferente")
        self.assertEqual(cloned_vm.disks[0].size_gb, disk.size_gb, "Tamaño debe ser igual")
        self.assertEqual(cloned_vm.disks[0].disk_type, disk.disk_type, "Tipo debe ser igual")

    def test_clone_with_region_change(self):
        
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

        
        cloned_vm = original_vm.clone(new_name="server-west", region="us-west-2")

        
        assert cloned_vm.network is not None  # Para type checker
        assert cloned_vm.disks is not None  # Para type checker
        self.assertEqual(cloned_vm.network.region, "us-west-2", "Región de red debe cambiar")
        self.assertEqual(cloned_vm.disks[0].region, "us-west-2", "Región de disco debe cambiar")

    def test_clone_from_prototype_success(self):
        
        result = self.clone_service.clone_from_prototype(
            prototype_name="aws-web-server",
            new_vm_name="production-web-server"
        )

        
        self.assertTrue(result.success, "Clonación debe ser exitosa")
        self.assertIsNotNone(result.vm_id, "Debe tener VM ID")
        self.assertEqual(result.provider, "aws", "Proveedor debe ser AWS")
        self.assertIn("production-web-server", result.message)

    def test_clone_from_prototype_with_customizations(self):
        
        result = self.clone_service.clone_from_prototype(
            prototype_name="azure-database",
            new_vm_name="custom-database",
            customizations={
                "vcpus": 8,
                "memoryGB": 64
            }
        )

        
        self.assertTrue(result.success, "Clonación debe ser exitosa")
        assert result.vm_details is not None  
        vm_details = result.vm_details
        self.assertEqual(vm_details['vcpus'], 8, "vCPUs deben ser 8")
        self.assertEqual(vm_details['memoryGB'], 64, "Memoria debe ser 64GB")

    def test_clone_from_nonexistent_prototype(self):
        
        result = self.clone_service.clone_from_prototype(
            prototype_name="nonexistent-prototype",
            new_vm_name="should-fail"
        )

        
        self.assertFalse(result.success, "Debe fallar")
        self.assertIn("no encontrado", result.message.lower())

    def test_list_prototypes(self):

        result = self.clone_service.list_available_prototypes()

        
        self.assertTrue(result['success'])
        self.assertGreater(result['count'], 0)
        self.assertIsInstance(result['prototypes'], list)

        
        for proto in result['prototypes']:
            self.assertIn('name', proto)
            self.assertIn('provider', proto)
            self.assertIn('vcpus', proto)
            self.assertIn('memoryGB', proto)
            self.assertIn('description', proto)

    def test_get_prototype_details(self):
        
        result = self.clone_service.get_prototype_details("aws-web-server")

        
        self.assertTrue(result['success'])
        self.assertIn('prototype', result)

        prototype = result['prototype']
        self.assertEqual(prototype['provider'], 'aws')
        self.assertIn('vcpus', prototype)
        self.assertIn('memoryGB', prototype)
        self.assertIn('network', prototype)
        self.assertIn('disks', prototype)

    def test_network_clone_method(self):
        
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

        
        self.assertNotEqual(cloned_network.networkId, original_network.networkId)
        self.assertEqual(cloned_network.name, "cloned-network")
        self.assertEqual(cloned_network.cidr_block, original_network.cidr_block)
        self.assertEqual(cloned_network.provider, original_network.provider)
        self.assertEqual(cloned_network.region, original_network.region)
        self.assertEqual(cloned_network.firewallRules, original_network.firewallRules)

    def test_disk_clone_method(self):
        
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

        
        self.assertNotEqual(cloned_disk.diskId, original_disk.diskId)
        self.assertEqual(cloned_disk.name, "cloned-disk")
        self.assertEqual(cloned_disk.size_gb, 200, "Tamaño debe cambiar a 200GB")
        self.assertEqual(cloned_disk.disk_type, original_disk.disk_type)
        self.assertEqual(cloned_disk.iops, original_disk.iops)

    def test_region_consistency_validation(self):
        
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
            region="us-west-2"  
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

       
        result = self.clone_service.clone_existing_vm(
            source_vm=vm,
            new_vm_name="should-fail-consistency"
        )

        
        self.assertFalse(result.success, "Debe fallar por inconsistencia de región")
        self.assertIn("región", result.message.lower())


def run_tests():
    
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
