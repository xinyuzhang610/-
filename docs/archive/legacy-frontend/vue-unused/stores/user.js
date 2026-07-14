// stores/user.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, register as apiRegister, getProfile } from '@/api/auth'

export const useUserStore = defineStore('user', () => {
  // 状态
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')

  // 计算属性
  const isLoggedIn = computed(() => !!token.value)
  const isTeacher = computed(() => user.value?.role === 'teacher')
  const isStudent = computed(() => user.value?.role === 'student')

  // 登录
  async function login(credentials) {
    try {
      const res = await apiLogin(credentials)
      token.value = res.data.token
      localStorage.setItem('token', res.data.token)
      await fetchProfile(res.data.user_id)
      return res.data
    } catch (error) {
      throw error
    }
  }

  // 注册
  async function register(userData) {
    try {
      const res = await apiRegister(userData)
      return res.data
    } catch (error) {
      throw error
    }
  }

  // 获取用户信息
  async function fetchProfile(userId) {
    try {
      const res = await getProfile(userId)
      user.value = res.data
    } catch (error) {
      console.error('获取用户信息失败:', error)
    }
  }

  // 退出登录
  function logout() {
    user.value = null
    token.value = ''
    localStorage.removeItem('token')
  }

  return {
    user,
    token,
    isLoggedIn,
    isTeacher,
    isStudent,
    login,
    register,
    fetchProfile,
    logout
  }
})
