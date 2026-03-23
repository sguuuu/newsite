<template>
  <div>
    <AppHeader />

    <section class="page-hero">
      <div class="container">
        <h1 class="page-hero-title">Мероприятия</h1>
        <p class="page-hero-subtitle">Олимпиады и конкурсы по финансовой грамотности</p>
      </div>
    </section>

    <section class="section">
      <div class="container">

        <!-- Основные вкладки -->
        <div class="filter-tabs" style="margin-bottom:24px;">
          <button class="filter-tab" :class="{ active: mainTab === 'olympiad' }" @click="setMainTab('olympiad')">Олимпиады</button>
          <button class="filter-tab" :class="{ active: mainTab === 'competition' }" @click="setMainTab('competition')">Конкурсы</button>
          <button class="filter-tab" :class="{ active: mainTab === 'archive' }" @click="setMainTab('archive')">Архив</button>
        </div>

        <!-- Фильтры для Олимпиад -->
        <div v-if="mainTab === 'olympiad'" style="display:flex; gap:12px; flex-wrap:wrap; margin-bottom:24px; align-items:center;">
          <div class="filter-tabs" style="margin-bottom:0;">
            <button class="filter-tab" :class="{ active: movementFilter === '' }" @click="movementFilter = ''">Все направления</button>
            <button class="filter-tab" :class="{ active: movementFilter === 'olympiad_movement' }" @click="movementFilter = 'olympiad_movement'">Подготовительно-олимпиадное</button>
            <button class="filter-tab" :class="{ active: movementFilter === 'career_guidance' }" @click="movementFilter = 'career_guidance'">Профориентационное</button>
          </div>
          <div class="filter-tabs" style="margin-bottom:0; margin-left:auto;">
            <button class="filter-tab" :class="{ active: statusFilter === '' }" @click="statusFilter = ''">Все статусы</button>
            <button class="filter-tab" :class="{ active: statusFilter === 'active' }" @click="statusFilter = 'active'">Активные</button>
            <button class="filter-tab" :class="{ active: statusFilter === 'upcoming' }" @click="statusFilter = 'upcoming'">Предстоящие</button>
          </div>
        </div>

        <!-- Фильтры для Конкурсов -->
        <div v-else-if="mainTab === 'competition'" style="display:flex; gap:12px; flex-wrap:wrap; margin-bottom:24px; align-items:center; justify-content:flex-end;">
          <div class="filter-tabs" style="margin-bottom:0;">
            <button class="filter-tab" :class="{ active: statusFilter === '' }" @click="statusFilter = ''">Все статусы</button>
            <button class="filter-tab" :class="{ active: statusFilter === 'active' }" @click="statusFilter = 'active'">Активные</button>
            <button class="filter-tab" :class="{ active: statusFilter === 'upcoming' }" @click="statusFilter = 'upcoming'">Предстоящие</button>
          </div>
        </div>

        <!-- Фильтры для архива -->
        <div v-else style="display:flex; gap:12px; flex-wrap:wrap; margin-bottom:24px; align-items:center;">
          <div class="filter-tabs" style="margin-bottom:0;">
            <button class="filter-tab" :class="{ active: archiveTypeFilter === '' }" @click="archiveTypeFilter = ''">Все типы</button>
            <button class="filter-tab" :class="{ active: archiveTypeFilter === 'olympiad' }" @click="archiveTypeFilter = 'olympiad'">Олимпиады</button>
            <button class="filter-tab" :class="{ active: archiveTypeFilter === 'competition' }" @click="archiveTypeFilter = 'competition'">Конкурсы</button>
          </div>
          <div class="filter-tabs" style="margin-bottom:0; margin-left:auto;">
            <button class="filter-tab" :class="{ active: movementFilter === '' }" @click="movementFilter = ''">Все направления</button>
            <button class="filter-tab" :class="{ active: movementFilter === 'olympiad_movement' }" @click="movementFilter = 'olympiad_movement'">Олимпиадное</button>
            <button class="filter-tab" :class="{ active: movementFilter === 'career_guidance' }" @click="movementFilter = 'career_guidance'">Профориентационное</button>
          </div>
        </div>

        <div v-if="loading" style="text-align:center; padding: 60px; color: var(--text-gray);">Загрузка...</div>
        <div v-else-if="filtered.length" class="events-grid">
          <div v-for="event in filtered" :key="event.id" class="event-card" style="cursor:pointer" @click="router.push('/events/' + event.id)">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
              <span class="event-date">{{ formatDate(event.start_date) }}</span>
              <span class="event-badge" :class="statusClass(event.status)">{{ statusLabel(event.status) }}</span>
            </div>
            <h3>{{ event.title }}</h3>
            <p>{{ event.short_description }}</p>
            <div style="display:flex; justify-content:space-between; align-items:center; font-size:13px; color: var(--text-gray); margin-bottom:6px;">
              <span>{{ typeLabel(event.event_type) }}</span>
              <span>{{ event.participant_count || 0 }} участников</span>
            </div>
            <div style="font-size:12px; color:var(--text-gray); margin-bottom:15px;">
              <span style="background:#f3f4f6; padding:2px 8px; border-radius:6px;">{{ movementLabel(event.movement_type) }}</span>
            </div>
            <div style="display:flex; gap:10px; flex-wrap:wrap;">
              <button class="btn btn-outline" @click.stop="router.push('/events/' + event.id)">Подробнее</button>
              <!-- Не авторизован + мероприятие открыто -->
              <RouterLink
                v-if="!auth.isAuthenticated && (event.status === 'active' || event.status === 'upcoming')"
                to="/auth"
                class="btn btn-primary"
                style="background:var(--primary-blue); color:white; text-decoration:none; font-size:13px;"
                @click.stop
              >Войти для участия</RouterLink>
              <!-- Участник + мероприятие открыто -->
              <button
                v-else-if="auth.isAuthenticated && auth.user?.role === 'participant' && (event.status === 'active' || event.status === 'upcoming')"
                class="btn btn-primary"
                style="background:var(--primary-blue); color:white; font-size:13px;"
                @click.stop="router.push('/events/' + event.id)"
              >Записаться</button>
            </div>
          </div>
        </div>
        <div v-else style="text-align:center; padding: 60px; color: var(--text-gray);">
          <p style="font-size:18px; margin-bottom:10px;">Мероприятий не найдено</p>
          <p style="font-size:14px;">Попробуйте изменить фильтры</p>
        </div>
      </div>
    </section>

    <footer class="footer">
      <div class="container">
        <div class="footer-content">
          <div class="footer-column">
            <h4>Школа финансовой культуры</h4>
            <p>Платформа Сочинского государственного университета</p>
          </div>
          <div class="footer-column">
            <h4>Мероприятия</h4>
            <ul class="footer-links">
              <li><RouterLink to="/events?type=olympiad">Олимпиады</RouterLink></li>
              <li><RouterLink to="/events?type=competition">Конкурсы</RouterLink></li>
              <li><RouterLink to="/documents">Документы</RouterLink></li>
            </ul>
          </div>
          <div class="footer-column">
            <h4>О платформе</h4>
            <ul class="footer-links">
              <li><RouterLink to="/about">О школе</RouterLink></li>
              <li><RouterLink to="/contacts">Контакты</RouterLink></li>
            </ul>
          </div>
          <div class="footer-column">
            <h4>Контакты</h4>
            <p>info@finansy.ru</p>
            <p>+7 (862) 123-45-67</p>
          </div>
        </div>
        <div class="footer-bottom">
          <p>© {{ new Date().getFullYear() }} Школа финансовой культуры. Сочинский государственный университет.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter, RouterLink } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import api from '@/api/index.js'
