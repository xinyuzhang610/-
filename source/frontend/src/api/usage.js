import axios from 'axios'
const client = axios.create({ baseURL: '/api/usage', timeout: 10000 })
export const getDashboard = () => client.get('/dashboard')
export const getMyUsage = (userId, limit = 100) => client.get('/my', { params: { user_id: userId, limit } })
