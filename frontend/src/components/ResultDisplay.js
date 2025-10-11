import React from 'react';
import './ResultDisplay.css';
import { format } from 'date-fns';

const getProviderIcon = (provider) => {
    switch (provider?.toLowerCase()) {
        case 'aws':
            return 'https://img.icons8.com/color/48/amazon-web-services.png';
        case 'azure':
            return 'https://img.icons8.com/color/48/azure-1.png';
        case 'google':
        case 'gcp':
            return 'https://img.icons8.com/color/48/google-cloud.png';
        case 'onpremise':
        case 'on-premise':
            return 'https://img.icons8.com/fluency/48/server.png';
        default:
            return 'https://img.icons8.com/fluency/48/cloud.png';
    }
};

const ResultDisplay = ({ result }) => {
    if (!result) return null;

    // Manejo de errores desde la API
    if (!result.success) {
        return (
            <div className="result-card-container error">
                <h3>❌ Error en la Operación</h3>
                <p>{result.message || result.error || 'Ocurrió un error desconocido.'}</p>
                {result.error_detail && <p><strong>Detalle:</strong> {result.error_detail}</p>}
            </div>
        );
    }

    const vm = result.vm_details;
    if (!vm) return null;

    // El backend devuelve a veces 'disks' y a veces 'storage'
    const disks = vm.disks || vm.storage || [];
    const disk = disks.length > 0 ? disks[0] : null;
    const compute = vm.compute || {};
    const instanceType = vm.type || vm.instance_type || vm.vm_type;

    return (
        <div className="result-card-container success">
            <h3>✅ {result.message || 'Operación completada con éxito'}</h3>
            <div className="vm-card">
                <div className="vm-card-header">
                    <img src={getProviderIcon(vm.provider)} alt={vm.provider} />
                    <h4>{vm.name}</h4>
                </div>
                <div className="vm-card-body">
                    <div className="vm-detail">
                        <span>ID de VM</span>
                        <strong>{vm.vmId}</strong>
                    </div>
                    <div className="vm-detail">
                        <span>Estado</span>
                        <strong className={`status status-${vm.status?.toLowerCase()}`}>{vm.status || 'Desconocido'}</strong>
                    </div>
                    {instanceType && (
                        <div className="vm-detail">
                            <span>Tipo de Instancia</span>
                            <strong>{instanceType}</strong>
                        </div>
                    )}
                    {(compute.cpu || compute.ram) && (
                         <div className="vm-detail">
                            <span>Cómputo</span>
                            <strong>{compute.cpu} vCPUs / {compute.ram} GB RAM</strong>
                        </div>
                    )}
                    <div className="vm-detail">
                        <span>Proveedor</span>
                        <strong>{vm.provider?.toUpperCase()}</strong>
                    </div>
                    <div className="vm-detail">
                        <span>Ubicación</span>
                        <strong>{vm.location || vm.region || 'N/A'}</strong>
                    </div>
                    <div className="vm-detail">
                        <span>Red</span>
                        <strong>{vm.network?.name || 'N/A'} ({vm.network?.networkId || 'N/A'})</strong>
                    </div>
                    <div className="vm-detail">
                        <span>Fecha de Creación</span>
                        <strong>{vm.createdAt ? format(new Date(vm.createdAt), 'dd/MM/yyyy HH:mm:ss') : 'N/A'}</strong>
                    </div>
                    {disk && (
                        <>
                            <div className="vm-detail">
                                <span>Almacenamiento</span>
                                <strong>{disk.size_gb || disk.size} GB ({disk.disk_type || disk.type})</strong>
                            </div>
                        </>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ResultDisplay;