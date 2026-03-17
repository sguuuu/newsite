<template>
  <header class="header">
    <div class="container">
      <div class="header-content">
        <RouterLink to="/" class="logo">
          <img :src="logoSrc" alt="СочиГУ" class="logo-icon" @error="handleLogoError" ref="logoImg">
          <span class="logo-text">Школа финансовой культуры</span>
        </RouterLink>

        <nav class="nav">
          <ul class="nav-list">
            <li><RouterLink to="/" class="nav-link" :class="{ active: route.path === '/' }">Главная</RouterLink></li>
            <li><RouterLink to="/events" class="nav-link" :class="{ active: route.path.startsWith('/events') }">Мероприятия</RouterLink></li>
            <li><RouterLink to="/documents" class="nav-link" :class="{ active: route.path === '/documents' }">Документы</RouterLink></li>
            <li><RouterLink to="/about" class="nav-link" :class="{ active: route.path === '/about' }">О школе</RouterLink></li>
            <li><RouterLink to="/contacts" class="nav-link" :class="{ active: route.path === '/contacts' }">Контакты</RouterLink></li>
          </ul>
        </nav>

        <div v-if="auth.isAuthenticated" class="user-menu">
          <div class="user-avatar-sm" aria-hidden="true">{{ userInitials }}</div>
          <span class="user-name">{{ auth.user?.first_name || 'Пользователь' }}</span>
          <RouterLink :to="dashboardPath" class="btn-login">Кабинет</RouterLink>
          <button class="btn-logout" @click="handleLogout">Выход</button>
        </div>
        <button v-else class="btn-login" @click="router.push('/auth')">Войти</button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth.js'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const logoImg = ref(null)
const logoSrc = '/images/sochgu-logo.png'

const userInitials = computed(() => {
  if (!auth.user) return 'У'
  return ((auth.user.first_name?.[0] || '') + (auth.user.last_name?.[0] || '')).toUpperCase() || 'У'
})

const dashboardPath = computed(() => {
  const map = { admin: '/dashboard/admin', teacher: '/dashboard/teacher', participant: '/dashboard/participant', jury: '/dashboard/jury' }
  return map[auth.user?.role] || '/dashboard'
})

function handleLogoError() {
  if (logoImg.value) logoImg.value.style.display = 'none'
}

async function handleLogout() {
  await auth.logout()
  router.push('/')
}
</script>
