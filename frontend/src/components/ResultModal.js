import React from 'react';
import { motion } from 'framer-motion';
import { FaTimes, FaCheckCircle, FaTimesCircle, FaAws, FaMicrosoft, FaGoogle, FaServer, FaCopy } from 'react-icons/fa';
import { format } from 'date-fns';
import './ResultModal.css';

const ResultModal = ({ result, onClose }) => {
    if (!result) return null;

    const getProviderIcon = (provider) => {
        switch (provider?.toLowerCase()) {
            case 'aws':
                return <FaAws size={40} color="#FF9900" />;
            case 'azure':
                return <FaMicrosoft size={40} color="#00A4EF" />;
            case 'google':
            case 'gcp':
                return <FaGoogle size={40} color="#4285F4" />;
            case 'onpremise':
            case 'on-premise':
                return <FaServer size={40} color="#6366f1" />;
            default:
                return <FaServer size={40} color="#667eea" />;
        }
    };

    const copyToClipboard = (text) => {
        navigator.clipboard.writeText(text);
    };

    const backdropVariants = {
        hidden: { opacity: 0 },
        visible: { opacity: 1 }
    };

    const modalVariants = {
        hidden: {
            opacity: 0,
            scale: 0.8,
            y: 50
        },
        visible: {
            opacity: 1,
            scale: 1,
            y: 0,
            transition: {
                type: "spring",
                stiffness: 300,
                damping: 25
            }
        },
        exit: {
            opacity: 0,
            scale: 0.8,
            y: 50,
            transition: {
                duration: 0.2
            }
        }
    };

    const renderSuccessResult = () => {
        const vm = result.vm_details;
        if (!vm) return null;

        const disks = Array.isArray(vm.disks) ? vm.disks : [];
        const disk = disks.length > 0 ? disks[0] : null;
        const network = vm.network || null;

        return (
            <motion.div
                className="modal-content success"
                variants={modalVariants}
                initial="hidden"
                animate="visible"
                exit="exit"
            >
                {/* Header del modal */}
                <div className="modal-header success-header">
                    <div className="modal-header-icon">
                        <FaCheckCircle size={50} />
                    </div>
                    <div className="modal-header-text">
                        <h2>✅ {result.message || 'Operación Exitosa'}</h2>
                        <p>La máquina virtual ha sido creada correctamente</p>
                    </div>
                    <button className="modal-close" onClick={onClose}>
                        <FaTimes />
                    </button>
                </div>

                {/* Información principal */}
                <div className="modal-body">
                    <div className="vm-header-card">
                        <div className="provider-icon-large">
                            {getProviderIcon(vm.provider)}
                        </div>
                        <div className="vm-main-info">
                            <h3>{vm.name}</h3>
                            <div className="vm-id-container">
                                <code className="vm-id">{vm.vmId}</code>
                                <button
                                    className="copy-button"
                                    onClick={() => copyToClipboard(vm.vmId)}
                                    title="Copiar ID"
                                >
                                    <FaCopy />
                                </button>
                            </div>
                            <div className="status-badge-large">
                                <span className={`status-dot ${vm.status?.toLowerCase()}`}></span>
                                {vm.status || 'Unknown'}
                            </div>
                        </div>
                    </div>

                    {/* Detalles en grid */}
                    <div className="details-grid">
                        {/* Proveedor y Ubicación */}
                        <div className="detail-card">
                            <h4>🌐 Proveedor y Ubicación</h4>
                            <div className="detail-row">
                                <span className="detail-label">Proveedor:</span>
                                <span className="detail-value">{vm.provider?.toUpperCase() || 'N/A'}</span>
                            </div>
                            {(vm.location || vm.region || network?.region) && (
                                <div className="detail-row">
                                    <span className="detail-label">Región:</span>
                                    <span className="detail-value">
                                        {vm.location || vm.region || network?.region || 'N/A'}
                                    </span>
                                </div>
                            )}
                            {vm.instance_type && (
                                <div className="detail-row">
                                    <span className="detail-label">Tipo de Instancia:</span>
                                    <span className="detail-value highlight">{vm.instance_type}</span>
                                </div>
                            )}
                        </div>

                        {/* Recursos de Cómputo */}
                        <div className="detail-card">
                            <h4>💻 Recursos de Cómputo</h4>
                            {vm.vcpus && (
                                <div className="detail-row">
                                    <span className="detail-label">vCPUs:</span>
                                    <span className="detail-value">{vm.vcpus} núcleos</span>
                                </div>
                            )}
                            {vm.memoryGB && (
                                <div className="detail-row">
                                    <span className="detail-label">Memoria RAM:</span>
                                    <span className="detail-value">{vm.memoryGB} GB</span>
                                </div>
                            )}
                            {vm.memoryOptimization !== undefined && vm.memoryOptimization !== null && (
                                <div className="detail-row">
                                    <span className="detail-label">Optimización de Memoria:</span>
                                    <span className={`detail-value ${vm.memoryOptimization ? 'enabled' : 'disabled'}`}>
                                        {vm.memoryOptimization ? '✓ Activada' : '✗ Desactivada'}
                                    </span>
                                </div>
                            )}
                            {vm.diskOptimization !== undefined && vm.diskOptimization !== null && (
                                <div className="detail-row">
                                    <span className="detail-label">Optimización de Disco:</span>
                                    <span className={`detail-value ${vm.diskOptimization ? 'enabled' : 'disabled'}`}>
                                        {vm.diskOptimization ? '✓ Activada' : '✗ Desactivada'}
                                    </span>
                                </div>
                            )}
                        </div>

                        {/* Red */}
                        {network && (
                            <div className="detail-card">
                                <h4>🌐 Configuración de Red</h4>
                                {network.name && (
                                    <div className="detail-row">
                                        <span className="detail-label">Red:</span>
                                        <span className="detail-value">{network.name}</span>
                                    </div>
                                )}
                                {network.networkId && (
                                    <div className="detail-row">
                                        <span className="detail-label">Network ID:</span>
                                        <span className="detail-value code-value">{network.networkId}</span>
                                    </div>
                                )}
                                {network.cidr_block && (
                                    <div className="detail-row">
                                        <span className="detail-label">CIDR Block:</span>
                                        <span className="detail-value code-value">{network.cidr_block}</span>
                                    </div>
                                )}
                                {network.publicIP !== undefined && network.publicIP !== null && (
                                    <div className="detail-row">
                                        <span className="detail-label">IP Pública:</span>
                                        <span className={`detail-value ${network.publicIP ? 'enabled' : 'disabled'}`}>
                                            {network.publicIP ? '✓ Asignada' : '✗ No asignada'}
                                        </span>
                                    </div>
                                )}
                                {network.firewallRules && Array.isArray(network.firewallRules) && network.firewallRules.length > 0 && (
                                    <div className="detail-row">
                                        <span className="detail-label">Reglas de Firewall:</span>
                                        <span className="detail-value">
                                            {network.firewallRules.join(', ')}
                                        </span>
                                    </div>
                                )}
                            </div>
                        )}

                        {/* Almacenamiento */}
                        {disk && (
                            <div className="detail-card">
                                <h4>💾 Almacenamiento</h4>
                                <div className="detail-row">
                                    <span className="detail-label">Disco ID:</span>
                                    <span className="detail-value code-value">{disk.diskId}</span>
                                </div>
                                <div className="detail-row">
                                    <span className="detail-label">Tamaño:</span>
                                    <span className="detail-value">{disk.size_gb} GB</span>
                                </div>
                                <div className="detail-row">
                                    <span className="detail-label">Tipo:</span>
                                    <span className="detail-value">{disk.disk_type}</span>
                                </div>
                                {disk.iops && (
                                    <div className="detail-row">
                                        <span className="detail-label">IOPS:</span>
                                        <span className="detail-value">{disk.iops}</span>
                                    </div>
                                )}
                            </div>
                        )}

                        {/* Información Adicional */}
                        <div className="detail-card">
                            <h4>📋 Información Adicional</h4>
                            {vm.createdAt && (
                                <div className="detail-row">
                                    <span className="detail-label">Fecha de Creación:</span>
                                    <span className="detail-value">
                                        {format(new Date(vm.createdAt), 'dd/MM/yyyy HH:mm:ss')}
                                    </span>
                                </div>
                            )}
                            {vm.keyPairName && (
                                <div className="detail-row">
                                    <span className="detail-label">Key Pair:</span>
                                    <span className="detail-value code-value">{vm.keyPairName}</span>
                                </div>
                            )}
                            {vm.provider && (
                                <div className="detail-row">
                                    <span className="detail-label">Provider ID:</span>
                                    <span className="detail-value">{vm.provider}</span>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                {/* Footer con acciones */}
                <div className="modal-footer">
                    <button className="btn-secondary" onClick={onClose}>
                        Cerrar
                    </button>
                    <button
                        className="btn-primary"
                        onClick={() => {
                            const dataStr = JSON.stringify(vm, null, 2);
                            const dataBlob = new Blob([dataStr], { type: 'application/json' });
                            const url = URL.createObjectURL(dataBlob);
                            const link = document.createElement('a');
                            link.href = url;
                            link.download = `vm-${vm.vmId}.json`;
                            link.click();
                        }}
                    >
                        Exportar JSON
                    </button>
                </div>
            </motion.div>
        );
    };

    const renderErrorResult = () => {
        return (
            <motion.div
                className="modal-content error"
                variants={modalVariants}
                initial="hidden"
                animate="visible"
                exit="exit"
            >
                <div className="modal-header error-header">
                    <div className="modal-header-icon">
                        <FaTimesCircle size={50} />
                    </div>
                    <div className="modal-header-text">
                        <h2>❌ Error en la Operación</h2>
                        <p>No se pudo completar la solicitud</p>
                    </div>
                    <button className="modal-close" onClick={onClose}>
                        <FaTimes />
                    </button>
                </div>

                <div className="modal-body">
                    <div className="error-details">
                        <div className="error-message-box">
                            <h4>Mensaje de Error:</h4>
                            <p>{result.message || result.error || 'Error desconocido'}</p>
                        </div>

                        {result.error_detail && (
                            <div className="error-detail-box">
                                <h4>Detalles Técnicos:</h4>
                                <pre>{typeof result.error_detail === 'string' ? result.error_detail : JSON.stringify(result.error_detail, null, 2)}</pre>
                            </div>
                        )}

                        {result.provider && (
                            <div className="error-info">
                                <strong>Proveedor:</strong> {result.provider}
                            </div>
                        )}
                    </div>

                    <div className="error-suggestions">
                        <h4>💡 Sugerencias:</h4>
                        <ul>
                            <li>Verifica que el backend esté ejecutándose correctamente</li>
                            <li>Revisa que todos los parámetros sean válidos</li>
                            <li>Asegúrate de que el proveedor esté disponible</li>
                            <li>Consulta los logs del servidor para más detalles</li>
                        </ul>
                    </div>
                </div>

                <div className="modal-footer">
                    <button className="btn-secondary" onClick={onClose}>
                        Cerrar
                    </button>
                </div>
            </motion.div>
        );
    };

    return (
        <motion.div
            className="modal-backdrop"
            variants={backdropVariants}
            initial="hidden"
            animate="visible"
            exit="hidden"
            onClick={onClose}
        >
            <div onClick={(e) => e.stopPropagation()}>
                {result.success ? renderSuccessResult() : renderErrorResult()}
            </div>
        </motion.div>
    );
};

export default ResultModal;