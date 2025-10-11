import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FaTools, FaServer, FaMicrochip, FaHdd, FaNetworkWired, FaCog, FaChevronDown } from 'react-icons/fa';
import { buildVm } from '../services/apiService';
import { getProviderKey } from './providerUtils';
import './FormStyles.css';

const instanceTypesByProvider = {
    aws: [
        { name: 't3.medium', cpu: 2, ram: 4, desc: 'Uso general balanceado' },
        { name: 'm5.large', cpu: 2, ram: 8, desc: 'Memoria estándar' },
        { name: 'r5.large', cpu: 2, ram: 16, desc: 'Optimizado en memoria' },
        { name: 'c5.large', cpu: 2, ram: 4, desc: 'Optimizado en CPU' },
    ],
    azure: [
        { name: 'Standard_B2s', cpu: 2, ram: 4, desc: 'Uso general' },
        { name: 'Standard_D2s_v3', cpu: 2, ram: 8, desc: 'Propósito general' },
        { name: 'Standard_E2s_v3', cpu: 2, ram: 16, desc: 'Optimizado en memoria' },
        { name: 'Standard_F2s_v2', cpu: 2, ram: 4, desc: 'Optimizado en CPU' },
    ],
    google: [
        { name: 'e2-standard-2', cpu: 2, ram: 8, desc: 'Estándar' },
        { name: 'n2-highmem-2', cpu: 2, ram: 16, desc: 'Alta memoria' },
        { name: 'n2-highcpu-2', cpu: 2, ram: 2, desc: 'Alta CPU' },
    ],
    onpremise: [
        { name: 'onprem-medium', cpu: 2, ram: 4, desc: 'Mediano' },
        { name: 'onprem-large', cpu: 4, ram: 16, desc: 'Grande' },
    ],
};

