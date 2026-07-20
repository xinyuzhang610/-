/**
 * Unified API base URL utility.
 *
 * Behavior:
 * - When VITE_API_BASE_URL is not set, returns '/api' (relative path for local dev proxy).
 * - When VITE_API_BASE_URL is set, returns the absolute backend origin + '/api'.
 * - Trims trailing slashes from the origin.
 * - Always ensures the result starts with '/' for relative paths or 'https://' for absolute.
 * - Never produces double '/api/api' or '//api'.
 */

const TRAILING_SLASH_RE = /\/+$/

/**
 * Get the API base URL.
 * @param {string} [path=''] - Optional path segment to append (e.g., '/chat/stream').
 * @returns {string} The full API base URL.
 */
export function getApiBaseUrl(path = '') {
  const envBase = import.meta.env?.VITE_API_BASE_URL

  let base
  if (envBase && envBase.trim()) {
    // Absolute backend origin — strip trailing slash, then append /api
    const origin = envBase.trim().replace(TRAILING_SLASH_RE, '')
    base = `${origin}/api`
  } else {
    // Local dev — use relative path, Vite proxy forwards to localhost:8000
    base = '/api'
  }

  if (path) {
    // Ensure path starts with '/'
    const normalizedPath = path.startsWith('/') ? path : `/${path}`
    // Avoid double /api/api
    if (base.endsWith('/api') && normalizedPath.startsWith('/api/')) {
      return base + normalizedPath.slice(4)
    }
    return base + normalizedPath
  }

  return base
}

/**
 * Get a full API endpoint URL.
 * @param {string} endpoint - The endpoint path (e.g., '/auth/login', '/chat/stream').
 * @returns {string} The full URL.
 */
export function getApiUrl(endpoint) {
  return getApiBaseUrl(endpoint)
}

export default getApiBaseUrl
