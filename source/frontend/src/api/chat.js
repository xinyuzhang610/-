import { createApiClient } from './client'

const client = createApiClient('/api/chat', 15000)

export const sendChat = (payload) => client.post('/', payload)
