import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useUserStore = defineStore('user', () => {
  // 状态
  const token = ref(localStorage.getItem('token') || '')
  const userName = ref(localStorage.getItem('userName') || '')
  const userRole = ref(localStorage.getItem('userRole') || 'teacher')

  // 计算属性
  const isLoggedIn = computed(() => !!token.value)

  // 登录
  const login = (loginData) => {
    const receivedToken = loginData.access_token || loginData.token
    const user = loginData.user || {}
    token.value = receivedToken
    userName.value = loginData.userName || user.name || user.username || ''
    userRole.value = loginData.userRole || user.role || 'teacher'

    localStorage.setItem('token', receivedToken)
    localStorage.setItem('userName', userName.value)
    localStorage.setItem('userRole', userRole.value)
  }

  // 登出
  const logout = () => {
    token.value = ''
    userName.value = ''
    userRole.value = 'teacher'

    localStorage.removeItem('token')
    localStorage.removeItem('userName')
    localStorage.removeItem('userRole')
  }

  return {
    token,
    userName,
    userRole,
    isLoggedIn,
    login,
    logout
  }
})
