import { createApiClient } from './client'
import { getApiBaseUrl } from './baseUrl'

const client = createApiClient(getApiBaseUrl('/plaza'))

export const getPlaza = ({ category = '', search = '' } = {}) =>
  client.get('/', { params: { ...(category && { category }), ...(search && { search }) } })
