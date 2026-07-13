<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <img src="../assets/logo.png" alt="智教通" class="login-logo" />
        <h1 class="login-title">智教通</h1>
        <p class="login-subtitle">AI智能体教学辅助平台</p>
      </div>

      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-btn"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>

      <div class="login-footer">
        <span>还没有账号？</span>
        <router-link to="/register" class="register-link">立即注册</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = async () => {
  try {
    // 验证表单
    await loginFormRef.value.validate()

    loading.value = true

    // TODO: 调用后端登录接口
    // 模拟登录成功
    setTimeout(() => {
      // 存储token
      localStorage.setItem('token', 'mock-token')
      localStorage.setItem('userRole', 'teacher')
      localStorage.setItem('userName', '张老师')

      ElMessage.success('登录成功')
      router.push('/teacher/home')
      loading.value = false
    }, 1000)
  } catch (error) {
    // 表单验证失败
    console.log('表单验证失败:', error)
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-logo {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
}

.login-title {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 8px;
}

.login-subtitle {
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--color-ink-soft);
}

.login-form {
  margin-bottom: 24px;
}

.login-form :deep(.el-input__wrapper) {
  border-radius: var(--radius-md);
  box-shadow: 0 0 0 1px var(--color-border) inset;
}

.login-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--color-ink) inset;
}

.login-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px var(--color-ink) inset;
}

.login-btn {
  width: 100%;
  border-radius: 46px;
  font-family: var(--font-misans);
  font-size: 16px;
  font-weight: 500;
  background: var(--color-ink);
  border-color: var(--color-ink);
  color: #fafafa;
  height: 40px;
}

.login-btn:hover {
  background: #3a3933;
  border-color: #3a3933;
}

.login-footer {
  text-align: center;
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--color-ink-soft);
}

.register-link {
  color: var(--color-ink);
  margin-left: 4px;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.register-link:hover {
  color: #3a3933;
}
</style>
