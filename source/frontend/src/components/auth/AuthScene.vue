<template>
  <aside class="auth-scene" :class="`is-${role}`" aria-label="智教通身份场景">
    <img :src="art.src" alt="" :width="art.width" :height="art.height">
    <div class="auth-scene__veil"></div>
    <div class="auth-scene__content">
      <RouterLink to="/" aria-label="返回智教通首页"><BrandMark /></RouterLink>
      <div class="scene-copy">
        <span class="scene-kicker">{{ role === 'teacher' ? 'TEACH WITH INTELLIGENCE' : 'LEARN WITH WONDER' }}</span>
        <h2>{{ title }}</h2>
        <p>{{ description }}</p>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import BrandMark from '../brand/BrandMark.vue'
import { generatedAssets } from '../../assets/generated/asset-manifest'

const props = defineProps({ role: { type: String, default: 'teacher' }, mode: { type: String, default: 'login' } })
const art = computed(() => props.role === 'student' ? generatedAssets.studentOrbit : generatedAssets.teacherOrbit)
const title = computed(() => props.role === 'student' ? '让好奇心成为你的导航' : props.mode === 'register' ? '把灵感，变成下一堂好课' : '让每一堂课，都看见更多可能')
const description = computed(() => props.role === 'student' ? '无需注册，从兴趣星图进入你的知识宇宙。' : '从需求发现到工具创造，让 AI 成为教师可靠的同行者。')
</script>

<style scoped>
.auth-scene{position:relative;min-height:100%;overflow:hidden;background:var(--ink-950)}.auth-scene>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center}.auth-scene.is-teacher>img{object-position:60% center}.auth-scene.is-student>img{object-position:36% center}.auth-scene__veil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,8,8,.2),rgba(4,8,8,.42) 55%,rgba(4,8,8,.92)),linear-gradient(90deg,rgba(4,8,8,.1),rgba(4,8,8,.5))}.auth-scene__content{position:relative;z-index:1;display:flex;flex-direction:column;justify-content:space-between;min-height:100%;padding:clamp(24px,4vw,58px)}.auth-scene__content>a{text-decoration:none;width:max-content}.scene-copy{max-width:600px}.scene-kicker{color:var(--gold-300);font-size:.72rem;letter-spacing:.25em}.scene-copy h2{max-width:12ch;margin:14px 0;font-family:var(--font-display);font-size:clamp(2.3rem,4.4vw,5.4rem);font-weight:500;line-height:1.04;color:var(--moon-50)}.scene-copy p{max-width:42ch;color:var(--moon-200);font-size:1rem;line-height:1.8}@media(max-width:880px){.auth-scene{min-height:300px}.auth-scene__content{min-height:300px}.scene-copy h2{font-size:clamp(2rem,8vw,3.5rem)}}
</style>
