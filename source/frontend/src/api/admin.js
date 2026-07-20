import { createApiClient } from './client'
import { getApiBaseUrl } from './baseUrl'

const client = createApiClient(getApiBaseUrl('/admin'))
export const getAdminUsers = (params = {}) => client.get('/users', { params })
export const updateAdminUser = (id, payload) => client.patch(`/users/${id}`, payload)
export const setAdminToolPlazaStatus = (id, status) => client.patch(`/tools/${id}/plaza`, { plaza_status: status })
export const getRecommendRules = () => client.get('/recommend-rules')
export const createRecommendRule = (payload) => client.post('/recommend-rules', payload)
export const updateRecommendRule = (id, payload) => client.patch(`/recommend-rules/${id}`, payload)
export const deleteRecommendRule = (id) => client.delete(`/recommend-rules/${id}`)
export const getAuditLogs = (params = {}) => client.get('/audit-logs', { params })
export const exportAuditLogs = () => client.get('/audit-logs/export', { responseType: 'blob' })
