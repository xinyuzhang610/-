import { describe, expect, it } from 'vitest'
import { getApiBaseUrl, getApiUrl } from './baseUrl'

describe('API base URL utility', () => {
  it('returns /api when VITE_API_BASE_URL is not set', () => {
    // In test environment, VITE_API_BASE_URL is typically not set
    expect(getApiBaseUrl()).toBe('/api')
  })

  it('appends path segment correctly', () => {
    expect(getApiBaseUrl('/chat/stream')).toBe('/api/chat/stream')
  })

  it('normalizes path without leading slash', () => {
    expect(getApiBaseUrl('chat/stream')).toBe('/api/chat/stream')
  })

  it('does not produce //api', () => {
    expect(getApiBaseUrl()).not.toContain('//api')
  })

  it('getApiUrl returns full endpoint URL', () => {
    expect(getApiUrl('/auth/login')).toBe('/api/auth/login')
  })

  it('getApiUrl with path', () => {
    expect(getApiUrl('/chat/stream')).toBe('/api/chat/stream')
  })
})
