import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export const getPresetTools = (category) =>
  api.get('/tools/presets', { params: { category } })

export const getTool = (id) =>
  api.get(`/tools/${id}`)

export const createTool = (data, creatorId) =>
  api.post('/tools/', data, { params: { creator_id: creatorId } })

export const updateTool = (id, data) =>
  api.put(`/tools/${id}`, data)

export const deleteTool = (id) =>
  api.delete(`/tools/${id}`)

export const getShareLink = (id) =>
  api.get(`/tools/${id}/share`)
