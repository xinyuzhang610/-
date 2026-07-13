<template>
  <el-container class="layout-container">
    <!-- 侧边栏 -->
    <el-aside :width="isCollapsed ? '64px' : '220px'" class="layout-aside">
      <div class="sidebar-content">
        <div class="logo-container">
          <img src="../assets/logo.png" alt="智教通" class="logo-img" />
          <span v-show="!isCollapsed" class="logo-text">智教通</span>
        </div>

        <el-menu
          :default-active="activeMenu"
          :collapse="isCollapsed"
          :router="true"
          class="sidebar-menu"
          background-color="#fcfaf8"
          text-color="#26251e"
          active-text-color="#26251e"
        >
          <!-- 教师端菜单 -->
          <template v-if="userRole === 'teacher'">
            <el-menu-item index="/teacher/home">
              <el-icon><HomeFilled /></el-icon>
              <template #title>需求引导</template>
            </el-menu-item>
            <el-menu-item index="/teacher/tools">
              <el-icon><Tools /></el-icon>
              <template #title>我的工具</template>
            </el-menu-item>
            <el-menu-item index="/teacher/dashboard">
              <el-icon><DataLine /></el-icon>
              <template #title>数据看板</template>
            </el-menu-item>
          </template>

          <!-- 学生端菜单 -->
          <template v-else>
            <el-menu-item index="/student/plaza">
              <el-icon><Grid /></el-icon>
              <template #title>工具广场</template>
            </el-menu-item>
            <el-menu-item index="/student/chat">
              <el-icon><ChatDotRound /></el-icon>
              <template #title>AI问答</template>
            </el-menu-item>
            <el-menu-item index="/student/records">
              <el-icon><Document /></el-icon>
              <template #title>学习记录</template>
            </el-menu-item>
          </template>
        </el-menu>
      </div>

      <!-- 返回首页 -->
      <div class="sidebar-bottom">
        <el-menu
          :collapse="isCollapsed"
          :router="true"
          class="sidebar-menu-bottom"
          background-color="#fcfaf8"
          text-color="#26251e"
        >
          <el-menu-item index="/" @click="goToHome">
            <el-icon><Back /></el-icon>
            <template #title>返回首页</template>
          </el-menu-item>
        </el-menu>
      </div>
    </el-aside>

    <!-- 右侧内容区 -->
    <el-container>
      <!-- 顶部头部 -->
      <el-header class="layout-header">
        <div class="header-left">
          <el-icon
            class="collapse-btn"
            @click="toggleCollapse"
          >
            <Fold v-if="!isCollapsed" />
            <Expand v-else />
          </el-icon>
          <el-breadcrumb separator="/">
            <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
            <el-breadcrumb-item>{{ currentPageTitle }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>

        <div class="header-right">
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-avatar :size="32" icon="UserFilled" />
              <span class="username">{{ userName }}</span>
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="home">返回首页</el-dropdown-item>
                <el-dropdown-item command="profile">个人信息</el-dropdown-item>
                <el-dropdown-item command="logout" divided>退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <!-- 主内容区 -->
      <el-main class="layout-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  HomeFilled,
  Tools,
  DataLine,
  Grid,
  ChatDotRound,
  Document,
  Fold,
  Expand,
  ArrowDown,
  UserFilled,
  Back
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

// 侧边栏折叠状态
const isCollapsed = ref(false)

// 用户信息（后续从 store 获取）
const userRole = ref('teacher') // teacher 或 student
const userName = ref('张老师')

// 当前激活的菜单
const activeMenu = computed(() => route.path)

// 当前页面标题
const currentPageTitle = computed(() => {
  const titleMap = {
    '/teacher/home': '需求引导',
    '/teacher/tools': '我的工具',
    '/teacher/dashboard': '数据看板',
    '/student/plaza': '工具广场',
    '/student/chat': 'AI问答',
    '/student/records': '学习记录'
  }
  return titleMap[route.path] || '首页'
})

// 切换侧边栏折叠
const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value
}

// 处理下拉菜单命令
const handleCommand = (command) => {
  if (command === 'logout') {
    // 清除登录状态
    localStorage.removeItem('token')
    localStorage.removeItem('userName')
    localStorage.removeItem('userRole')
    router.push('/login')
  } else if (command === 'profile') {
    // 跳转个人信息页
    console.log('查看个人信息')
  } else if (command === 'home') {
    // 返回首页
    router.push('/')
  }
}

// 返回首页
const goToHome = () => {
  router.push('/')
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
  background: var(--color-bg);
}

/* 侧边栏 */
.layout-aside {
  background: var(--color-bg);
  border-right: 1px solid var(--color-chip-bg);
  transition: width 0.3s;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.sidebar-content {
  flex: 1;
  overflow-y: auto;
}

.logo-container {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
  border-bottom: 1px solid var(--color-chip-bg);
}

.logo-img {
  width: 32px;
  height: 32px;
  margin-right: 8px;
}

.logo-text {
  font-family: var(--font-display);
  font-size: 18px;
  font-weight: 600;
  color: var(--color-ink);
  white-space: nowrap;
}

.sidebar-menu {
  border-right: none;
}

.sidebar-menu .el-menu-item {
  font-family: var(--font-sans);
  font-size: 14px;
}

.sidebar-menu .el-menu-item:hover {
  background: var(--color-chip-bg);
}

.sidebar-menu .el-menu-item.is-active {
  background: rgba(38, 37, 30, 0.08);
}

.sidebar-bottom {
  border-top: 1px solid var(--color-chip-bg);
  flex-shrink: 0;
}

/* 顶部头部 */
.layout-header {
  background: var(--color-bg);
  border-bottom: 1px solid var(--color-chip-bg);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  height: 60px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.collapse-btn {
  font-size: 20px;
  cursor: pointer;
  color: var(--color-ink-soft);
  transition: color 0.3s;
}

.collapse-btn:hover {
  color: var(--color-ink);
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: var(--radius-md);
  transition: background 0.3s;
}

.user-info:hover {
  background: var(--color-chip-bg);
}

.username {
  font-family: var(--font-sans);
  font-size: 14px;
  color: var(--color-ink);
}

/* 主内容区 */
.layout-main {
  background: var(--color-bg);
  padding: 24px;
  overflow-y: auto;
}
</style>