import { useAuthStore } from '@/stores/auth.js'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()
const events = ref([])
const loading = ref(false)

// Определяем начальную вкладку из query-параметра
const initialType = route.query.type || 'olympiad'
const mainTab = ref(['olympiad', 'competition', 'archive'].includes(initialType) ? initialType : 'olympiad')
const movementFilter = ref('')
const statusFilter = ref('')
const archiveTypeFilter = ref('')

function setMainTab(tab) {
  mainTab.value = tab
  movementFilter.value = ''
  statusFilter.value = ''
  archiveTypeFilter.value = ''
}

const filtered = computed(() => {
  if (mainTab.value === 'archive') {
    return events.value.filter(e => {
      if (e.status !== 'completed' && e.status !== 'cancelled') return false
      if (archiveTypeFilter.value && e.event_type !== archiveTypeFilter.value) return false
      if (movementFilter.value && e.movement_type !== movementFilter.value) return false
      return true
    })
  }
  return events.value.filter(e => {
    if (e.event_type !== mainTab.value) return false
    if (e.status === 'completed' || e.status === 'cancelled') return false
    if (statusFilter.value && e.status !== statusFilter.value) return false
    if (movementFilter.value && e.movement_type !== movementFilter.value) return false
    return true
  })
})

onMounted(fetchEvents)

async function fetchEvents() {
  loading.value = true
  try {
    const res = await api.get('/api/events/')
    events.value = res.data.results || res.data
  } catch {
    events.value = []
  } finally {
    loading.value = false
  }
}

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' }) : ''
}
function statusClass(s) {
  return { active: 'status-active', upcoming: 'status-soon', completed: 'status-completed', draft: 'status-pending', cancelled: 'status-pending' }[s] || 'status-pending'
}
function statusLabel(s) {
  return { active: 'Активно', upcoming: 'Скоро', completed: 'Завершено', draft: 'Черновик', cancelled: 'Отменено' }[s] || s
}
function typeLabel(t) {
  return { olympiad: 'Олимпиада', competition: 'Конкурс' }[t] || t
}
function movementLabel(m) {
  return { olympiad_movement: 'Олимпиадное движение', career_guidance: 'Профориентационное движение' }[m] || m
}
</script>
