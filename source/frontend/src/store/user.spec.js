import { beforeEach, describe, expect, it } from 'vitest'
import { createPinia, setActivePinia } from 'pinia'
import { useUserStore } from './user'

describe('user store login contract', () => {
  beforeEach(() => {
    localStorage.clear()
    setActivePinia(createPinia())
  })

  it('stores the backend access_token returned by login', () => {
    const store = useUserStore()
    store.login({ access_token: 'jwt-from-api', user: { username: 'student-a', role: 'student' } })

    expect(store.token).toBe('jwt-from-api')
    expect(localStorage.getItem('token')).toBe('jwt-from-api')
    expect(store.userRole).toBe('student')
  })
})
