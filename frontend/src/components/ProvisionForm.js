import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FaRocket, FaCloud, FaMapMarkerAlt } from 'react-icons/fa';
import { provisionVm } from '../services/apiService';
import './FormStyles.css';

const ProvisionForm = ({ providers, onResult }) => {
    const [provider, setProvider] = useState(providers[0] || '');
    const [vmType, setVmType] = useState('t2.micro');
    const [region, setRegion] = useState('us-east-1');
    const [submitting, setSubmitting] = useState(false);

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: {
            opacity: 1,
            y: 0,
            transition: { duration: 0.4 }
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        onResult(null);

        const payload = {
            provider: provider,
            config: {
                type: vmType,
                region: region,
            },
        };

        try {
            const result = await provisionVm(payload);
            onResult(result);
        } catch (err) {
            onResult({
                success: false,
                message: err.message || 'Error en el aprovisionamiento',
                error_detail: err.error_detail
            });
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <motion.div
            className="form-modern-container"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
        >
            <motion.div className="form-header" variants={itemVariants}>
                <div className="form-icon-badge factory">
                    <FaRocket size={30} />
                </div>
                <div>
                    <h2>⚡ Provisión Rápida</h2>
                    <p className="form-description">
                        Utiliza el patrón Factory para crear VMs con configuración estándar en segundos
                    </p>
                </div>
            </motion.div>

            <form onSubmit={handleSubmit}>
                <motion.div className="form-grid-layout" variants={itemVariants}>
                    {/* Proveedor */}
                    <div className="form-field-modern">
                        <label htmlFor="provider">
                            <FaCloud /> Proveedor de Nube
                        </label>
                        <div className="input-wrapper">
                            <select
                                id="provider"
                                value={provider}
                                onChange={(e) => setProvider(e.target.value)}
                                required
                                className="modern-select"
                            >
                                {providers.map((p) => (
                                    <option key={p} value={p}>
                                        {p.charAt(0).toUpperCase() + p.slice(1)}
                                    </option>
                                ))}
                            </select>
                        </div>
                        <span className="field-hint">Selecciona el proveedor cloud</span>
                    </div>

                    {/* Tipo de VM */}
                    <div className="form-field-modern">
                        <label htmlFor="vmType">
                            💻 Tipo de Instancia
                        </label>
                        <div className="input-wrapper">
                            <input
                                type="text"
                                id="vmType"
                                value={vmType}
                                onChange={(e) => setVmType(e.target.value)}
                                placeholder="Ej: t2.micro, Standard_B1s"
                                required
                                className="modern-input"
                            />
                        </div>
                        <span className="field-hint">Tipo de instancia del proveedor</span>
                    </div>

                    {/* Región */}
                    <div className="form-field-modern full-width">
                        <label htmlFor="region">
                            <FaMapMarkerAlt /> Región / Ubicación
                        </label>
                        <div className="input-wrapper">
                            <input
                                type="text"
                                id="region"
                                value={region}
                                onChange={(e) => setRegion(e.target.value)}
                                placeholder="Ej: us-east-1, eastus, us-central1-a"
                                required
                                className="modern-input"
                            />
                        </div>
                        <span className="field-hint">Región donde se desplegará la VM</span>
                    </div>
                </motion.div>

                <motion.div variants={itemVariants}>
                    <motion.button
                        type="submit"
                        className="submit-button-modern factory"
                        disabled={submitting}
                        whileHover={{ scale: submitting ? 1 : 1.02 }}
                        whileTap={{ scale: submitting ? 1 : 0.98 }}
                    >
                        {submitting ? (
                            <>
                                <div className="spinner-small"></div>
                                Aprovisionando...
                            </>
                        ) : (
                            <>
                                <FaRocket /> Aprovisionar VM
                            </>
                        )}
                    </motion.button>
                </motion.div>
            </form>

            <motion.div className="form-footer-info" variants={itemVariants}>
                <div className="info-badge">
                    <strong>🏭 Factory Pattern</strong>
                    <p>Creación estandarizada y rápida de recursos</p>
                </div>
            </motion.div>
        </motion.div>
    );
};

export default ProvisionForm;