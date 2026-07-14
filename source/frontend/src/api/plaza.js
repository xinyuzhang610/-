import axios from 'axios'

const client = axios.create({ baseURL: '/api/plaza', timeout: 10000 })

export const getPlaza = ({ category = '', search = '' } = {}) =>
  client.get('/', { params: { ...(category && { category }), ...(search && { search }) } })
