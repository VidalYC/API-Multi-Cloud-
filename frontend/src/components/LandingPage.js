import React from 'react';
import { motion } from 'framer-motion';
import { FaCloud, FaTools, FaRocket, FaAws, FaMicrosoft, FaGoogle, FaServer } from 'react-icons/fa';
import './LandingPage.css';

const LandingPage = ({ onStart }) => {
    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.2,
                delayChildren: 0.1
            }
        }
    };

    const itemVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: {
            opacity: 1,
            y: 0,
            transition: { duration: 0.6, ease: "easeOut" }
        }
    };

    const floatVariants = {
        animate: {
            y: [0, -10, 0],
            transition: {
                duration: 3,
                repeat: Infinity,
                ease: "easeInOut"
            }
        }
    };

    return (
        <div className="landing-container">
            
            <div className="background-shapes">
                <div className="shape shape-1"></div>
                <div className="shape shape-2"></div>
                <div className="shape shape-3"></div>
            </div>

            <motion.div
                className="landing-content"
                variants={containerVariants}
                initial="hidden"
                animate="visible"
            >
                
                <motion.header className="hero-section" variants={itemVariants}>
                    <motion.div
                        className="hero-icon"
                        variants={floatVariants}
                        animate="animate"
                    >
                        <FaCloud size={80} />
                    </motion.div>
                    <h1>API de Aprovisionamiento Multi-Cloud</h1>
                    <p className="subtitle">
                        Implementando Patrones de Diseño <strong>Factory</strong> y <strong>Builder</strong> con Principios <strong>SOLID</strong>
                    </p>
                    <div className="hero-badges">
                        <span className="badge">🏗️ Clean Architecture</span>
                        <span className="badge">⚡ REST API</span>
                        <span className="badge">🔄 Multi-Cloud</span>
                    </div>
                </motion.header>

                
                <motion.section className="providers-section" variants={itemVariants}>
                    <h2>Proveedores Soportados</h2>
                    <div className="providers-grid">
                        <motion.div
                            className="provider-card"
                            whileHover={{ scale: 1.05, rotate: 2 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            <FaAws size={50} color="#FF9900" />
                            <h3>Amazon AWS</h3>
                            <p>EC2, VPC, EBS</p>
                        </motion.div>
                        <motion.div
                            className="provider-card"
                            whileHover={{ scale: 1.05, rotate: -2 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            <FaMicrosoft size={50} color="#00A4EF" />
                            <h3>Microsoft Azure</h3>
                            <p>Virtual Machines, VNet</p>
                        </motion.div>
                        <motion.div
                            className="provider-card"
                            whileHover={{ scale: 1.05, rotate: 2 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            <FaGoogle size={50} color="#4285F4" />
                            <h3>Google Cloud</h3>
                            <p>Compute Engine, VPC</p>
                        </motion.div>
                        <motion.div
                            className="provider-card"
                            whileHover={{ scale: 1.05, rotate: -2 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            <FaServer size={50} color="#6366f1" />
                            <h3>On-Premise</h3>
                            <p>Datacenter, VMware</p>
                        </motion.div>
                    </div>
                </motion.section>

                
                <motion.section className="features-section" variants={itemVariants}>
                    <h2>Características Principales</h2>
                    <div className="features-grid">
                        <motion.div
                            className="feature-card"
                            whileHover={{ y: -10 }}
                            transition={{ duration: 0.3 }}
                        >
                            <div className="feature-icon">
                                <FaRocket size={40} />
                            </div>
                            <h3>Provisión Rápida</h3>
                            <p>Factory Pattern para crear VMs con configuración estándar en segundos</p>
                        </motion.div>
                        <motion.div
                            className="feature-card"
                            whileHover={{ y: -10 }}
                            transition={{ duration: 0.3 }}
                        >
                            <div className="feature-icon">
                                <FaTools size={40} />
                            </div>
                            <h3>Construcción Personalizada</h3>
                            <p>Builder Pattern para configurar cada detalle de tu infraestructura</p>
                        </motion.div>
                        <motion.div
                            className="feature-card"
                            whileHover={{ y: -10 }}
                            transition={{ duration: 0.3 }}
                        >
                            <div className="feature-icon">
                                📚
                            </div>
                            <h3>Plantillas Predefinidas</h3>
                            <p>Director Pattern con configuraciones optimizadas para casos de uso comunes</p>
                        </motion.div>
                    </div>
                </motion.section>

                
                <motion.section className="patterns-section" variants={itemVariants}>
                    <h2>Patrones de Diseño Implementados</h2>
                    <div className="patterns-grid">
                        <motion.div
                            className="pattern-card"
                            whileHover={{ scale: 1.03 }}
                        >
                            <div className="pattern-number">01</div>
                            <h3>🏭 Factory Method</h3>
                            <p>
                                Encapsula la lógica de creación de proveedores cloud. 
                                Permite agregar nuevos proveedores sin modificar código existente (OCP).
                            </p>
                            <ul>
                                <li>✓ Abstracción de creación</li>
                                <li>✓ Extensibilidad</li>
                                <li>✓ Bajo acoplamiento</li>
                            </ul>
                        </motion.div>
                        <motion.div
                            className="pattern-card"
                            whileHover={{ scale: 1.03 }}
                        >
                            <div className="pattern-number">02</div>
                            <h3>🛠️ Builder</h3>
                            <p>
                                Construcción paso a paso de VMs complejas con validación de región.
                                Separa la construcción de la representación.
                            </p>
                            <ul>
                                <li>✓ Construcción flexible</li>
                                <li>✓ Configuración granular</li>
                                <li>✓ Validación integrada</li>
                            </ul>
                        </motion.div>
                        <motion.div
                            className="pattern-card"
                            whileHover={{ scale: 1.03 }}
                        >
                            <div className="pattern-number">03</div>
                            <h3>📐 Director</h3>
                            <p>
                                Define algoritmos de construcción para VMs estándar, optimizadas en memoria
                                y optimizadas en disco según especificaciones del documento.
                            </p>
                            <ul>
                                <li>✓ Configuraciones predefinidas</li>
                                <li>✓ Mejores prácticas</li>
                                <li>✓ Consistencia</li>
                            </ul>
                        </motion.div>
                    </div>
                </motion.section>

                
                <motion.section className="cta-section" variants={itemVariants}>
                    <motion.div
                        className="cta-content"
                        whileHover={{ scale: 1.02 }}
                    >
                        <h2>¿Listo para Comenzar?</h2>
                        <p>Experimenta el poder de los patrones de diseño en acción</p>
                        <motion.button
                            className="cta-button"
                            onClick={onStart}
                            whileHover={{ scale: 1.05 }}
                            whileTap={{ scale: 0.95 }}
                        >
                            <FaRocket /> Ir a la Herramienta de Aprovisionamiento
                        </motion.button>
                    </motion.div>
                </motion.section>

                
                <motion.footer className="landing-footer" variants={itemVariants}>
                    <p>🎓 Universidad Popular del Cesar - Ingeniería de Software</p>
                    <p className="tech-stack">Desarrollado con Python Flask + React + Design Patterns</p>
                </motion.footer>
            </motion.div>
        </div>
    );
};

export default LandingPage;