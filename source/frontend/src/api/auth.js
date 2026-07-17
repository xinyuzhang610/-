import { createApiClient } from './client'
import { getApiBaseUrl } from './baseUrl'

const authClient = createApiClient(getApiBaseUrl('/auth'))

export const login = (credentials) => authClient.post('/login', credentials)
export const register = (profile) => authClient.post('/register', profile)
