import { createApiClient } from './client'
import { getApiBaseUrl } from './baseUrl'

const client = createApiClient(getApiBaseUrl('/plaza'))

export const getPlaza = ({ category = '', search = '', sort = 'hot', page = 1, pageSize = 20 } = {}) =>
  client.get('/', { params: {
    ...(category && { category }),
    ...(search && { search }),
    sort,
    page,
    page_size: pageSize,
  } })
