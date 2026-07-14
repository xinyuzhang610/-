import { createApiClient } from './client'
const client = createApiClient('/api/usage')
export const getDashboard = () => client.get('/dashboard')
export const getMyUsage = (limit = 100) => client.get('/my', { params: { limit } })
