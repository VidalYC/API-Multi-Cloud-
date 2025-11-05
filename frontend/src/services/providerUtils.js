/**
 * Normaliza el nombre del proveedor para usarlo como clave en objetos.
 * Maneja alias como 'gcp' -> 'google' y 'on-premise' -> 'onpremise'.
 * @param {string} provider - El nombre del proveedor desde el formulario.
 * @returns {string} La clave normalizada del proveedor.
 */
export const getProviderKey = (provider) => {
    if (provider === 'gcp') return 'google';
    if (provider === 'on-premise') return 'onpremise';
    return provider;
};