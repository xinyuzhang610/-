<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="login-icon">🏠</div>
        <h1 class="login-title">智教通</h1>
        <p class="login-subtitle">AI智能体教学辅助平台</p>
      </div>

      <!-- 身份选择 -->
      <div class="role-selection">
        <div
          class="role-card"
          :class="{ active: selectedRole === 'teacher' }"
          @click="selectRole('teacher')"
        >
          <div class="role-icon">👨‍🏫</div>
          <div class="role-name">我是教师</div>
          <div class="role-desc">创建工具管理</div>
        </div>
        <div
          class="role-card"
          :class="{ active: selectedRole === 'student' }"
          @click="selectRole('student')"
        >
          <div class="role-icon">👨‍🎓</div>
          <div class="role-name">我是学生</div>
          <div class="role-desc">使用工具学习</div>
        </div>
      </div>

      <!-- 教师登录表单 -->
      <div v-if="selectedRole === 'teacher'" class="login-form-area">
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
              size="large"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
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
            登 录
          </el-button>
        </el-form>

        <div class="form-footer">
          <span>还没有账号？</span>
          <router-link to="/register" class="register-link">立即注册</router-link>
        </div>
      </div>

      <!-- 学生入口 -->
      <div v-if="selectedRole === 'student'" class="student-entry">
        <p class="entry-desc">无需注册，直接进入工具广场开始学习</p>
        <el-button
          type="primary"
          size="large"
          class="entry-btn"
          @click="enterStudent"
        >
          进入工具广场
        </el-button>
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
const selectedRole = ref('')

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

// 选择身份
const selectRole = (role) => {
  selectedRole.value = role
}

// 处理登录
const handleLogin = async () => {
  try {
    await loginFormRef.value.validate()
    loading.value = true

    // TODO: 调用后端登录接口
    setTimeout(() => {
      localStorage.setItem('token', 'mock-token')
      localStorage.setItem('userRole', 'teacher')
      localStorage.setItem('userName', '张老师')

      ElMessage.success('登录成功')
      router.push('/teacher/home')
      loading.value = false
    }, 1000)
  } catch (error) {
    console.log('表单验证失败:', error)
  }
}

// 学生进入工具广场
const enterStudent = () => {
  localStorage.setItem('userRole', 'student')
  router.push('/student/plaza')
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
  animation: fadeIn 0.5s var(--ease-out);
}

.login-card {
  width: 100%;
  max-width: 400px;
  background: white;
  border-radius: var(--radius-lg);
  padding: 40px;
  box-shadow: var(--shadow-lg);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.login-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.login-title {
  font-family: var(--font-heading);
  font-size: 28px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 8px;
}

.login-subtitle {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-ink-soft);
}

/* 身份选择 */
.role-selection {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.role-card {
  padding: 16px 12px;
  border: 2px solid var(--color-chip-bg);
  border-radius: var(--radius-md);
  text-align: center;
  cursor: pointer;
  transition: all var(--duration-normal) ease;
}

.role-card:hover {
  border-color: var(--color-ink);
  transform: translateY(-2px);
}

.role-card.active {
  border-color: var(--color-ink);
  background: var(--color-chip-bg);
}

.role-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.role-name {
  font-family: var(--font-ui);
  font-size: 14px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 4px;
}

.role-desc {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--color-ink-soft);
}

/* 登录表单 */
.login-form-area {
  animation: slideUp 0.3s var(--ease-out);
}

.login-form {
  margin-bottom: 24px;
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
  transform: translateY(-2px);
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
}

.register-link:hover {
  color: var(--color-primary-hover);
}

/* 学生入口 */
.student-entry {
  text-align: center;
  animation: slideUp 0.3s var(--ease-out);
}

.entry-desc {
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-ink-soft);
  margin-bottom: 24px;
}

.entry-btn {
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

.entry-btn:hover {
  background: var(--color-primary-hover);
  border-color: var(--color-primary-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* 动画 */
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式 */
@media (max-width: 768px) {
  .login-card {
    padding: 24px;
  }

  .login-title {
    font-size: 24px;
  }
}
</style>
