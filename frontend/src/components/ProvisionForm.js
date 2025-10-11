import React, { useState } from 'react';
import { provisionVm } from '../services/apiService';
import './ProvisionForm.css';

const ProvisionForm = ({ providers, onResult }) => {
    const [provider, setProvider] = useState(providers[0] || '');
    const [vmType, setVmType] = useState('t2.micro'); // Valor por defecto para AWS
    const [region, setRegion] = useState('us-east-1'); // Valor por defecto para AWS
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        setError(null);
        onResult(null); // Limpiar resultado anterior

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
            setError(err.message || 'Ocurrió un error desconocido.');
            onResult(null);
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="form-container">
            <h2>⚡ Provisión Rápida (Factory Pattern)</h2>
            <p>Crea una VM con configuración estándar. Ideal para entornos de desarrollo y pruebas rápidas.</p>
            
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="provider">Proveedor de Nube</label>
                    <select
                        id="provider"
                        value={provider}
                        onChange={(e) => setProvider(e.target.value)}
                        required
                    >
                        {providers.map((p) => (
                            <option key={p} value={p}>
                                {p.charAt(0).toUpperCase() + p.slice(1)}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="form-group">
                    <label htmlFor="vmType">Tipo de Instancia</label>
                    <input
                        type="text"
                        id="vmType"
                        value={vmType}
                        onChange={(e) => setVmType(e.target.value)}
                        placeholder="Ej: t2.micro, Standard_B1s"
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="region">Región / Ubicación</label>
                    <input
                        type="text"
                        id="region"
                        value={region}
                        onChange={(e) => setRegion(e.target.value)}
                        placeholder="Ej: us-east-1, eastus"
                        required
                    />
                </div>

                <button type="submit" className="submit-button" disabled={submitting}>
                    {submitting ? 'Aprovisionando...' : '🚀 Aprovisionar VM'}
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

export default ProvisionForm;