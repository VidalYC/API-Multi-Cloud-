import React, { useState, useEffect } from 'react';
import { getProviders } from './services/apiService';
import './App.css'; // Necesitaremos algunos estilos
import ProvisionForm from './components/ProvisionForm';
import BuildForm from './components/BuildForm'; // Importamos el formulario Builder
import PresetForm from './components/PresetForm'; // Importamos el formulario Director
import ResultDisplay from './components/ResultDisplay';

function App() {
    const [activeTab, setActiveTab] = useState('quick'); // 'quick', 'custom', 'template'
    const [providers, setProviders] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [result, setResult] = useState(null);

    // Cargar los proveedores cuando el componente se monta
    useEffect(() => {
        const fetchProviders = async () => {
            try {
                const data = await getProviders();
                // Filtramos los alias para no repetirlos en el selector
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
    };

    const renderContent = () => {
        // Aquí irían los formularios reales
        if (activeTab === 'quick') {
            return <ProvisionForm providers={providers} onResult={handleResult} />;
        }
        if (activeTab === 'custom') {
            return <BuildForm providers={providers} onResult={handleResult} />; // Usamos el componente
        }
        if (activeTab === 'template') {
            return <PresetForm providers={providers} onResult={handleResult} />; // Usamos el componente
        }
    };

    return (
        <div className="container">
            <header>
                <h1>🚀 Aprovisionamiento de VMs Multi-Cloud</h1>
                <p>Una interfaz unificada para desplegar máquinas virtuales en diferentes proveedores de nube.</p>
            </header>

            <div className="tabs">
                <button onClick={() => setActiveTab('quick')} className={activeTab === 'quick' ? 'active' : ''}>
                    ⚡ Provisión Rápida
                </button>
                <button onClick={() => setActiveTab('custom')} className={activeTab === 'custom' ? 'active' : ''}>
                    🛠️ Construcción Personalizada
                </button>
                <button onClick={() => setActiveTab('template')} className={activeTab === 'template' ? 'active' : ''}>
                    📚 Usar Plantilla
                </button>
            </div>

            <main>
                {loading && <p>Cargando proveedores...</p>}
                {error && <div className="error-message">{error}</div>}
                {!loading && !error && renderContent()}
            </main>

            <ResultDisplay result={result} />
        </div>
    );
}

export default App;
