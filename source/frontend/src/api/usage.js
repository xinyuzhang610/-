import { createApiClient } from './client'
import { getApiBaseUrl } from './baseUrl'
const client = createApiClient(getApiBaseUrl('/usage'))
export const getDashboard = () => client.get('/dashboard')
export const getMyUsage = (page = 1, pageSize = 100) => client.get('/my', { params: { page, page_size: pageSize } })
