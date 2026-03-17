import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

const routes = [
  { path: '/', component: () => import('@/views/HomeView.vue') },
  { path: '/auth', component: () => import('@/views/AuthView.vue') },
  { path: '/events', component: () => import('@/views/EventsView.vue') },
  { path: '/events/:id', component: () => import('@/views/EventDetailView.vue') },
  { path: '/documents', component: () => import('@/views/DocumentsView.vue') },
  { path: '/about', component: () => import('@/views/AboutView.vue') },
  { path: '/contacts', component: () => import('@/views/ContactsView.vue') },
  {
    path: '/dashboard',
    redirect: () => {
      const auth = useAuthStore()
      if (!auth.isAuthenticated) return '/auth'
      const map = { admin: '/dashboard/admin', teacher: '/dashboard/teacher', participant: '/dashboard/participant', jury: '/dashboard/jury' }
      return map[auth.user?.role] || '/auth'
    }
  },
  {
    path: '/dashboard/admin',
    component: () => import('@/views/dashboard/AdminDashboard.vue'),
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/dashboard/participant',
    component: () => import('@/views/dashboard/ParticipantDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard/teacher',
    component: () => import('@/views/dashboard/TeacherDashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/dashboard/jury',
    component: () => import('@/views/dashboard/JuryDashboard.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 })
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next('/auth?redirect=' + to.path)
  } else {
    next()
  }
})

export default router
