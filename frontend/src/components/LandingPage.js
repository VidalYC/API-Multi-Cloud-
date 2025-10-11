import React from 'react';
import './LandingPage.css'; // Estilos específicos para la landing

const LandingPage = ({ onStart }) => {
    return (
        <div className="landing-container">
            <header className="landing-header">
                <h1>🚀 API de Aprovisionamiento Multi-Cloud</h1>
                <p className="subtitle">
                    Implementando Patrones de Diseño Factory y Builder con Principios SOLID.
                </p>
            </header>

            <main className="landing-main">
                <section className="feature-section">
                    <h2>¿Qué es este proyecto?</h2>
                    <p>
                        Una API REST robusta que unifica la creación de máquinas virtuales (VMs)
                        a través de múltiples proveedores de nube como <strong>AWS, Azure, Google Cloud</strong> y
                        soluciones <strong>On-Premise</strong>.
                    </p>
                </section>

                <section className="patterns-section">
                    <h2>Patrones en Acción</h2>
                    <div className="patterns-grid">
                        <div className="pattern-card">
                            <h3>🏭 Factory Pattern</h3>
                            <p>Para aprovisionamiento rápido y estandarizado. Ideal para crear VMs con configuraciones predeterminadas del proveedor de forma instantánea.</p>
                        </div>
                        <div className="pattern-card">
                            <h3>🛠️ Builder Pattern</h3>
                            <p>Para construcción flexible y detallada. Permite configurar cada aspecto de tu VM paso a paso, perfecto para entornos complejos.</p>
                        </div>
                    </div>
                </section>

                <section className="cta-section">
                    <h2>¡Pruébalo ahora!</h2>
                    <p>Experimenta la flexibilidad de aprovisionar y construir VMs a través de una interfaz unificada.</p>
                    <button onClick={onStart} className="cta-button">
                        Ir a la Herramienta de Aprovisionamiento
                    </button>
                </section>
            </main>

            <footer className="landing-footer">
                <p>Universidad Popular del Cesar - Especialización en Ingeniería de Software</p>
            </footer>
        </div>
    );
};

export default LandingPage;