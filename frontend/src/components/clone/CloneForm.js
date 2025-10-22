import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaCopy, FaInfoCircle } from 'react-icons/fa';
import { cloneVm, getPrototypes, getPrototypeDetails } from '../../services/apiService';
import './CloneForm.css';

const CloneForm = ({ onSubmit }) => {
  const [prototypeName, setPrototypeName] = useState('');
  const [newVmName, setNewVmName] = useState('');
  const [availablePrototypes, setAvailablePrototypes] = useState([]);
  const [selectedPrototype, setSelectedPrototype] = useState(null);
  const [showCustomizations, setShowCustomizations] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

 
  const [customVcpus, setCustomVcpus] = useState('');
  const [customMemory, setCustomMemory] = useState('');
  const [customRegion, setCustomRegion] = useState('');

  
  useEffect(() => {
    fetchPrototypesData();
  }, []);

  const fetchPrototypesData = async () => {
    try {
      const data = await getPrototypes();
      if (data.success) {
        setAvailablePrototypes(data.prototypes);
      }
    } catch (error) {
      console.error('Error fetching prototypes:', error);
    }
  };

  const handlePrototypeChange = async (e) => {
    const name = e.target.value;
    setPrototypeName(name);

    if (name) {
      try {
        const data = await getPrototypeDetails(name);
        if (data.success) {
          setSelectedPrototype(data.prototype);
          
          setCustomVcpus(data.prototype.vcpus.toString());
          setCustomMemory(data.prototype.memoryGB.toString());
          setCustomRegion(data.prototype.network?.region || '');
        }
      } catch (error) {
        console.error('Error fetching prototype details:', error);
      }
    } else {
      setSelectedPrototype(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const customizations = {};

      if (showCustomizations) {
        if (customVcpus && customVcpus !== selectedPrototype?.vcpus.toString()) {
          customizations.vcpus = parseInt(customVcpus);
        }
        if (customMemory && customMemory !== selectedPrototype?.memoryGB.toString()) {
          customizations.memoryGB = parseInt(customMemory);
        }
        if (customRegion && customRegion !== selectedPrototype?.network?.region) {
          customizations.region = customRegion;
        }
      }

      const payload = {
        prototype_name: prototypeName,
        new_vm_name: newVmName,
        customizations: Object.keys(customizations).length > 0 ? customizations : undefined
      };

      const result = await cloneVm(payload);
      onSubmit(result);

      
      if (result.success) {
        setPrototypeName('');
        setNewVmName('');
        setSelectedPrototype(null);
        setShowCustomizations(false);
      }
    } catch (error) {
      onSubmit({
        success: false,
        message: error.message || 'Error al clonar la VM',
        error_detail: error.error || 'Error desconocido'
      });
    } finally {
      setIsLoading(false);
    }
  };

  const getProviderBadgeClass = (provider) => {
    const classes = {
      aws: 'provider-badge-aws',
      azure: 'provider-badge-azure',
      google: 'provider-badge-google',
      onpremise: 'provider-badge-onpremise'
    };
    return classes[provider] || 'provider-badge-default';
  };

  return (
    <motion.div
      className="clone-form-container"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="form-header">
        <FaCopy className="header-icon" />
        <h2>Clonar desde Prototipo</h2>
        <p className="form-subtitle">
          Crea VMs basadas en configuraciones predefinidas
        </p>
      </div>

      <form onSubmit={handleSubmit} className="clone-form">
        
        <div className="form-group">
          <label htmlFor="prototype">
            Prototipo <span className="required">*</span>
          </label>
          <select
            id="prototype"
            value={prototypeName}
            onChange={handlePrototypeChange}
            required
            disabled={isLoading}
            className="form-select"
          >
            <option value="">Selecciona un prototipo...</option>
            {availablePrototypes.map((proto) => (
              <option key={proto.name} value={proto.name}>
                {proto.description} ({proto.provider.toUpperCase()})
              </option>
            ))}
          </select>
          <small className="form-hint">
            Selecciona una configuración base para clonar
          </small>
        </div>

        
        {selectedPrototype && (
          <motion.div
            className="prototype-details-card"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            transition={{ duration: 0.3 }}
          >
            <h4>
              <FaInfoCircle /> Detalles del Prototipo
            </h4>
            <div className="prototype-info-grid">
              <div className="info-item">
                <span className="info-label">Proveedor:</span>
                <span className={`provider-badge ${getProviderBadgeClass(selectedPrototype.provider)}`}>
                  {selectedPrototype.provider.toUpperCase()}
                </span>
              </div>
              <div className="info-item">
                <span className="info-label">Tipo de Instancia:</span>
                <span className="info-value">{selectedPrototype.instance_type}</span>
              </div>
              <div className="info-item">
                <span className="info-label">vCPUs:</span>
                <span className="info-value">{selectedPrototype.vcpus}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Memoria:</span>
                <span className="info-value">{selectedPrototype.memoryGB} GB</span>
              </div>
              <div className="info-item">
                <span className="info-label">Región:</span>
                <span className="info-value">{selectedPrototype.network?.region}</span>
              </div>
              <div className="info-item">
                <span className="info-label">Disco:</span>
                <span className="info-value">
                  {selectedPrototype.disks?.[0]?.size_gb} GB ({selectedPrototype.disks?.[0]?.disk_type})
                </span>
              </div>
            </div>
          </motion.div>
        )}

        
        <div className="form-group">
          <label htmlFor="vmName">
            Nombre de la Nueva VM <span className="required">*</span>
          </label>
          <input
            type="text"
            id="vmName"
            value={newVmName}
            onChange={(e) => setNewVmName(e.target.value)}
            placeholder="ej: web-server-prod-01"
            required
            disabled={isLoading}
            className="form-input"
          />
          <small className="form-hint">
            Nombre único para identificar la VM clonada
          </small>
        </div>

        
        {selectedPrototype && (
          <div className="customizations-toggle">
            <label className="toggle-label">
              <input
                type="checkbox"
                checked={showCustomizations}
                onChange={(e) => setShowCustomizations(e.target.checked)}
                disabled={isLoading}
              />
              <span>Personalizar configuración</span>
            </label>
          </div>
        )}

        
        {showCustomizations && selectedPrototype && (
          <motion.div
            className="customizations-section"
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            transition={{ duration: 0.3 }}
          >
            <h4>Personalización Opcional</h4>
            <div className="customizations-grid">
              <div className="form-group">
                <label htmlFor="customVcpus">vCPUs</label>
                <input
                  type="number"
                  id="customVcpus"
                  value={customVcpus}
                  onChange={(e) => setCustomVcpus(e.target.value)}
                  min="1"
                  max="128"
                  disabled={isLoading}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label htmlFor="customMemory">Memoria (GB)</label>
                <input
                  type="number"
                  id="customMemory"
                  value={customMemory}
                  onChange={(e) => setCustomMemory(e.target.value)}
                  min="1"
                  max="1024"
                  disabled={isLoading}
                  className="form-input"
                />
              </div>

              <div className="form-group">
                <label htmlFor="customRegion">Región</label>
                <input
                  type="text"
                  id="customRegion"
                  value={customRegion}
                  onChange={(e) => setCustomRegion(e.target.value)}
                  placeholder={selectedPrototype.network?.region}
                  disabled={isLoading}
                  className="form-input"
                />
                <small className="form-hint">
                  Cambiar región clonará red y disco a la nueva región
                </small>
              </div>
            </div>
          </motion.div>
        )}

        
        <motion.button
          type="submit"
          className="submit-button"
          disabled={isLoading || !prototypeName || !newVmName}
          whileHover={!isLoading ? { scale: 1.02 } : {}}
          whileTap={!isLoading ? { scale: 0.98 } : {}}
        >
          {isLoading ? (
            <>
              <div className="spinner"></div>
              Clonando VM...
            </>
          ) : (
            <>
              <FaCopy /> Clonar VM
            </>
          )}
        </motion.button>
      </form>

      
      
    </motion.div>
  );
};

export default CloneForm;
