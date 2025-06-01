import { api } from '../boot/axios'

const apiService = {
  // Operazioni sui dispositivi
  async getDevices() {
    const response = await api.get('/devices')
    return response.data
  },

  async getDevice(id) {
    const response = await api.get(`/devices/${id}`)
    return response.data
  },

  async createDevice(deviceData) {
    const response = await api.post('/devices', deviceData)
    return response.data
  },

  async updateDevice(id, deviceData) {
    const response = await api.put(`/devices/${id}`, deviceData)
    return response.data
  },

  async deleteDevice(id) {
    const response = await api.delete(`/devices/${id}`)
    return response.data
  },

  // Operazioni sugli utenti
  async getCurrentUser() {
    const response = await api.get('/user')
    return response.data
  },

  async updateUser(userData) {
    const response = await api.put('/user', userData)
    return response.data
  },

  // Operazioni sulle stanze
  async getRooms() {
    const response = await api.get('/rooms')
    return response.data
  },

  async createRoom(roomData) {
    const response = await api.post('/rooms', roomData)
    return response.data
  },

  async updateRoom(id, roomData) {
    const response = await api.put(`/rooms/${id}`, roomData)
    return response.data
  },

  async deleteRoom(id) {
    const response = await api.delete(`/rooms/${id}`)
    return response.data
  }
}

export default apiService 