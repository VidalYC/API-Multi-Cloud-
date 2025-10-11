import React, { useState } from 'react';
import { buildVm } from '../services/apiService';
import { getProviderKey } from './providerUtils'; // Ruta corregida
import './ProvisionForm.css'; // Reutilizamos los estilos

const instanceTypesByProvider = {
    aws: [
        { name: 't2.micro', cpu: 1, ram: 1 },
        { name: 't2.small', cpu: 1, ram: 2 },
        { name: 't3.medium', cpu: 2, ram: 4 },
        { name: 'm5.large', cpu: 2, ram: 8 },
    ],
    azure: [
        { name: 'Standard_B1s', cpu: 1, ram: 1 },
        { name: 'Standard_B2s', cpu: 2, ram: 4 },
        { name: 'Standard_D2s_v3', cpu: 2, ram: 8 },
    ],
    google: [
        { name: 'e2-micro', cpu: 1, ram: 1 },
        { name: 'e2-small', cpu: 1, ram: 2 },
        { name: 'e2-medium', cpu: 2, ram: 4 },
        { name: 'e2-standard-2', cpu: 2, ram: 8 },
    ],
    onpremise: [
        { name: 'onprem-small', cpu: 1, ram: 2 },
        { name: 'onprem-medium', cpu: 2, ram: 4 },
        { name: 'onprem-large', cpu: 4, ram: 16 },
    ],
    gcp: [], // Alias for google
    'on-premise': [], // Alias for onpremise
};

// Componente reutilizable para campos del formulario
const FormField = ({ id, label, children, hint }) => (
    <div className="form-group">
        <label htmlFor={id}>{label}</label>
        {hint && <p className="form-hint">{hint}</p>}
        {children}
    </div>
);

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
        // Nuevos campos para opciones avanzadas
        monitoring: true,
        optimized: false,
        resource_group: 'default-rg',
    });
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        const { name, value, type, checked } = e.target;
        setFormData(prev => {
            const newFormData = {
                ...prev,
                [name]: type === 'checkbox' ? checked : value
            };

            // Si cambia el proveedor, reseteamos el tipo de instancia
            if (name === 'provider') {
                newFormData.vm_type = '';
            };

            return newFormData;
        });
    };

    const handleInstanceTypeChange = (e) => {
        const selectedType = e.target.value;
        const providerKey = getProviderKey(formData.provider);
        const typeData = (instanceTypesByProvider[providerKey] || []).find(t => t.name === selectedType);

        setFormData(prev => ({
            ...prev,
            vm_type: selectedType,
            cpu: typeData ? String(typeData.cpu) : prev.cpu,
            ram: typeData ? String(typeData.ram) : prev.ram,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitting(true);
        setError(null);
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
        // Limpiar valores nulos o indefinidos del payload
        Object.keys(build_config).forEach(key => (build_config[key] === undefined) && delete build_config[key]);
        Object.keys(build_config.advanced_options).forEach(key => (build_config.advanced_options[key] === undefined) && delete build_config.advanced_options[key]);

        const payload = {
            provider: formData.provider,
            build_config: build_config,
        };

        try {
            const result = await buildVm(payload);
            onResult(result);
        } catch (err) {
            setError(err.message || 'Ocurrió un error desconocido.');
            onResult(null);
        } finally {
            setSubmitting(false);
        }
    };

    const isCustomInstance = !formData.vm_type;
    const providerKey = getProviderKey(formData.provider);
    const currentInstanceTypes = instanceTypesByProvider[providerKey] || [];

    return (
        <div className="form-container">
            <h2>🛠️ Construcción Personalizada (Builder Pattern)</h2>
            <p>Define cada aspecto de tu VM. Ideal para entornos de producción con requisitos específicos.</p>

            <form onSubmit={handleSubmit}>
                <fieldset>
                    <legend>Configuración Principal</legend>
                    <FormField id="build-provider" label="Proveedor de Nube">
                        <select id="build-provider" name="provider" value={formData.provider} onChange={handleChange} required>
                            {providers.map((p) => (
                                <option key={p} value={p}>{p.charAt(0).toUpperCase() + p.slice(1)}</option>
                            ))}
                        </select>
                    </FormField>
                    <FormField id="name" label="Nombre de la VM">
                        <input type="text" id="name" name="name" value={formData.name} onChange={handleChange} required />
                    </FormField>
                    <FormField id="location" label="Región / Ubicación">
                        <input type="text" id="location" name="location" value={formData.location} onChange={handleChange} required />
                    </FormField>
                </fieldset>

                <fieldset>
                    <legend>Recursos de Cómputo</legend>
                    <FormField id="vm_type" label="Tipo de Instancia (Opcional)" hint='Elige un tipo predefinido o "Personalizado" para especificar CPU/RAM manualmente.'>
                        <select id="vm_type" name="vm_type" value={formData.vm_type} onChange={handleInstanceTypeChange}>
                            <option value="">-- Personalizado --</option>
                            {currentInstanceTypes.map(type => (
                                <option key={type.name} value={type.name}>
                                    {type.name} ({type.cpu} vCPU, {type.ram} GB RAM)
                                </option>
                            ))}
                        </select>
                    </FormField>
                    <div className="form-grid">
                        <FormField id="cpu" label="vCPUs">
                            <input type="number" id="cpu" name="cpu" value={formData.cpu} onChange={handleChange} placeholder="Ej: 2"
                                readOnly={!isCustomInstance} className={!isCustomInstance ? 'readonly-input' : ''}
                            />
                        </FormField>
                        <FormField id="ram" label="RAM (GB)">
                            <input type="number" id="ram" name="ram" value={formData.ram} onChange={handleChange} placeholder="Ej: 4"
                                readOnly={!isCustomInstance} className={!isCustomInstance ? 'readonly-input' : ''}
                            />
                        </FormField>
                    </div>
                </fieldset>

                <fieldset>
                    <legend>Almacenamiento</legend>
                    <div className="form-grid">
                        <FormField id="disk_gb" label="Disco (GB)">
                            <input type="number" id="disk_gb" name="disk_gb" value={formData.disk_gb} onChange={handleChange} placeholder="Ej: 50" />
                        </FormField>
                        <FormField id="disk_type" label="Tipo de Disco">
                            <input type="text" id="disk_type" name="disk_type" value={formData.disk_type} onChange={handleChange} placeholder="Ej: ssd, standard" />
                        </FormField>
                    </div>
                </fieldset>

                <fieldset>
                    <legend>Opciones Avanzadas</legend>
                    <FormField id="resource_group" label="Grupo de Recursos (Opcional)">
                        <input type="text" id="resource_group" name="resource_group" value={formData.resource_group} onChange={handleChange} />
                    </FormField>
                    <div className="form-group checkbox-group">
                        <label>
                            <input type="checkbox" name="monitoring" checked={formData.monitoring} onChange={handleChange} />
                            Activar Monitoreo
                        </label>
                        <label>
                            <input type="checkbox" name="optimized" checked={formData.optimized} onChange={handleChange} />
                            Optimización de Disco
                        </label>
                    </div>
                </fieldset>

                <button type="submit" className="submit-button builder" disabled={submitting}>
                    {submitting ? 'Construyendo...' : '🛠️ Construir VM'}
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

export default BuildForm;