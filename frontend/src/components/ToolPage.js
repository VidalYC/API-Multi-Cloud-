import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaArrowLeft, FaBolt, FaTools, FaBookOpen } from 'react-icons/fa';
import { getProviders } from '../services/apiService';
import ProvisionForm from './ProvisionForm';
import BuildForm from './BuildForm';
import PresetForm from './PresetForm';
import ResultModal from './ResultModal';
import './ToolPage.css';

const ToolPage = ({ onBackToHome }) => {
    const [activeTab, setActiveTab] = useState('quick');
    const [providers, setProviders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [result, setResult] = useState(null);
    const [showModal, setShowModal] = useState(false);

    useEffect(() => {
        const fetchProviders = async () => {
            try {
                const data = await getProviders();
                const uniqueProviders = [...new Set(data.providers.map(p => {
                    if (p === 'gcp') return 'google';
                    if (p === 'on-premise') return 'onpremise';
                    return p;
                }))];
                setProviders(uniqueProviders);
                setLoading(false);
            } catch (err) {
                setError('No se pudieron cargar los proveedores. ¿El backend está funcionando?');
                setLoading(false);
            }
        };
        fetchProviders();
    }, []);

    const handleResult = (res) => {
        setResult(res);
        if (res) {
            setShowModal(true);
        }
    };

    const closeModal = () => {
        setShowModal(false);
    };

    const tabConfig = [
        { id: 'quick', label: 'Provisión Rápida', icon: <FaBolt />, color: '#28a745' },
        { id: 'custom', label: 'Construcción Personalizada', icon: <FaTools />, color: '#ff8c00' },
        { id: 'template', label: 'Usar Plantilla', icon: <FaBookOpen />, color: '#6a5acd' }
    ];

    const renderContent = () => {
        switch (activeTab) {
            case 'quick':
                return <ProvisionForm providers={providers} onResult={handleResult} />;
            case 'custom':
                return <BuildForm providers={providers} onResult={handleResult} />;
            case 'template':
                return <PresetForm providers={providers} onResult={handleResult} />;
            default:
                return null;
        }
    };

    return (
        <div className="tool-page">
            {/* Header con gradiente */}
            <motion.header
                className="tool-header"
                initial={{ y: -100, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.5 }}
            >
                <motion.button
                    className="back-button-tool"
                    onClick={onBackToHome}
                    whileHover={{ scale: 1.05, x: -5 }}
                    whileTap={{ scale: 0.95 }}
                >
                    <FaArrowLeft /> Volver al Inicio
                </motion.button>
                <div className="header-content">
                    <h1>🚀 Panel de Aprovisionamiento de VMs</h1>
                    <p>Gestiona tu infraestructura multi-cloud desde una única interfaz</p>
                </div>
            </motion.header>

            {/* Contenedor principal */}
            <div className="tool-container">
                {/* Tabs mejoradas */}
                <motion.div
                    className="tabs-enhanced"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.2 }}
                >
                    {tabConfig.map((tab, index) => (
                        <motion.button
                            key={tab.id}
                            className={`tab-button ${activeTab === tab.id ? 'active' : ''}`}
                            onClick={() => setActiveTab(tab.id)}
                            style={{
                                '--tab-color': tab.color
                            }}
                            whileHover={{ y: -3 }}
                            whileTap={{ scale: 0.98 }}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.1 * index }}
                        >
                            <span className="tab-icon">{tab.icon}</span>
                            <span className="tab-label">{tab.label}</span>
                            {activeTab === tab.id && (
                                <motion.div
                                    className="tab-indicator"
                                    layoutId="activeTab"
                                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                                />
                            )}
                        </motion.button>
                    ))}
                </motion.div>

                {/* Área de contenido con animación */}
                <AnimatePresence mode="wait">
                    <motion.main
                        key={activeTab}
                        className="form-area"
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20 }}
                        transition={{ duration: 0.3 }}
                    >
                        {loading && (
                            <div className="loading-container">
                                <div className="loading-spinner-large"></div>
                                <p>Cargando proveedores...</p>
                            </div>
                        )}
                        {error && (
                            <motion.div
                                className="error-banner"
                                initial={{ opacity: 0, y: -20 }}
                                animate={{ opacity: 1, y: 0 }}
                            >
                                <span className="error-icon">⚠️</span>
                                <div>
                                    <strong>Error de conexión</strong>
                                    <p>{error}</p>
                                </div>
                            </motion.div>
                        )}
                        {!loading && !error && renderContent()}
                    </motion.main>
                </AnimatePresence>
            </div>

            {/* Modal de resultados */}
            <AnimatePresence>
                {showModal && (
                    <ResultModal
                        result={result}
                        onClose={closeModal}
                    />
                )}
            </AnimatePresence>
        </div>
    );
};

export default ToolPage;