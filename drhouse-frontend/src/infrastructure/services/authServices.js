// src/infrastructure/services/authServices.js
import CookiesService from '../uitls/cookiesService';

const API_BASE_URL = 'http://localhost:1712/api/users';

const authService = {
  login: async (username, password) => {
    try {
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password })
      });

      if (!response.ok) {
        throw new Error('Credenciales inválidas');
      }

      const data = await response.json();

      // Guardamos el access_token en la cookie
      if (data.access_token) {
        CookiesService.set('token', data.access_token);
      } else {
        console.error("Respuesta sin access_token.");
      }

      return data;
    } catch (error) {
      console.error('Error en login!', error);
      throw error;
    }
  },

  register: async (username, email, full_name, password) => {
    try {
      const response = await fetch(`${API_BASE_URL}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          username, 
          email, 
          full_name, 
          password 
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Error en el registro');
      }

      const data = await response.json();

      // Si el registro también proporciona un access_token, guárdalo
      if (data.access_token) {
        CookiesService.set('token', data.access_token);
      }

      return data;
    } catch (error) {
      console.error('Error en registro!', error);
      throw error;
    }
  },

  logout: () => {
    CookiesService.remove('token');
  },

  isAuthenticated: () => {
    return !!CookiesService.get('token');
  },

  getToken: () => {
    return CookiesService.get('token');
  },

  // Método para obtener información del usuario autenticado
  getUserInfo: async () => {
    try {
      const token = CookiesService.get('token');
      if (!token) {
        throw new Error('No hay token de autenticación');
      }

      const response = await fetch(`${API_BASE_URL}/profile`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`
        },
      });

      if (!response.ok) {
        throw new Error('Error al obtener información del usuario');
      }

      return await response.json();
    } catch (error) {
      console.error('Error obteniendo info del usuario!', error);
      throw error;
    }
  },
}

export default authService;
