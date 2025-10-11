import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FaBookOpen, FaRocket, FaServer, FaDatabase, FaCode } from 'react-icons/fa';
import { buildPresetVm } from '../services/apiService';
import './FormStyles.css';

const presetOptions = [
    {
        id: 'minimal',
        name: 'Minimal',
        icon: <FaCode size={40} />,
        color: '#17a2b8',
        description: 'Desarrollo y Testing',
        specs: '1 vCPU / 1 GB RAM / 10 GB Disco',
        useCases: ['Desarrollo local', 'Testing', 'Proyectos pequeños']
    },
    {
        id: 'standard',
        name: 'Standard',
        icon: <FaServer size={40} />,
        color: '#28a745',
        description: 'Servidor Web',
        specs: '2 vCPU / 4 GB RAM / 50 GB Disco',
        useCases: ['Aplicaciones web', 'APIs REST', 'Microservicios']
    },
    {
        id: 'high-performance',
        name: 'High Performance',
        icon: <FaDatabase size={40} />,
        color: '#dc3545',
        description: 'Base de Datos',
        specs: '8 vCPU / 32 GB RAM / 500 GB Disco',
        useCases: ['Bases de datos', 'Analytics', 'Machine Learning']
    }
];

const PresetForm = ({ providers, onResult }) => {
    const [provider, setProvider] = useState(providers[0] || '');
    const [preset, setPreset] = useState('standard');
    const [name, setName] = useState('preset-vm-1');
    const [location, setLocation] = useState('us-east-1');
    const [submitting, setSubmitting] = useState(false);

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: { staggerChildren: 0.1 }
        }
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0, transition: { duration: 0.4 } }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        onResult(null);

        const payload = { provider, preset, name, location };

        try {
            const result = await buildPresetVm(payload);
            onResult(result);
        } catch (err) {
            onResult({
                success: false,
                message: err.message || 'Error al aplicar plantilla',
                error_detail: err.error_detail
            });
        } finally {
            setSubmitting(false);
        }
    };

    const selectedPreset = presetOptions.find(p => p.id === preset);

    return (
        <motion.div
            className="form-modern-container"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
        >
            <motion.div className="form-header" variants={itemVariants}>
                <div className="form-icon-badge director">
                    <FaBookOpen size={30} />
                </div>
                <div>
                    <h2>📚 Usar Plantilla</h2>
                    <p className="form-description">
                        Director Pattern con configuraciones pre-optimizadas para casos de uso comunes
                    </p>
                </div>
            </motion.div>

            <form onSubmit={handleSubmit}>
                {/* Selección de Plantilla */}
                <motion.div variants={itemVariants}>
                    <h3 style={{ marginBottom: '1.5rem', color: '#495057' }}>
                        🎯 Selecciona una Plantilla
                    </h3>
                    <div className="selection-cards">
                        {presetOptions.map((option) => (
                            <motion.div
                                key={option.id}
                                className={`selection-card preset-card ${preset === option.id ? 'selected' : ''}`}
                                onClick={() => setPreset(option.id)}
                                whileHover={{ scale: 1.03, y: -5 }}
                                whileTap={{ scale: 0.98 }}
                                style={{
                                    borderColor: preset === option.id ? option.color : '#e9ecef'
                                }}
                            >
                                <div
                                    className="selection-card-icon"
                                    style={{ color: option.color }}
                                >
                                    {option.icon}
                                </div>
                                <h4>{option.name}</h4>
                                <p style={{ fontWeight: 600, color: '#495057', marginBottom: '0.5rem' }}>
                                    {option.description}
                                </p>
                                <span className="field-hint" style={{ display: 'block', marginBottom: '0.75rem' }}>
                                    {option.specs}
                                </span>
                                <div className="tags-container">
                                    {option.useCases.map((useCase, idx) => (
                                        <span key={idx} className="tag">
                                            {useCase}
                                        </span>
                                    ))}
                                </div>
                            </motion.div>
                        ))}
                    </div>
                </motion.div>

                {/* Información de la plantilla seleccionada */}
                {selectedPreset && (
                    <motion.div
                        className="inline-alert info"
                        variants={itemVariants}
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                    >
                        <div className="inline-alert-icon">ℹ️</div>
                        <div>
                            <strong>Plantilla: {selectedPreset.name}</strong>
                            <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.9rem' }}>
                                Esta configuración es ideal para: {selectedPreset.useCases.join(', ')}
                            </p>
                        </div>
                    </motion.div>
                )}

                {/* Configuración */}
                <motion.fieldset variants={itemVariants}>
                    <legend>⚙️ Configuración</legend>
                    <div className="form-grid-layout">
                        <div className="form-field-modern">
                            <label>☁️ Proveedor de Nube</label>
                            <select
                                value={provider}
                                onChange={(e) => setProvider(e.target.value)}
                                className="modern-select"
                                required
                            >
                                {providers.map((p) => (
                                    <option key={p} value={p}>
                                        {p.charAt(0).toUpperCase() + p.slice(1)}
                                    </option>
                                ))}
                            </select>
                        </div>

                        <div className="form-field-modern">
                            <label>🏷️ Nombre de la VM</label>
                            <input
                                type="text"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                className="modern-input"
                                required
                            />
                        </div>

                        <div className="form-field-modern full-width">
                            <label>🌍 Región / Ubicación</label>
                            <input
                                type="text"
                                value={location}
                                onChange={(e) => setLocation(e.target.value)}
                                className="modern-input"
                                placeholder="Ej: us-east-1, eastus, us-central1-a"
                                required
                            />
                            <span className="field-hint">
                                Región donde se desplegará la VM
                            </span>
                        </div>
                    </div>
                </motion.fieldset>

                {/* Resumen */}
                <motion.div
                    className="preset-summary"
                    variants={itemVariants}
                    style={{
                        padding: '1.5rem',
                        background: 'linear-gradient(135deg, rgba(106, 90, 205, 0.05), rgba(147, 112, 219, 0.05))',
                        borderRadius: '15px',
                        border: '2px solid rgba(106, 90, 205, 0.2)',
                        marginBottom: '2rem'
                    }}
                >
                    <h4 style={{ margin: '0 0 1rem 0', color: '#6a5acd', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                        <FaRocket /> Resumen de Despliegue
                    </h4>
                    <div style={{ display: 'grid', gridTemplateColumns: 'auto 1fr', gap: '0.75rem 1.5rem', fontSize: '0.95rem' }}>
                        <strong>Plantilla:</strong>
                        <span>{selectedPreset?.name}</span>
                        
                        <strong>Proveedor:</strong>
                        <span>{provider.toUpperCase()}</span>
                        
                        <strong>Nombre:</strong>
                        <span>{name}</span>
                        
                        <strong>Ubicación:</strong>
                        <span>{location}</span>
                        
                        <strong>Especificaciones:</strong>
                        <span>{selectedPreset?.specs}</span>
                    </div>
                </motion.div>

                <motion.div variants={itemVariants}>
                    <motion.button
                        type="submit"
                        className="submit-button-modern director"
                        disabled={submitting}
                        whileHover={{ scale: submitting ? 1 : 1.02 }}
                        whileTap={{ scale: submitting ? 1 : 0.98 }}
                    >
                        {submitting ? (
                            <>
                                <div className="spinner-small"></div>
                                Aplicando Plantilla...
                            </>
                        ) : (
                            <>
                                <FaBookOpen /> Crear desde Plantilla
                            </>
                        )}
                    </motion.button>
                </motion.div>
            </form>

            <motion.div className="form-footer-info" variants={itemVariants}>
                <div className="info-badge">
                    <strong>📐 Director Pattern</strong>
                    <p>Configuraciones predefinidas que siguen las mejores prácticas de la industria</p>
                </div>
            </motion.div>
        </motion.div>
    );
};

export default PresetForm;