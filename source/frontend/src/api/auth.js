import axios from 'axios'

const authClient = axios.create({
  baseURL: '/api/auth',
  timeout: 10000
})

export const login = (credentials) => authClient.post('/login', credentials)
export const register = (profile) => authClient.post('/register', profile)

