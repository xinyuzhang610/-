import { createApiClient } from './client'
const client = createApiClient('/api/recommend')
export const getRecommendation = (payload) => client.post('/', payload)
