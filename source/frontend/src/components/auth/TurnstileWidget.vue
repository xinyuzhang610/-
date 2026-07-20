<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'

const props = defineProps({
  siteKey: { type: String, required: true },
  action: { type: String, default: 'login' }
})

const emit = defineEmits(['verify', 'expire', 'error'])

const widgetRef = ref(null)
const widgetId = ref(null)
const scriptLoaded = ref(false)
const scriptError = ref(false)

function loadScript() {
  if (document.querySelector('script[src*="challenges.cloudflare.com"]')) {
    scriptLoaded.value = true
    return
  }
  const script = document.createElement('script')
  script.src = 'https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit'
  script.async = true
  script.defer = true
  script.onload = () => { scriptLoaded.value = true }
  script.onerror = () => { scriptError.value = true }
  document.head.appendChild(script)
}

function renderWidget() {
  if (!scriptLoaded.value || !window.turnstile || !widgetRef.value) return
  if (widgetId.value !== null) {
    try { window.turnstile.remove(widgetId.value) } catch {}
  }
  widgetId.value = window.turnstile.render(widgetRef.value, {
    sitekey: props.siteKey,
    action: props.action,
    callback: (token) => emit('verify', token),
    'expired-callback': () => emit('expire'),
    'error-callback': () => emit('error')
  })
}

function reset() {
  if (widgetId.value !== null && window.turnstile) {
    try { window.turnstile.reset(widgetId.value) } catch {}
  }
}

watch(scriptLoaded, (loaded) => { if (loaded) renderWidget() })

onMounted(() => {
  if (!props.siteKey) { scriptError.value = true; return }
  loadScript()
})

onBeforeUnmount(() => {
  if (widgetId.value !== null && window.turnstile) {
    try { window.turnstile.remove(widgetId.value) } catch {}
  }
})

defineExpose({ reset })
</script>

<template>
  <div v-if="scriptError" class="turnstile-error" role="alert">Turnstile 配置错误：请检查 VITE_TURNSTILE_SITE_KEY</div>
  <div v-else ref="widgetRef" class="turnstile-widget" />
</template>

<style scoped>
.turnstile-widget { margin: 12px 0; }
.turnstile-error { padding: 12px; border-left: 3px solid var(--cinnabar-500); background: rgba(168,58,46,.12); color: #ffd8d2; font-size: 0.85rem; margin: 12px 0; }
</style>
