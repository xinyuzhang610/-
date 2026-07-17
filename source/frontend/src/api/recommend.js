import { createApiClient } from './client'
import { getApiBaseUrl } from './baseUrl'
const client = createApiClient(getApiBaseUrl('/recommend'))
export const getRecommendation = (payload) => client.post('/', payload)
