import axios from 'axios'

const client = axios.create({ baseURL: '/api/chat', timeout: 15000 })

export const sendChat = (payload) => client.post('/', payload)