const BuildForm = ({ providers, onResult }) => {
    const [formData, setFormData] = useState({
        provider: providers[0] || '',
        name: 'custom-vm-1',
        vm_type: '',
        cpu: '2',
        ram: '4',
        disk_gb: '50',
        disk_type: 'ssd',
        location: 'us-east-1',
        monitoring: true,
        optimized: false,
        resource_group: 'default-rg',
    });
    
    const [submitting, setSubmitting] = useState(false);
    const [showAdvanced, setShowAdvanced] = useState(false);

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: { staggerChildren: 0.08 }
        }
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.4 } }
    };

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: type === 'checkbox' ? checked : value
        }));
    };

    const handleInstanceTypeChange = (type) => {
        const providerKey = getProviderKey(formData.provider);
        const typeData = (instanceTypesByProvider[providerKey] || []).find(t => t.name === type);

        setFormData(prev => ({
            ...prev,
            vm_type: type,
            cpu: typeData ? String(typeData.cpu) : prev.cpu,
            ram: typeData ? String(typeData.ram) : prev.ram,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        onResult(null);

        const build_config = {
            name: formData.name,
            location: formData.location,
            vm_type: formData.vm_type || undefined,
            cpu: formData.cpu ? parseInt(formData.cpu, 10) : undefined,
            ram: formData.ram ? parseInt(formData.ram, 10) : undefined,
            disk_gb: formData.disk_gb ? parseInt(formData.disk_gb, 10) : undefined,
            disk_type: formData.disk_type || undefined,
            advanced_options: {
                monitoring: formData.monitoring,
                optimized: formData.optimized,
                resource_group: formData.resource_group || undefined,
            }
        };

        Object.keys(build_config).forEach(key => 
            (build_config[key] === undefined) && delete build_config[key]
        );
        Object.keys(build_config.advanced_options).forEach(key => 
            (build_config.advanced_options[key] === undefined) && delete build_config.advanced_options[key]
        );

        const payload = { provider: formData.provider, build_config };

        try {
            const result = await buildVm(payload);
            onResult(result);
        } catch (err) {
            onResult({
                success: false,
                message: err.message || 'Error en la construcción',
                error_detail: err.error_detail
            });
        } finally {
            setSubmitting(false);
        }
    };

    const providerKey = getProviderKey(formData.provider);
    const currentInstanceTypes = instanceTypesByProvider[providerKey] || [];
    const isCustomInstance = !formData.vm_type;

    return (
        <motion.div
            className="form-modern-container"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
        >
            <motion.div className="form-header" variants={itemVariants}>
                <div className="form-icon-badge builder">
                    <FaTools size={30} />
                </div>
                <div>
                    <h2>🛠️ Construcción Personalizada</h2>
                    <p className="form-description">
                        Usa el patrón Builder para definir cada aspecto de tu VM con precisión
                    </p>
                </div>
            </motion.div>

            <form onSubmit={handleSubmit}>
                {/* Configuración Principal */}
                <motion.fieldset variants={itemVariants}>
                    <legend>📋 Configuración Principal</legend>
                    <div className="form-grid-layout">
                        <div className="form-field-modern">
                            <label><FaServer /> Proveedor</label>
                            <select name="provider" value={formData.provider} onChange={handleChange} className="modern-select" required>
                                {providers.map(p => (
                                    <option key={p} value={p}>{p.charAt(0).toUpperCase() + p.slice(1)}</option>
                                ))}
                            </select>
                        </div>
                        <div className="form-field-modern">
                            <label>🏷️ Nombre de la VM</label>
                            <input type="text" name="name" value={formData.name} onChange={handleChange} className="modern-input" required />
                        </div>
                        <div className="form-field-modern full-width">
                            <label>🌍 Región / Ubicación</label>
                            <input type="text" name="location" value={formData.location} onChange={handleChange} className="modern-input" required />
                            <span className="field-hint">Región donde se desplegará la VM</span>
                        </div>
                    </div>
                </motion.fieldset>

                {/* Tipo de Instancia */}
                <motion.fieldset variants={itemVariants}>
                    <legend><FaMicrochip /> Tipo de Instancia</legend>
                    <div className="selection-cards">
                        <motion.div
                            className={`selection-card ${!formData.vm_type ? 'selected' : ''}`}
                            onClick={() => handleInstanceTypeChange('')}
                            whileHover={{ scale: 1.02 }}
                            whileTap={{ scale: 0.98 }}
                        >
                            <div className="selection-card-icon">⚙️</div>
                            <h4>Personalizado</h4>
                            <p>Configura manualmente</p>
                        </motion.div>
                        {currentInstanceTypes.map(type => (
                            <motion.div
                                key={type.name}
                                className={`selection-card ${formData.vm_type === type.name ? 'selected' : ''}`}
                                onClick={() => handleInstanceTypeChange(type.name)}
                                whileHover={{ scale: 1.02 }}
                                whileTap={{ scale: 0.98 }}
                            >
                                <div className="selection-card-icon">💻</div>
                                <h4>{type.name}</h4>
                                <p>{type.cpu} vCPU / {type.ram} GB RAM</p>
                                <span className="field-hint">{type.desc}</span>
                            </motion.div>
                        ))}
                    </div>

                    <AnimatePresence>
                        {isCustomInstance && (
                            <motion.div
                                className="form-grid-layout"
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: 'auto' }}
                                exit={{ opacity: 0, height: 0 }}
                            >
                                <div className="form-field-modern">
                                    <label>🔢 vCPUs</label>
                                    <input type="number" name="cpu" value={formData.cpu} onChange={handleChange} className="modern-input" min="1" />
                                </div>
                                <div className="form-field-modern">
                                    <label>💾 RAM (GB)</label>
                                    <input type="number" name="ram" value={formData.ram} onChange={handleChange} className="modern-input" min="1" />
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </motion.fieldset>

                {/* Almacenamiento */}
                <motion.fieldset variants={itemVariants}>
                    <legend><FaHdd /> Almacenamiento</legend>
                    <div className="form-grid-layout">
                        <div className="form-field-modern">
                            <label>📦 Tamaño del Disco (GB)</label>
                            <input type="number" name="disk_gb" value={formData.disk_gb} onChange={handleChange} className="modern-input" min="10" />
                        </div>
                        <div className="form-field-modern">
                            <label>💿 Tipo de Disco</label>
                            <select name="disk_type" value={formData.disk_type} onChange={handleChange} className="modern-select">
                                <option value="ssd">SSD (Rápido)</option>
                                <option value="standard">Standard (Estándar)</option>
                                <option value="balanced">Balanced (Balanceado)</option>
                            </select>
                        </div>
                    </div>
                </motion.fieldset>

                {/* Opciones Avanzadas */}
                <motion.div variants={itemVariants}>
                    <div
                        className="collapsible-header"
                        onClick={() => setShowAdvanced(!showAdvanced)}
                    >
                        <h4><FaCog /> Opciones Avanzadas</h4>
                        <FaChevronDown className={`collapsible-icon ${showAdvanced ? 'open' : ''}`} />
                    </div>
                    
                    <AnimatePresence>
                        {showAdvanced && (
                            <motion.div
                                className="collapsible-content"
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: 'auto' }}
                                exit={{ opacity: 0, height: 0 }}
                            >
                                <div className="form-field-modern">
                                    <label>🏢 Grupo de Recursos</label>
                                    <input type="text" name="resource_group" value={formData.resource_group} onChange={handleChange} className="modern-input" />
                                    <span className="field-hint">Opcional: Grupo lógico para organizar recursos</span>
                                </div>
                                
                                <div className="checkbox-group-modern">
                                    <div className="checkbox-item">
                                        <input type="checkbox" name="monitoring" id="monitoring" checked={formData.monitoring} onChange={handleChange} />
                                        <label htmlFor="monitoring">
                                            <strong>📊 Activar Monitoreo</strong>
                                            <span className="field-hint">Habilita métricas y alertas</span>
                                        </label>
                                    </div>
                                    <div className="checkbox-item">
                                        <input type="checkbox" name="optimized" id="optimized" checked={formData.optimized} onChange={handleChange} />
                                        <label htmlFor="optimized">
                                            <strong>⚡ Optimización de Disco</strong>
                                            <span className="field-hint">Mejora el rendimiento I/O</span>
                                        </label>
                                    </div>
                                </div>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </motion.div>

                <motion.div variants={itemVariants}>
                    <motion.button
                        type="submit"
                        className="submit-button-modern builder"
                        disabled={submitting}
                        whileHover={{ scale: submitting ? 1 : 1.02 }}
                        whileTap={{ scale: submitting ? 1 : 0.98 }}
                    >
                        {submitting ? (
                            <>
                                <div className="spinner-small"></div>
                                Construyendo VM...
                            </>
                        ) : (
                            <>
                                <FaTools /> Construir VM Personalizada
                            </>
                        )}
                    </motion.button>
                </motion.div>
            </form>

            <motion.div className="form-footer-info" variants={itemVariants}>
                <div className="info-badge">
                    <strong>🛠️ Builder Pattern</strong>
                    <p>Construcción paso a paso con máxima flexibilidad y control</p>
                </div>
            </motion.div>
        </motion.div>
    );
};

export default BuildForm;