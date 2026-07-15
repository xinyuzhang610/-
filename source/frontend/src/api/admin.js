import { createApiClient } from './client'

const client = createApiClient('/api/admin')
export const getAdminUsers = (params = {}) => client.get('/users', { params })
export const updateAdminUser = (id, payload) => client.patch(`/users/${id}`, payload)
export const getRecommendRules = () => client.get('/recommend-rules')
export const createRecommendRule = (payload) => client.post('/recommend-rules', payload)
export const getAuditLogs = (params = {}) => client.get('/audit-logs', { params })
