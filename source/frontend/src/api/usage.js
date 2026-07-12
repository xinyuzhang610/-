import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export const getMyUsage = (userId, limit = 20) =>
  api.get('/usage/my', { params: { user_id: userId, limit } })

export const getToolUsage = (toolId) =>
  api.get(`/usage/tool/${toolId}`)

export const getDashboard = () =>
  api.get('/usage/dashboard')
