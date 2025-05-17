import axios from 'axios';

// Configurazione separata per Sanctum e API
const sanctumClient = axios.create({
  baseURL: '/',  // Base URL diverso per Sanctum
  withCredentials: true,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
});

const apiClient = axios.create({
  baseURL: '/api',  // Prefisso API normale
  withCredentials: true,
  headers: {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
  }
});

const authService = {
  async login(email, password) {
    try {
      // Prima chiamata a Sanctum (senza /api)
      await sanctumClient.get('/sanctum/csrf-cookie');
      
      // Chiamata API normale (con /api)
      const response = await apiClient.post('/login', { email, password });

      if (response.data.token) {
        localStorage.setItem('auth_token', response.data.token);
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`;
      }
      return response.data;

    } catch (error) {
      throw new Error(error.response?.data?.message || 'Login failed');
    }
  },

  async register(name, email, password, password_confirmation) {
    try {
      await sanctumClient.get('/sanctum/csrf-cookie');
      const response = await apiClient.post('/register', {
        name, email, password, password_confirmation
      });

      if (response.data.token) {
        localStorage.setItem('auth_token', response.data.token);
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${response.data.token}`;
      }
      return response.data;

    } catch (error) {
      throw new Error(error.response?.data?.message || 'Registration failed');
    }
  },

  logout() {
    return apiClient.post('/logout')
      .then(() => {
        localStorage.removeItem('auth_token');
        delete apiClient.defaults.headers.common['Authorization'];
      });
  },

  getCurrentUser() {
    const token = localStorage.getItem('auth_token');
    return token ? { token } : null;
  }
};

export default authService;