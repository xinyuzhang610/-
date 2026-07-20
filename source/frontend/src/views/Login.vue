<template>
  <main class="auth-page">
    <AuthScene :role="selectedRole" mode="login" />
    <section class="auth-panel" aria-labelledby="login-title">
      <div class="auth-panel__inner">
        <RouterLink class="home-link" to="/">← 返回首页</RouterLink>
        <div class="auth-heading"><span>WELCOME BACK</span><h1 id="login-title">进入智教通</h1><p>选择身份，继续你的智慧教学旅程。</p></div>
        <IdentitySwitch v-model="selectedRole" />

        <form class="auth-form" @submit.prevent="handleLogin">
          <div class="field"><label for="login-username">用户名</label><input id="login-username" v-model.trim="form.username" autocomplete="username" minlength="3" required placeholder="请输入用户名"></div>
          <div class="field"><label for="login-password">密码</label><input id="login-password" v-model="form.password" autocomplete="current-password" minlength="6" required type="password" placeholder="请输入密码"></div>
          <TurnstileWidget v-if="turnstileSiteKey" ref="turnstileRef" :site-key="turnstileSiteKey" action="login" @verify="onCaptchaVerify" @expire="onCaptchaExpire" @error="onCaptchaError" />
          <p v-else class="form-hint">开发环境：验证码已跳过</p>
          <p v-if="errorMessage" class="form-error" role="alert">{{ errorMessage }}</p>
          <AppButton class="submit-button" type="submit" :variant="selectedRole === 'teacher' ? 'gold' : 'jade'" :loading="loading">登录{{ selectedRole === 'teacher' ? '教师工作台' : '学生学习空间' }}</AppButton>
          <p class="auth-footnote">还没有账号？<RouterLink :to="`/register?role=${selectedRole}`">创建{{ selectedRole === 'teacher' ? '教师' : '学生' }}账号</RouterLink></p>
        </form>
      </div>
    </section>
  </main>
</template>

<script setup>
import { reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import { login as loginRequest } from '../api/auth'
import AuthScene from '../components/auth/AuthScene.vue'
import IdentitySwitch from '../components/auth/IdentitySwitch.vue'
import AppButton from '../components/ui/AppButton.vue'
import TurnstileWidget from '../components/auth/TurnstileWidget.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const selectedRole = ref(route.query.role === 'student' ? 'student' : 'teacher')
const loading = ref(false)
const errorMessage = ref('')
const form = reactive({ username: '', password: '' })
const captchaToken = ref(null)
const turnstileRef = ref(null)

const turnstileSiteKey = import.meta.env?.VITE_TURNSTILE_SITE_KEY || ''
const isDemoMode = import.meta.env?.VITE_DEMO_MODE === 'true'

// 未配置 Turnstile 或演示模式下自动跳过验证码
if (!turnstileSiteKey || isDemoMode) {
  captchaToken.value = 'dev-bypass'
}

watch(selectedRole, () => { errorMessage.value = '' })

function onCaptchaVerify(token) { captchaToken.value = token }
function onCaptchaExpire() { captchaToken.value = null }
function onCaptchaError() { captchaToken.value = null }

async function handleLogin() {
  if (!captchaToken.value) {
    errorMessage.value = '请完成验证码验证'
    return
  }
  loading.value = true
  errorMessage.value = ''
  try {
    // 演示模式下模拟登录，无需后端
    if (isDemoMode) {
      userStore.login({
        access_token: 'demo-token',
        user: { name: form.username || '演示用户', role: selectedRole.value }
      })
      const fallback = selectedRole.value === 'student' ? '/student/guidance' : '/teacher/home'
      await router.push(route.query.redirect || fallback)
      return
    }
    const response = await loginRequest({ username: form.username, password: form.password, expected_role: selectedRole.value, captcha_token: captchaToken.value })
    const payload = response.data
    userStore.login(payload)
    const fallback = payload.user?.role === 'student' ? '/student/guidance' : '/teacher/home'
    await router.push(route.query.redirect || fallback)
  } catch (error) {
    errorMessage.value = error.response?.data?.detail || '暂时无法登录，请检查网络或稍后重试。'
    if (turnstileRef.value) turnstileRef.value.reset()
    captchaToken.value = null
  } finally {
    loading.value = false
  }
}

</script>

<style scoped>
.auth-page{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(420px,.85fr);min-height:100vh;background:var(--ink-950);color:var(--moon-50)}.auth-panel{display:grid;place-items:center;padding:clamp(28px,5vw,72px);background:radial-gradient(circle at 90% 10%,var(--effect-jade-soft),transparent 35%),var(--ink-900)}.auth-panel__inner{width:min(100%,520px)}.home-link{display:inline-block;margin-bottom:clamp(28px,6vh,68px);color:var(--moon-300);text-decoration:none}.auth-heading>span{color:var(--gold-300);font-size:.7rem;letter-spacing:.24em}.auth-heading h1{margin:10px 0;font-family:var(--font-display);font-size:clamp(2.4rem,4vw,4.5rem);font-weight:500}.auth-heading p{margin-bottom:28px;color:var(--moon-300);line-height:1.7}.auth-form{display:grid;gap:18px;margin-top:24px}.field{display:grid;gap:8px}.field label{color:var(--moon-200);font-size:.86rem}.field input{width:100%;min-height:50px;padding:0 16px;border:1px solid var(--color-border);border-radius:var(--radius-md);background:rgba(255,255,255,.045);color:var(--moon-50);font:inherit}.field input:focus-visible{outline:3px solid var(--focus-ring);outline-offset:2px}.form-error{padding:11px 13px;border-left:3px solid var(--cinnabar-500);background:rgba(168,58,46,.12);color:#ffd8d2;line-height:1.5}.form-hint{padding:8px 0;color:var(--ink-300);font-size:.85rem;text-align:center}.submit-button{width:100%}.auth-footnote{text-align:center;color:var(--moon-300);font-size:.9rem}.auth-footnote a{color:var(--gold-300)}.student-entry{position:relative;margin-top:26px;padding:28px;border:1px solid var(--color-border);border-radius:var(--radius-xl);background:var(--material-panel);overflow:hidden}.student-entry h2{font-family:var(--font-display);font-size:1.8rem}.student-entry p{margin:10px 0 22px;color:var(--moon-300);line-height:1.7}.student-pulse{position:absolute;right:-40px;top:-40px;width:150px;height:150px;border:1px solid var(--jade-400);border-radius:50%;box-shadow:0 0 55px var(--effect-jade-soft)}@media(max-width:880px){.auth-page{grid-template-columns:1fr}.auth-panel{padding:36px 22px 60px}.home-link{margin-bottom:32px}}@media(prefers-reduced-motion:reduce){.student-pulse{display:none}}
</style>
