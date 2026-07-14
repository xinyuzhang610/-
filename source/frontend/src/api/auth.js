import { createApiClient } from './client'

const authClient = createApiClient('/api/auth')

export const login = (credentials) => authClient.post('/login', credentials)
export const register = (profile) => authClient.post('/register', profile)
