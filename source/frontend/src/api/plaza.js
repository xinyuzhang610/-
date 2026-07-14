import { createApiClient } from './client'

const client = createApiClient('/api/plaza')

export const getPlaza = ({ category = '', search = '' } = {}) =>
  client.get('/', { params: { ...(category && { category }), ...(search && { search }) } })
