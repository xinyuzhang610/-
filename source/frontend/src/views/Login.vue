<template>
  <div class="auth-container">
    <!-- 左侧插画 -->
    <div class="auth-illustration">
      <div class="illustration-content">
        <div class="illustration-icon">🎓</div>
        <h2 class="illustration-title">智教通</h2>
        <p class="illustration-desc">AI智能体教学辅助平台</p>
        <p class="illustration-quote">"让AI赋能每一堂课"</p>
      </div>
    </div>

    <!-- 右侧表单 -->
    <div class="auth-form">
      <div class="form-header">
        <h1 class="form-title">欢迎回来</h1>
        <p class="form-subtitle">登录智教通</p>
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
            placeholder="用户名"
            size="large"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-button
          type="primary"
          size="large"
          class="login-btn"
          :loading="loading"
          @click="handleLogin"
        >
          登录
        </el-button>
      </el-form>

      <div class="form-footer">
        <span>还没有账号？</span>
        <router-link to="/register" class="register-link">立即注册 →</router-link>
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
.auth-container {
  display: flex;
  min-height: 100vh;
}

/* 左侧插画 */
.auth-illustration {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-chip-bg);
  padding: var(--space-2xl);
  animation: fadeInLeft 0.5s var(--ease-out);
}

.illustration-content {
  text-align: center;
}

.illustration-icon {
  font-size: 80px;
  margin-bottom: var(--space-lg);
}

.illustration-title {
  font-family: var(--font-heading);
  font-size: 36px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: var(--space-sm);
}

.illustration-desc {
  font-family: var(--font-body);
  font-size: 16px;
  color: var(--color-ink-soft);
  margin-bottom: var(--space-xl);
}

.illustration-quote {
  font-family: var(--font-title);
  font-size: 18px;
  font-style: italic;
  color: var(--color-ink);
}

/* 右侧表单 */
.auth-form {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: var(--space-2xl);
  max-width: 500px;
  animation: fadeInRight 0.5s var(--ease-out) 0.2s both;
}

.form-header {
  margin-bottom: var(--space-2xl);
}

.form-title {
  font-family: var(--font-heading);
  font-size: 32px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: var(--space-sm);
}

.form-subtitle {
  font-family: var(--font-body);
  font-size: 16px;
  color: var(--color-ink-soft);
}

.login-form {
  margin-bottom: var(--space-lg);
}

.login-form :deep(.el-input__wrapper) {
  border-radius: var(--radius-md);
  box-shadow: 0 0 0 1px var(--color-border) inset;
  transition: box-shadow var(--duration-fast) ease;
}

.login-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--color-ink) inset;
}

.login-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px var(--color-ink) inset;
}

.login-btn {
  width: 100%;
  border-radius: var(--radius-full);
  font-family: var(--font-ui);
  font-size: 16px;
  font-weight: 500;
  background: var(--color-primary);
  border-color: var(--color-primary);
  height: 48px;
  transition: all var(--duration-fast) ease;
}

.login-btn:hover {
  background: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

.form-footer {
  text-align: center;
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-ink-soft);
}

.register-link {
  color: var(--color-primary);
  margin-left: var(--space-xs);
  text-decoration: none;
  font-weight: 500;
  transition: color var(--duration-fast) ease;
}

.register-link:hover {
  color: var(--color-primary-hover);
}

/* 动画 */
@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(20px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 响应式 */
@media (max-width: 768px) {
  .auth-container {
    flex-direction: column;
  }

  .auth-illustration {
    min-height: 200px;
    padding: var(--space-lg);
  }

  .illustration-icon {
    font-size: 60px;
  }

  .illustration-title {
    font-size: 28px;
  }

  .auth-form {
    max-width: 100%;
    padding: var(--space-lg);
  }

  .form-title {
    font-size: 24px;
  }
}
</style>
