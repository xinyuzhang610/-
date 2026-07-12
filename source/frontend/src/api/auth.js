import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export const login = (data) => api.post('/auth/login', data)
export const register = (data) => api.post('/auth/register', data)
export const getProfile = (userId) => api.get(`/auth/profile/${userId}`)
