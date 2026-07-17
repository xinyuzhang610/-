import { createApiClient } from './client'
import { getApiBaseUrl } from './baseUrl'

const client = createApiClient(getApiBaseUrl('/favorites'))
export const listFavorites = (params = {}) => client.get('', { params })
export const addFavorite = (toolId) => client.put(`/${toolId}`)
export const removeFavorite = (toolId) => client.delete(`/${toolId}`)
