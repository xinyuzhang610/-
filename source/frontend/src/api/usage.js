import { createApiClient } from './client'
import { getApiBaseUrl } from './baseUrl'
const client = createApiClient(getApiBaseUrl('/usage'))
export const getDashboard = ({ days = 7, toolId } = {}) => client.get('/dashboard', { params: { days, ...(toolId ? { tool_id: toolId } : {}) } })
export const exportDashboard = ({ days = 7, toolId } = {}) => client.get('/dashboard/export', { params: { days, ...(toolId ? { tool_id: toolId } : {}) }, responseType: 'blob' })
export const getMyUsage = (page = 1, pageSize = 100) => client.get('/my', { params: { page, page_size: pageSize } })
export const getStudentStats = () => client.get('/student-stats')
