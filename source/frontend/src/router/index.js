import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/auth/Register.vue')
  },
  {
    path: '/teacher',
    component: () => import('../layouts/TeacherLayout.vue'),
    children: [
      {
        path: '',
        name: 'TeacherHome',
        component: () => import('../views/teacher/Guidance.vue')
      },
      {
        path: 'tools',
        name: 'TeacherTools',
        component: () => import('../views/teacher/MyTools.vue')
      },
      {
        path: 'dashboard',
        name: 'TeacherDashboard',
        component: () => import('../views/teacher/Dashboard.vue')
      }
    ]
  },
  {
    path: '/student',
    component: () => import('../layouts/StudentLayout.vue'),
    children: [
      {
        path: '',
        name: 'StudentHome',
        component: () => import('../views/student/Guidance.vue')
      },
      {
        path: 'plaza',
        name: 'StudentPlaza',
        component: () => import('../views/student/Plaza.vue')
      },
      {
        path: 'tool/:toolId',
        name: 'StudentTool',
        component: () => import('../views/student/ToolUse.vue')
      },
      {
        path: 'chat',
        name: 'StudentChat',
        component: () => import('../views/student/AIChat.vue')
      },
      {
        path: 'records',
        name: 'StudentRecords',
        component: () => import('../views/student/Records.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
