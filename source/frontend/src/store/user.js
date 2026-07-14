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
    token.value = loginData.token
    userName.value = loginData.userName
    userRole.value = loginData.userRole || 'teacher'

    localStorage.setItem('token', loginData.token)
    localStorage.setItem('userName', loginData.userName)
    localStorage.setItem('userRole', loginData.userRole || 'teacher')
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
