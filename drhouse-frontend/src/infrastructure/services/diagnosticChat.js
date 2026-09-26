import CookiesService from '../uitls/cookiesService';

const API_BASE_URL_DIAGNOSTICS = 'http://localhost:1712/api';

/**
 * Service para diagnósticos médicos
 * @param {string} userInput - Texto ingresado por el usuario
 * @param {string} mode - Modo de operación (ej: "diagnose", "symptoms", "explain")
 * @returns {Promise} - Respuesta de la API
 */
export const diagnosticService = async (userInput, mode = 'diagnose') => {  
  try {
    // Intentar obtener token de diferentes fuentes
    let token = CookiesService.get('authToken') || 
                CookiesService.get('token') || 
                CookiesService.get('access_token') ||
                localStorage.getItem('authToken') ||
                localStorage.getItem('token') ||
                localStorage.getItem('access_token');
    
    // Headers base
    const headers = {
      'Content-Type': 'application/json'
    };
    
    // Añadir Authorization solo si hay token
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    } else {
      console.warn('No se encontró token de autenticación, enviando sin autorización');
    }

    // Log para debug
    console.log('Enviando petición a:', `${API_BASE_URL_DIAGNOSTICS}/diagnostics/`);
    console.log('Headers:', headers);
    console.log('Body:', { user_input: userInput, mode: mode });

    const response = await fetch(`${API_BASE_URL_DIAGNOSTICS}/diagnostics/`, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({ 
        user_input: userInput, 
        mode: mode 
      })
    });

    console.log('Response status:', response.status);
    console.log('Response ok:', response.ok);
    console.log('Response headers:', response.headers);

    if (!response.ok) {
      // Intentar obtener el mensaje de error del servidor
      let errorMessage;
      try {
        const errorData = await response.json();
        errorMessage = errorData.message || errorData.error || errorData.detail || 'Error desconocido';
        console.error('Error del servidor:', errorData);
      } catch (parseError) {
        // Si no se puede parsear el JSON, usar el texto de respuesta
        try {
          errorMessage = await response.text();
        } catch (textError) {
          errorMessage = `${response.status} - ${response.statusText}`;
        }
      }
      
      if (response.status === 401) {
        throw new Error('Token de autenticación inválido o expirado');
      } else if (response.status === 500) {
        throw new Error(`Error interno del servidor: ${errorMessage}`);
      } else {
        throw new Error(`Error en diagnósticos: ${response.status} - ${errorMessage}`);
      }
    }

    // AQUÍ ESTÁ EL CAMBIO PRINCIPAL - Agregar logs para ver qué devuelve el backend
    const responseData = await response.json();
    console.log('Respuesta completa del backend:', responseData);
    console.log('Tipo de responseData:', typeof responseData);
    console.log('Claves en responseData:', Object.keys(responseData));
    
    // Verificar diferentes posibles estructuras de respuesta
    if (responseData.response) {
      console.log('Usando responseData.response:', responseData.response);
    } else if (responseData.message) {
      console.log('Usando responseData.message:', responseData.message);
    } else if (responseData.data) {
      console.log('Usando responseData.data:', responseData.data);
    } else if (responseData.result) {
      console.log('Usando responseData.result:', responseData.result);
    } else {
      console.log('Estructura de respuesta no reconocida, devolviendo objeto completo');
    }

    return responseData;

  } catch (error) {
    console.error('Error en diagnosticService:', error);
    throw error;
  }
};