import React, { useState, useEffect } from 'react';
import { getProviders } from '../services/apiService';
import ProvisionForm from './ProvisionForm';
import BuildForm from './BuildForm';
import ResultDisplay from './ResultDisplay';
import '../App.css';

const ToolPage = ({ onBackToHome }) => {
    const [providers, setProviders] = useState([]);
    const [result, setResult] = useState(null);

    useEffect(() => {
        const fetchProviders = async () => {
            try {
                const data = await getProviders();
                const mainProviders = data.filter(p => p !== 'gcp' && p !== 'on-premise');
                setProviders(mainProviders);
            } catch (error) {
                console.error("Error fetching providers:", error);
                setProviders(['aws', 'azure', 'google', 'onpremise']); // Fallback
            }
        };
        fetchProviders();
    }, []);

    const handleResult = (res) => {
        setResult(res);
    };

    return (
        <div className="App">
            <header className="App-header">
                <button onClick={onBackToHome} className="back-button">← Volver al Inicio</button>
                <h1>Panel de Aprovisionamiento de VMs</h1>
            </header>
            <main className="App-main">
                <div className="form-section">
                    <ProvisionForm providers={providers} onResult={handleResult} />
                </div>
                <div className="form-section">
                    <BuildForm providers={providers} onResult={handleResult} />
                </div>
            </main>
            {result && <ResultDisplay result={result} />}
        </div>
    );
};

export default ToolPage;