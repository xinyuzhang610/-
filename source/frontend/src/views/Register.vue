<template>
  <main class="auth-page">
    <AuthScene :role="selectedRole" mode="register" />
    <section class="auth-panel" aria-labelledby="register-title">
      <div class="auth-panel__inner">
        <RouterLink class="home-link" to="/">← 返回首页</RouterLink>
        <div class="auth-heading"><span>CREATE YOUR ORBIT</span><h1 id="register-title">创建教师账号</h1><p>让工具、课堂与学习数据在同一个知识轨道相遇。</p></div>
        <IdentitySwitch v-model="selectedRole" />
        <div v-if="selectedRole === 'student'" class="student-entry"><h2>学生无需注册</h2><p>直接进入兴趣引导，找到适合自己的学习工具。</p><AppButton variant="jade" @click="enterStudent">进入兴趣星图</AppButton></div>
        <form v-else class="auth-form" @submit.prevent="handleRegister">
          <div class="form-grid">
            <div class="field"><label for="register-username">用户名</label><input id="register-username" v-model.trim="form.username" autocomplete="username" minlength="3" required></div>
            <div class="field"><label for="register-name">姓名</label><input id="register-name" v-model.trim="form.name" autocomplete="name" required></div>
            <div class="field"><label for="register-password">密码</label><input id="register-password" v-model="form.password" autocomplete="new-password" minlength="6" required type="password"></div>
            <div class="field"><label for="register-confirm">确认密码</label><input id="register-confirm" v-model="form.confirmPassword" autocomplete="new-password" minlength="6" required type="password"></div>
            <div class="field"><label for="register-school">学校</label><input id="register-school" v-model.trim="form.school" autocomplete="organization" required></div>
            <div class="field"><label for="register-subject">任教学科</label><select id="register-subject" v-model="form.subject" required><option disabled value="">请选择学科</option><option v-for="subject in subjects" :key="subject">{{ subject }}</option></select></div>
            <div class="field field-wide"><label for="register-grade">任教年级</label><select id="register-grade" v-model="form.grade" required><option disabled value="">请选择年级</option><option v-for="grade in grades" :key="grade">{{ grade }}</option></select></div>
          </div>
          <p v-if="errorMessage" class="form-error" role="alert">{{ errorMessage }}</p>
          <AppButton class="submit-button" type="submit" variant="gold" :loading="loading">创建账号</AppButton>
          <p class="auth-footnote">已有账号？<RouterLink to="/login?role=teacher">返回登录</RouterLink></p>
        </form>
      </div>
    </section>
  </main>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { register as registerRequest } from '../api/auth'
import AuthScene from '../components/auth/AuthScene.vue'
import IdentitySwitch from '../components/auth/IdentitySwitch.vue'
import AppButton from '../components/ui/AppButton.vue'

const route = useRoute()
const router = useRouter()
const selectedRole = ref(route.query.role === 'student' ? 'student' : 'teacher')
const loading = ref(false)
const errorMessage = ref('')
const subjects = ['语文','数学','英语','物理','化学','生物','历史','地理','政治','信息技术']
const grades = ['初一','初二','初三','高一','高二','高三']
const form = reactive({ username:'', password:'', confirmPassword:'', name:'', school:'', subject:'', grade:'' })
watch(selectedRole, () => { errorMessage.value = '' })

async function handleRegister() {
  if (form.password !== form.confirmPassword) { errorMessage.value = '两次输入的密码不一致。'; return }
  loading.value = true
  errorMessage.value = ''
  try {
    const { confirmPassword, ...profile } = form
    await registerRequest({ ...profile, role: 'teacher' })
    await router.push('/login?role=teacher')
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || '暂时无法注册，请检查网络或稍后重试。'
  } finally { loading.value = false }
}

async function enterStudent() { localStorage.setItem('userRole','student'); await router.push('/student/guidance') }
</script>

<style scoped>
.auth-page{display:grid;grid-template-columns:minmax(0,.9fr) minmax(520px,1.1fr);min-height:100vh;background:var(--ink-950);color:var(--moon-50)}.auth-panel{display:grid;place-items:center;padding:clamp(28px,4vw,62px);background:radial-gradient(circle at 90% 10%,var(--effect-gold-soft),transparent 34%),var(--ink-900)}.auth-panel__inner{width:min(100%,680px)}.home-link{display:inline-block;margin-bottom:30px;color:var(--moon-300);text-decoration:none}.auth-heading>span{color:var(--gold-300);font-size:.7rem;letter-spacing:.24em}.auth-heading h1{margin:8px 0;font-family:var(--font-display);font-size:clamp(2.2rem,3.6vw,4rem);font-weight:500}.auth-heading p{margin-bottom:22px;color:var(--moon-300);line-height:1.7}.auth-form{display:grid;gap:18px;margin-top:22px}.form-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}.field{display:grid;gap:7px}.field-wide{grid-column:1/-1}.field label{color:var(--moon-200);font-size:.82rem}.field input,.field select{width:100%;min-height:48px;padding:0 14px;border:1px solid var(--color-border);border-radius:var(--radius-md);background:rgba(255,255,255,.045);color:var(--moon-50);font:inherit}.field select option{color:#111}.field input:focus-visible,.field select:focus-visible{outline:3px solid var(--focus-ring);outline-offset:2px}.form-error{padding:11px 13px;border-left:3px solid var(--cinnabar-500);background:rgba(168,58,46,.12);color:#ffd8d2}.submit-button{width:100%}.auth-footnote{text-align:center;color:var(--moon-300);font-size:.9rem}.auth-footnote a{color:var(--gold-300)}.student-entry{margin-top:22px;padding:24px;border:1px solid var(--color-border);border-radius:var(--radius-xl);background:var(--material-panel)}.student-entry h2{font-family:var(--font-display);font-size:1.7rem}.student-entry p{margin:8px 0 20px;color:var(--moon-300)}@media(max-width:980px){.auth-page{grid-template-columns:1fr}.auth-panel{padding:36px 22px 60px}}@media(max-width:620px){.form-grid{grid-template-columns:1fr}.field-wide{grid-column:auto}}
</style>
