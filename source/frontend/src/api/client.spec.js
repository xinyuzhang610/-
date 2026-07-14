import { describe, expect, it } from 'vitest'

describe('API client authentication', () => {
  it('adds the saved bearer token to every API request', async () => {
    localStorage.setItem('token', 'session-token')
    const { createApiClient } = await import('./client.js')
    const client = createApiClient('/api/test')
    const interceptor = client.interceptors.request.handlers.find(Boolean)

    expect(interceptor.fulfilled({ headers: {} }).headers.Authorization).toBe('Bearer session-token')
  })
})
