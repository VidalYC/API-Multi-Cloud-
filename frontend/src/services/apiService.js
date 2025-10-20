import axios from 'axios';


const API_URL = 'http://localhost:5000';


export const getProviders = async () => {
    try {
        const response = await axios.get(`${API_URL}/api/providers`);
        return response.data;
    } catch (error) {
        console.error("Error fetching providers:", error);
        throw error.response.data || { message: "Error de conexión" };
    }
};


export const provisionVm = async (payload) => {
    try {
        const response = await axios.post(`${API_URL}/api/vm/provision`, payload);
        return response.data;
    } catch (error) {
        console.error("Error provisioning VM:", error);
        throw error.response.data || { message: "Error en el aprovisionamiento" };
    }
};


export const buildVm = async (payload) => {
    try {
        const response = await axios.post(`${API_URL}/api/vm/build`, payload);
        return response.data;
    } catch (error) {
        console.error("Error building VM:", error);
        throw error.response.data || { message: "Error en la construcción" };
    }
};


export const buildPresetVm = async (payload) => {
    try {
        const response = await axios.post(`${API_URL}/api/vm/build/preset`, payload);
        return response.data;
    } catch (error) {
        console.error("Error building preset VM:", error);
        throw error.response.data || { message: "Error en la construcción de preset" };
    }
};


export const cloneVm = async (payload) => {
    try {
        const response = await axios.post(`${API_URL}/api/vm/clone`, payload);
        return response.data;
    } catch (error) {
        console.error("Error cloning VM:", error);
        throw error.response.data || { message: "Error en la clonación" };
    }
};


export const getPrototypes = async () => {
    try {
        const response = await axios.get(`${API_URL}/api/prototypes`);
        return response.data;
    } catch (error) {
        console.error("Error fetching prototypes:", error);
        throw error.response.data || { message: "Error al obtener prototipos" };
    }
};


export const getPrototypeDetails = async (name) => {
    try {
        const response = await axios.get(`${API_URL}/api/prototypes/${name}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching prototype details:", error);
        throw error.response.data || { message: "Error al obtener detalles del prototipo" };
    }
};
