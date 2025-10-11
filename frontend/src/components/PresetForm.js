import React, { useState } from 'react';
import { buildPresetVm } from '../services/apiService';
import './ProvisionForm.css'; // Reutilizamos los estilos

const PresetForm = ({ providers, onResult }) => {
    const [provider, setProvider] = useState(providers[0] || '');
    const [preset, setPreset] = useState('standard');
    const [name, setName] = useState('preset-vm-1');
    const [location, setLocation] = useState('us-east-1');
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        setError(null);
        onResult(null);

        const payload = {
            provider,
            preset,
            name,
            location,
        };

        try {
            const result = await buildPresetVm(payload);
            onResult(result);
        } catch (err) {
            setError(err.message || 'Ocurrió un error desconocido.');
            onResult(null);
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="form-container">
            <h2>📚 Usar Plantilla (Director Pattern)</h2>
            <p>Elige una configuración pre-optimizada. Ideal para desplegar entornos conocidos rápidamente.</p>

            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="preset-provider">Proveedor de Nube</label>
                    <select id="preset-provider" value={provider} onChange={(e) => setProvider(e.target.value)} required>
                        {providers.map((p) => (
                            <option key={p} value={p}>{p.charAt(0).toUpperCase() + p.slice(1)}</option>
                        ))}
                    </select>
                </div>

                <div className="form-group">
                    <label htmlFor="preset">Plantilla de VM</label>
                    <select id="preset" value={preset} onChange={(e) => setPreset(e.target.value)} required>
                        <option value="minimal">Minimal (Para desarrollo)</option>
                        <option value="standard">Standard (Servidor Web)</option>
                        <option value="high-performance">High-Performance (Base de Datos)</option>
                    </select>
                </div>

                <div className="form-group">
                    <label htmlFor="preset-name">Nombre de la VM</label>
                    <input type="text" id="preset-name" value={name} onChange={(e) => setName(e.target.value)} required />
                </div>

                <div className="form-group">
                    <label htmlFor="preset-location">Región / Ubicación</label>
                    <input type="text" id="preset-location" value={location} onChange={(e) => setLocation(e.target.value)} required />
                </div>

                <button type="submit" className="submit-button director" disabled={submitting}>
                    {submitting ? 'Aplicando plantilla...' : '📚 Crear desde Plantilla'}
                </button>
            </form>

            {error && (
                <div className="error-message form-error">
                    <strong>Error:</strong> {error}
                </div>
            )}
        </div>
    );
};

export default PresetForm;