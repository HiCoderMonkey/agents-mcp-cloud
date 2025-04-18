import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Login from '../views/Login.vue'
import Agents from '../views/Agents.vue'
import AgentDetail from '../views/AgentDetail.vue'
import SDKKeys from '../views/SDKKeys.vue'
import MCPServers from '../views/MCPServers.vue'
import MCPServerDetail from '../views/MCPServerDetail.vue'
import MCPServerForm from '../views/MCPServerForm.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { guest: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/Register.vue'),
    meta: { guest: true }
  },
  {
    path: '/mcp-servers',
    name: 'MCPServers',
    component: MCPServers,
    meta: { requiresAuth: true }
  },
  {
    path: '/mcp-servers/create',
    name: 'CreateMCPServer',
    component: MCPServerForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/mcp-servers/:id',
    name: 'MCPServerDetail',
    component: MCPServerDetail,
    meta: { requiresAuth: true }
  },
  {
    path: '/mcp-servers/:id/edit',
    name: 'EditMCPServer',
    component: MCPServerForm,
    meta: { requiresAuth: true }
  },
  {
    path: '/agents',
    name: 'Agents',
    component: Agents,
    meta: { requiresAuth: true }
  },
  {
    path: '/agents/:id',
    name: 'AgentDetail',
    component: AgentDetail,
    meta: { requiresAuth: true }
  },
  {
    path: '/sdk-keys',
    name: 'SDKKeys',
    component: SDKKeys,
    meta: { requiresAuth: true }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('../views/Profile.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    component: () => import('../views/ResetPassword.vue')
  },
  {
    path: '*',
    redirect: '/'
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('token')
  
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!loggedIn) {
      next('/login')
    } else {
      next()
    }
  } else if (to.matched.some(record => record.meta.guest)) {
    if (loggedIn) {
      next('/')
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router 