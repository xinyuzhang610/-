import axios from 'axios'

export function createApiClient(baseURL, timeout = 10000) {
  const client = axios.create({ baseURL, timeout })
  client.interceptors.request.use((config) => {
    const token = localStorage.getItem('token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
  })
  return client
}

export default createApiClient('/api')
