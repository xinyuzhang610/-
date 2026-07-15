import { createApiClient } from './client'

const client = createApiClient('/api/favorites')
export const listFavorites = (params = {}) => client.get('', { params })
export const addFavorite = (toolId) => client.put(`/${toolId}`)
export const removeFavorite = (toolId) => client.delete(`/${toolId}`)
