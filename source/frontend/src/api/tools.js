import axios from 'axios'
const client = axios.create({ baseURL: '/api/tools', timeout: 10000 })
export const getPresetTools = (category) => client.get('/presets', { params: category ? { category } : {} })
export const deleteTool = (id) => client.delete(`/${id}`)
export const getShareLink = (id) => client.get(`/${id}/share`)

