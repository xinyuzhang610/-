<template>
  <el-container class="layout-container">
    <el-header class="header">
      <div class="header-left">
        <span class="logo">智教通</span>
        <el-menu
          :default-active="activeMenu"
          mode="horizontal"
          router
          class="nav-menu"
        >
          <el-menu-item index="/student">需求引导</el-menu-item>
          <el-menu-item index="/student/plaza">工具广场</el-menu-item>
          <el-menu-item index="/student/chat">AI问答</el-menu-item>
          <el-menu-item index="/student/records">学习记录</el-menu-item>
        </el-menu>
      </div>
      <el-button type="text" @click="goHome">返回首页</el-button>
    </el-header>
    <el-main class="main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const activeMenu = computed(() => route.path)

const goHome = () => {
  router.push('/')
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}
.header {
  background-color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
  padding: 0 20px;
}
.header-left {
  display: flex;
  align-items: center;
}
.logo {
  font-size: 20px;
  font-weight: bold;
  margin-right: 30px;
}
.nav-menu {
  border-bottom: none;
}
.main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
