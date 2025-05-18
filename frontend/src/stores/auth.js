import { defineStore } from 'pinia';
import { api } from 'src/boot/axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user')) || null,
    token: localStorage.getItem('token') || null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    getUser: (state) => state.user,
  },

  actions: {
    async login(credentials) {
      try {
        const response = await api.post('/login', credentials);
        this.setAuth(response.data);
        return response;
      } catch (error) {
        throw error;
      }
    },

    async register(userData) {
      try {
        const response = await api.post('/register', userData);
        this.setAuth(response.data);
        return response;
      } catch (error) {
        throw error;
      }
    },

    async logout() {
      try {
        await api.post('/logout');
      } catch (error) {
        console.error('Logout error:', error);
      } finally {
        this.clearAuth();
      }
    },

    setAuth(data) {
      this.token = data.token;
      this.user = data.user;
      localStorage.setItem('token', data.token);
      localStorage.setItem('user', JSON.stringify(data.user));
    },

    clearAuth() {
      this.token = null;
      this.user = null;
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  },
}); 