<template>
  <div class="register-container">
    <div class="register-card">
      <div class="register-header">
        <img src="../assets/logo.png" alt="智教通" class="register-logo" />
        <h1 class="register-title">注册账号</h1>
        <p class="register-subtitle">加入智教通，开启智能教学之旅</p>
      </div>

      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        class="register-form"
        label-position="top"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="registerForm.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            size="large"
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="registerForm.password"
            type="password"
            placeholder="请输入密码（至少6位）"
            prefix-icon="Lock"
            size="large"
            show-password
          />
        </el-form-item>

        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input
            v-model="registerForm.confirmPassword"
            type="password"
            placeholder="请再次输入密码"
            prefix-icon="Lock"
            size="large"
            show-password
          />
        </el-form-item>

        <el-form-item label="姓名" prop="name">
          <el-input
            v-model="registerForm.name"
            placeholder="请输入真实姓名"
            size="large"
          />
        </el-form-item>

        <el-form-item label="学校" prop="school">
          <el-input
            v-model="registerForm.school"
            placeholder="请输入学校名称"
            size="large"
          />
        </el-form-item>

        <el-form-item label="科目" prop="subject">
          <el-select
            v-model="registerForm.subject"
            placeholder="请选择科目"
            size="large"
            style="width: 100%"
          >
            <el-option label="语文" value="语文" />
            <el-option label="数学" value="数学" />
            <el-option label="英语" value="英语" />
            <el-option label="物理" value="物理" />
            <el-option label="化学" value="化学" />
            <el-option label="生物" value="生物" />
            <el-option label="历史" value="历史" />
            <el-option label="地理" value="地理" />
            <el-option label="政治" value="政治" />
            <el-option label="信息技术" value="信息技术" />
          </el-select>
        </el-form-item>

        <el-form-item label="年级" prop="grade">
          <el-select
            v-model="registerForm.grade"
            placeholder="请选择年级"
            size="large"
            style="width: 100%"
          >
            <el-option label="初一" value="初一" />
            <el-option label="初二" value="初二" />
            <el-option label="初三" value="初三" />
            <el-option label="高一" value="高一" />
            <el-option label="高二" value="高二" />
            <el-option label="高三" value="高三" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="register-btn"
            :loading="loading"
            @click="handleRegister"
          >
            注册
          </el-button>
        </el-form-item>
      </el-form>

      <div class="register-footer">
        <span>已有账号？</span>
        <router-link to="/login" class="login-link">立即登录</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const registerFormRef = ref(null)
const loading = ref(false)

// 注册表单数据
const registerForm = reactive({
  username: '',
  password: '',
  confirmPassword: '',
  name: '',
  school: '',
  subject: '',
  grade: ''
})

// 确认密码验证
const validateConfirmPassword = (rule, value, callback) => {
  if (value !== registerForm.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 表单验证规则
const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, message: '用户名长度不能少于3位', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  school: [
    { required: true, message: '请输入学校名称', trigger: 'blur' }
  ],
  subject: [
    { required: true, message: '请选择科目', trigger: 'change' }
  ],
  grade: [
    { required: true, message: '请选择年级', trigger: 'change' }
  ]
}

// 处理注册
const handleRegister = async () => {
  try {
    // 验证表单
    await registerFormRef.value.validate()

    loading.value = true

    // TODO: 调用后端注册接口
    // 模拟注册成功
    setTimeout(() => {
      ElMessage.success('注册成功，请登录')
      router.push('/login')
      loading.value = false
    }, 1000)
  } catch (error) {
    // 表单验证失败
    console.log('表单验证失败:', error)
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg);
  padding: 20px;
}

.register-card {
  width: 100%;
  max-width: 480px;
  background: white;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
}

.register-header {
  text-align: center;
  margin-bottom: 32px;
}

.register-logo {
  width: 64px;
  height: 64px;
  margin-bottom: 16px;
}

.register-title {
  font-family: var(--font-display);
  font-size: 28px;
  font-weight: 600;
  color: var(--color-ink);
  margin-bottom: 8px;
}

.register-subtitle {
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--color-ink-soft);
}

.register-form {
  margin-bottom: 24px;
}

.register-form :deep(.el-form-item__label) {
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--color-ink);
}

.register-form :deep(.el-input__wrapper) {
  border-radius: var(--radius-md);
  box-shadow: 0 0 0 1px var(--color-border) inset;
}

.register-form :deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px var(--color-ink) inset;
}

.register-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px var(--color-ink) inset;
}

.register-form :deep(.el-select .el-input__wrapper) {
  border-radius: var(--radius-md);
}

.register-btn {
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

.register-btn:hover {
  background: #3a3933;
  border-color: #3a3933;
}

.register-footer {
  text-align: center;
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--color-ink-soft);
}

.login-link {
  color: var(--color-ink);
  margin-left: 4px;
  text-decoration: underline;
  text-underline-offset: 3px;
}

.login-link:hover {
  color: #3a3933;
}
</style>
