<template>
  <el-container class="layout-container">
    <el-aside width="200px" class="aside">
      <div class="logo">智教通</div>
      <el-menu
        :default-active="activeMenu"
        router
        class="aside-menu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409eff"
      >
        <el-menu-item index="/teacher">
          <span>需求引导</span>
        </el-menu-item>
        <el-menu-item index="/teacher/tools">
          <span>我的工具</span>
        </el-menu-item>
        <el-menu-item index="/teacher/dashboard">
          <span>数据看板</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="header">
        <span class="header-title">教师端</span>
        <el-button type="text" @click="logout">退出登录</el-button>
      </el-header>
      <el-main class="main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const activeMenu = computed(() => route.path)

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}
.aside {
  background-color: #304156;
}
.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: #fff;
  font-size: 20px;
  font-weight: bold;
}
.aside-menu {
  border-right: none;
}
.header {
  background-color: #fff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 1px 4px rgba(0,21,41,.08);
}
.header-title {
  font-size: 18px;
  font-weight: bold;
}
.main {
  background-color: #f0f2f5;
  padding: 20px;
}
</style>
