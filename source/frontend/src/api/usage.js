import { createApiClient } from './client'
const client = createApiClient('/api/usage')
export const getDashboard = () => client.get('/dashboard')
export const getMyUsage = (page = 1, pageSize = 100) => client.get('/my', { params: { page, page_size: pageSize } })
