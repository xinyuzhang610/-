import { createRouter, createWebHistory } from 'vue-router'

// 路由配置
const routes = [
  // 登录注册页（不需要布局）
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { requiresAuth: false }
  },

  // 功能详情页
  {
    path: '/feature/discover',
    name: 'FeatureDiscover',
    component: () => import('../views/feature/Discover.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/feature/agent',
    name: 'FeatureAgent',
    component: () => import('../views/feature/Agent.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/feature/resource',
    name: 'FeatureResource',
    component: () => import('../views/feature/Resource.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/feature/path',
    name: 'FeaturePath',
    component: () => import('../views/feature/Path.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/feature/analysis',
    name: 'FeatureAnalysis',
    component: () => import('../views/feature/Analysis.vue'),
    meta: { requiresAuth: false }
  },

  // 教程页面
  {
    path: '/tutorial/guide',
    name: 'TutorialGuide',
    component: () => import('../views/tutorial/Guide.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/tutorial/share',
    name: 'TutorialShare',
    component: () => import('../views/tutorial/Share.vue'),
    meta: { requiresAuth: false }
  },

  // 教师端（需要登录）
  {
    path: '/teacher',
    component: () => import('../layout/index.vue'),
    meta: { requiresAuth: true, role: 'teacher' },
    children: [
      {
        path: '',
        redirect: '/teacher/home'
      },
      {
        path: 'home',
        name: 'TeacherHome',
        component: () => import('../views/teacher/Home.vue'),
        meta: { title: '需求引导' }
      },
      {
        path: 'tools',
        name: 'TeacherTools',
        component: () => import('../views/teacher/Tools.vue'),
        meta: { title: '我的工具' }
      },
      {
        path: 'dashboard',
        name: 'TeacherDashboard',
        component: () => import('../views/teacher/Dashboard.vue'),
        meta: { title: '数据看板' }
      }
    ]
  },

  // 学生端（不需要登录）
  {
    path: '/student',
    component: () => import('../layout/index.vue'),
    meta: { requiresAuth: false },
    children: [
      {
        path: '',
        redirect: '/student/plaza'
      },
      {
        path: 'plaza',
        name: 'StudentPlaza',
        component: () => import('../views/student/Plaza.vue'),
        meta: { title: '工具广场' }
      },
      {
        path: 'chat',
        name: 'StudentChat',
        component: () => import('../views/student/Chat.vue'),
        meta: { title: 'AI问答' }
      },
      {
        path: 'records',
        name: 'StudentRecords',
        component: () => import('../views/student/Records.vue'),
        meta: { title: '学习记录' }
      },
      {
        path: 'guidance',
        name: 'StudentGuidance',
        component: () => import('../views/student/Guidance.vue'),
        meta: { title: '需求引导' }
      }
    ]
  },

  // 工具使用页（独立布局，适合分享链接访问）
  {
    path: '/tool/:id',
    name: 'ToolUse',
    component: () => import('../views/student/ToolUse.vue'),
    meta: { requiresAuth: false }
  },

  // 首页（小米风格落地页）
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { requiresAuth: false }
  },

  // 404页面
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  // 需要登录的页面
  if (to.meta.requiresAuth && !token) {
    next('/login')
    return
  }

  // 已登录访问登录页，跳转到教师端首页
  if (to.path === '/login' && token) {
    next('/teacher/home')
    return
  }

  next()
})

export default router
