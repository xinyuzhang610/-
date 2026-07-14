<template>
  <div class="workspace" :class="{ 'is-collapsed': collapsed }">
    <button v-if="mobileOpen" class="drawer-backdrop" aria-label="关闭导航" @click="mobileOpen=false"></button>
    <aside class="sidebar" :class="{ 'is-open': mobileOpen }">
      <RouterLink class="brand-link" to="/"><BrandMark :compact="collapsed" /></RouterLink>
      <nav :aria-label="role === 'teacher' ? '教师工作台导航' : '学生学习导航'">
        <RouterLink v-for="item in navItems" :key="item.to" :to="item.to" :aria-current="route.path===item.to?'page':undefined" @click="mobileOpen=false">
          <svg viewBox="0 0 24 24" aria-hidden="true"><path :d="item.icon"/></svg><span>{{ item.label }}</span>
        </RouterLink>
      </nav>
      <div class="sidebar-footer"><RouterLink to="/">返回首页</RouterLink><button @click="logout">退出登录</button></div>
    </aside>
    <div class="workspace-body">
      <header class="workspace-header">
        <div><button class="mobile-menu" aria-label="打开导航菜单" @click="mobileOpen=true"><span></span><span></span></button><button class="collapse-control" :aria-label="collapsed?'展开侧栏':'收起侧栏'" @click="collapsed=!collapsed">{{ collapsed ? '→' : '←' }}</button></div>
        <div class="page-context"><span>{{ role==='teacher'?'TEACHER ORBIT':'STUDENT ORBIT' }}</span><strong>{{ route.meta.title || '智教通' }}</strong><em v-if="demoEnabled">{{ demoLabel }}</em></div>
        <div class="profile"><span>{{ initials }}</span><div><small>{{ role==='teacher'?'教师':'学生' }}</small><strong>{{ userName }}</strong></div></div>
      </header>
      <main class="workspace-main"><RouterView /></main>
    </div>
  </div>
</template>
<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../store/user'
import BrandMark from '../components/brand/BrandMark.vue'
import { useDemoMode } from '../composables/useDemoMode'
const route=useRoute(),router=useRouter(),store=useUserStore()
const collapsed=ref(false),mobileOpen=ref(false)
const { enabled: demoEnabled, label: demoLabel }=useDemoMode()
const role=computed(()=>route.path.startsWith('/student')?'student':'teacher')
const userName=computed(()=>store.userName||localStorage.getItem('userName')||(role.value==='teacher'?'教师用户':'探索者'))
const initials=computed(()=>userName.value.slice(0,1))
const teacherNav=[
 {to:'/teacher/home',label:'需求引导',icon:'M4 19V5h16v14H4Zm4-9h8M8 14h5'},
 {to:'/teacher/tools',label:'我的工具',icon:'M14 6 18 2l4 4-4 4M3 21l8-8m2-7 5 5M5 3l4 4'},
 {to:'/teacher/dashboard',label:'数据洞察',icon:'M4 20V10m6 10V4m6 16v-7m4 7H2'}]
const studentNav=[
 {to:'/student/guidance',label:'兴趣引导',icon:'M12 3a7 7 0 0 0-4 12v3h8v-3a7 7 0 0 0-4-12Z'},
 {to:'/student/plaza',label:'工具广场',icon:'M4 4h6v6H4V4Zm10 0h6v6h-6V4ZM4 14h6v6H4v-6Zm10 0h6v6h-6v-6Z'},
 {to:'/student/chat',label:'AI 问答',icon:'M4 5h16v11H8l-4 4V5Z'},
 {to:'/student/records',label:'学习轨迹',icon:'M5 19V5m0 14h15M8 15l3-4 3 2 5-7'}]
const navItems=computed(()=>role.value==='teacher'?teacherNav:studentNav)
function logout(){store.logout();router.push('/login')}
function onKey(e){if(e.key==='Escape')mobileOpen.value=false}
onMounted(()=>document.addEventListener('keydown',onKey));onBeforeUnmount(()=>document.removeEventListener('keydown',onKey))
</script>
<style scoped>
.workspace{display:grid;grid-template-columns:260px 1fr;min-height:100vh;background:var(--ink-950);color:var(--moon-50)}.sidebar{position:sticky;top:0;display:flex;flex-direction:column;height:100vh;padding:24px 16px;border-right:1px solid var(--color-border);background:linear-gradient(180deg,var(--ink-900),var(--ink-950));z-index:20;transition:width var(--duration-normal)}.brand-link{display:block;padding:4px 8px 28px;text-decoration:none}.sidebar nav{display:grid;gap:8px}.sidebar nav a,.sidebar-footer a,.sidebar-footer button{display:flex;align-items:center;gap:13px;min-height:48px;padding:0 13px;border:1px solid transparent;border-radius:var(--radius-md);background:transparent;color:var(--moon-300);text-decoration:none;font:inherit}.sidebar nav a svg{width:21px;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round}.sidebar nav a:hover,.sidebar nav a[aria-current="page"]{color:var(--moon-50);background:var(--material-panel-dark);border-color:var(--color-border)}.sidebar nav a[aria-current="page"] svg{color:var(--gold-300)}.sidebar-footer{display:grid;gap:4px;margin-top:auto}.sidebar-footer button{width:100%;cursor:pointer}.workspace-body{min-width:0}.workspace-header{position:sticky;top:0;z-index:10;display:grid;grid-template-columns:1fr auto 1fr;align-items:center;min-height:76px;padding:0 28px;border-bottom:1px solid var(--color-border);background:rgba(16,25,22,.86);backdrop-filter:blur(18px)}.workspace-header>div:first-child{display:flex;gap:8px}.collapse-control,.mobile-menu{display:grid;place-items:center;min-width:44px;min-height:44px;border:1px solid var(--color-border);border-radius:50%;background:transparent;color:var(--moon-200);cursor:pointer}.mobile-menu{display:none}.mobile-menu span{display:block;width:18px;height:1px;background:currentColor;margin:2px}.page-context{text-align:center}.page-context span,.profile small{display:block;color:var(--gold-300);font-size:.62rem;letter-spacing:.16em}.page-context strong{display:block;margin-top:3px}.profile{display:flex;justify-content:flex-end;align-items:center;gap:10px}.profile>span{display:grid;place-items:center;width:38px;height:38px;border:1px solid var(--jade-400);border-radius:50%;color:var(--jade-400)}.profile strong{display:block;font-size:.82rem}.workspace-main{padding:clamp(20px,4vw,48px)}.is-collapsed{grid-template-columns:88px 1fr}.is-collapsed .sidebar nav a span,.is-collapsed .sidebar-footer,.is-collapsed :deep(.brand-copy){display:none}.is-collapsed .sidebar nav a{justify-content:center}.drawer-backdrop{display:none}@media(max-width:900px){.workspace,.is-collapsed{grid-template-columns:1fr}.sidebar{position:fixed;left:0;width:280px;transform:translateX(-102%);box-shadow:30px 0 80px rgba(0,0,0,.45)}.sidebar.is-open{transform:translateX(0)}.drawer-backdrop{display:block;position:fixed;inset:0;border:0;background:rgba(0,0,0,.6);z-index:15}.collapse-control{display:none}.mobile-menu{display:block}.workspace-header{grid-template-columns:1fr auto}.page-context{display:none}.workspace-main{padding:22px 16px}.profile div{display:none}}
.page-context em{display:inline-block;margin-top:5px;padding:2px 7px;border:1px solid var(--gold-400);border-radius:99px;color:var(--gold-300);font-size:.62rem;font-style:normal}
</style>
