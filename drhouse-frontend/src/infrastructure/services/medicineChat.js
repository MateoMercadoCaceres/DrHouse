const API_BASE_URL_DIAGNOSTICS = 'http://localhost:1712/api';

/**
 * Service para información de medicinas
 * @param {string} medicineName - Nombre de la medicina
 * @param {string} mode - Modo de operación (ej: "info")
 * @returns {Promise} - Respuesta de la API
 */
export const medicineService = async (medicineName, mode = 'info') => {
  try {
    const response = await fetch(`${API_BASE_URL_DIAGNOSTICS}/medicines/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ medicine_name: medicineName, mode })
    });

    if (!response.ok) {
      throw new Error(`Error en medicinas: ${response.status} - ${response.statusText}`);
    }

    return await response.json();

  } catch (error) {
    console.error('Error en medicineService!', error);
    throw error;
  }
};

