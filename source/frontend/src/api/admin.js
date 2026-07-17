import { createApiClient } from './client'
import { getApiBaseUrl } from './baseUrl'

const client = createApiClient(getApiBaseUrl('/admin'))
export const getAdminUsers = (params = {}) => client.get('/users', { params })
export const updateAdminUser = (id, payload) => client.patch(`/users/${id}`, payload)
export const getRecommendRules = () => client.get('/recommend-rules')
export const createRecommendRule = (payload) => client.post('/recommend-rules', payload)
export const getAuditLogs = (params = {}) => client.get('/audit-logs', { params })
