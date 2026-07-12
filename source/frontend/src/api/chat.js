import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000
})

export const sendMessage = (data) =>
  api.post('/chat/', data)
