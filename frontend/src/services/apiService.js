import axios from 'axios';

// La URL base de tu API backend
const API_URL = 'http://localhost:5000';

/**
 * Obtiene la lista de proveedores disponibles.
 * Corresponde a: GET /api/providers
 */
export const getProviders = async () => {
    try {
        const response = await axios.get(`${API_URL}/api/providers`);
        return response.data;
    } catch (error) {
        console.error("Error fetching providers:", error);
        throw error.response.data || { message: "Error de conexión" };
    }
};

/**
 * Aprovisiona una VM usando el Factory Pattern.
 * Corresponde a: POST /api/vm/provision
 */
export const provisionVm = async (payload) => {
    try {
        const response = await axios.post(`${API_URL}/api/vm/provision`, payload);
        return response.data;
    } catch (error) {
        console.error("Error provisioning VM:", error);
        throw error.response.data || { message: "Error en el aprovisionamiento" };
    }
};

/**
 * Construye una VM personalizada usando el Builder Pattern.
 * Corresponde a: POST /api/vm/build
 */
export const buildVm = async (payload) => {
    try {
        const response = await axios.post(`${API_URL}/api/vm/build`, payload);
        return response.data;
    } catch (error) {
        console.error("Error building VM:", error);
        throw error.response.data || { message: "Error en la construcción" };
    }
};

/**
 * Construye una VM predefinida usando el Director Pattern.
 * Corresponde a: POST /api/vm/build/preset
 */
export const buildPresetVm = async (payload) => {
    try {
        const response = await axios.post(`${API_URL}/api/vm/build/preset`, payload);
        return response.data;
    } catch (error) {
        console.error("Error building preset VM:", error);
        throw error.response.data || { message: "Error en la construcción de preset" };
    }
};

/**
 * Clona una VM desde un prototipo usando el Prototype Pattern.
 * Corresponde a: POST /api/vm/clone
 */
export const cloneVm = async (payload) => {
    try {
        const response = await axios.post(`${API_URL}/api/vm/clone`, payload);
        return response.data;
    } catch (error) {
        console.error("Error cloning VM:", error);
        throw error.response.data || { message: "Error en la clonación" };
    }
};

/**
 * Obtiene la lista de prototipos disponibles.
 * Corresponde a: GET /api/prototypes
 */
export const getPrototypes = async () => {
    try {
        const response = await axios.get(`${API_URL}/api/prototypes`);
        return response.data;
    } catch (error) {
        console.error("Error fetching prototypes:", error);
        throw error.response.data || { message: "Error al obtener prototipos" };
    }
};

/**
 * Obtiene los detalles de un prototipo específico.
 * Corresponde a: GET /api/prototypes/<name>
 */
export const getPrototypeDetails = async (name) => {
    try {
        const response = await axios.get(`${API_URL}/api/prototypes/${name}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching prototype details:", error);
        throw error.response.data || { message: "Error al obtener detalles del prototipo" };
    }
};
