import { defineStore } from 'pinia';
import authService from '../services/auth';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: authService.getCurrentUser(),
  }),

  getters: {
    isAuthenticated: (state) => !!state.user,
    getUser: (state) => state.user,
  },

  actions: {
    async login(email, password) {
      try {
        const response = await authService.login(email, password);
        this.user = response;
        return response;
      } catch (error) {
        throw error;
      }
    },

    async register(name, email, password, password_confirmation) {
      try {
        const response = await authService.register(name, email, password, password_confirmation);
        this.user = response;
        return response;
      } catch (error) {
        throw error;
      }
    },

    logout() {
      authService.logout();
      this.user = null;
    },
  },
}); 