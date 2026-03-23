<template>
  <div>
    <AppHeader />
    <section class="section">
      <div class="container" style="max-width:900px;">
        <div v-if="loading" style="text-align:center; padding:60px; color:var(--text-gray);">Загрузка...</div>
        <div v-else-if="event">
          <!-- Header -->
          <div style="margin-bottom:30px;">
            <RouterLink to="/events" style="color:var(--primary-blue); font-size:14px; text-decoration:none;">← Назад к мероприятиям</RouterLink>
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-top:20px; flex-wrap:wrap; gap:15px;">
              <div>
                <span class="event-badge" :class="statusClass(event.status)" style="margin-bottom:10px; display:inline-block">{{ statusLabel(event.status) }}</span>
                <h1 style="font-size:32px; color:var(--primary-dark); margin-bottom:10px;">{{ event.title }}</h1>
                <p style="color:var(--text-gray); font-size:16px;">{{ typeLabel(event.event_type) }} • {{ formatLabel(event.format) }}</p>
              </div>
              <!-- Не авторизован -->
              <div v-if="!auth.isAuthenticated && isOpenEvent">
                <RouterLink to="/auth" class="btn btn-primary" style="background:var(--primary-blue); color:white; text-decoration:none; display:inline-flex; align-items:center; gap:8px;">
                  <svg class="icon" style="width:16px;height:16px"><use href="#ic-user"/></svg>
                  Войти для участия
                </RouterLink>
              </div>
              <!-- Авторизован как участник -->
              <div v-else-if="canRegister">
                <button v-if="!isRegistered" class="btn btn-primary" style="background:var(--primary-blue); color:white;" @click="register" :disabled="regLoading">
                  {{ regLoading ? 'Регистрируем...' : 'Записаться' }}
                </button>
                <div v-else style="padding:12px 24px; background:#d1fae5; color:#065f46; border-radius:10px; font-weight:600;">Вы зарегистрированы ✓</div>
              </div>
            </div>
          </div>

          <!-- Info cards -->
          <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap:20px; margin-bottom:30px;">
            <div style="background:white; padding:20px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.05);">
              <div style="color:var(--text-gray); font-size:12px; margin-bottom:6px;">Начало</div>
              <div style="font-weight:600;">{{ formatDate(event.start_date) }}</div>
            </div>
            <div style="background:white; padding:20px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.05);">
              <div style="color:var(--text-gray); font-size:12px; margin-bottom:6px;">Окончание</div>
              <div style="font-weight:600;">{{ formatDate(event.end_date) }}</div>
            </div>
            <div style="background:white; padding:20px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.05);">
              <div style="color:var(--text-gray); font-size:12px; margin-bottom:6px;">Срок подачи заявки</div>
              <div style="font-weight:600;">{{ formatDate(event.registration_deadline) }}</div>
            </div>
            <div style="background:white; padding:20px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.05);">
              <div style="color:var(--text-gray); font-size:12px; margin-bottom:6px;">Участников</div>
              <div style="font-weight:600;">{{ event.participant_count || 0 }} / {{ event.max_participants || '∞' }}</div>
            </div>
          </div>

          <!-- Description -->
          <div style="background:white; padding:30px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.05); margin-bottom:30px;">
            <h2 style="font-size:22px; color:var(--primary-dark); margin-bottom:15px;">Описание</h2>
            <div style="line-height:1.8; color:var(--text-dark);">{{ event.description }}</div>
          </div>

          <!-- Age -->
          <div v-if="event.age_min || event.age_max" style="background:white; padding:30px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.05); margin-bottom:30px;">
            <h2 style="font-size:22px; color:var(--primary-dark); margin-bottom:10px;">Возрастные ограничения</h2>
            <p>{{ event.age_min && event.age_max ? `от ${event.age_min} до ${event.age_max} лет` : event.age_min ? `от ${event.age_min} лет` : `до ${event.age_max} лет` }}</p>
          </div>

          <!-- Документы мероприятия -->
          <div v-if="eventDocs.length" style="background:white; padding:30px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.05); margin-bottom:30px;">
            <h2 style="font-size:22px; color:var(--primary-dark); margin-bottom:20px;">Документы мероприятия</h2>
            <div style="display:flex; flex-direction:column; gap:12px;">
              <div v-for="doc in eventDocs" :key="doc.id"
                   style="display:flex; justify-content:space-between; align-items:center; padding:14px 18px; background:#f8fafc; border-radius:10px; border:1px solid #e2e8f0;">
                <div style="display:flex; align-items:center; gap:12px;">
                  <svg class="icon" style="width:20px;height:20px;color:var(--primary-blue);flex-shrink:0"><use href="#ic-file"/></svg>
                  <div>
                    <div style="font-weight:600; font-size:14px;">{{ doc.title }}</div>
                    <div style="font-size:12px; color:var(--text-gray);">{{ docTypeLabel(doc.doc_type) }} · {{ doc.file_size_display }}</div>
                  </div>
                </div>
                <a :href="'/api/documents/' + doc.id + '/download/'"
                   style="display:flex;align-items:center;gap:6px;padding:8px 16px;background:var(--primary-blue);color:white;border-radius:8px;font-size:13px;font-weight:600;text-decoration:none;">
                  <svg class="icon" style="width:14px;height:14px"><use href="#ic-download"/></svg>
                  Скачать
                </a>
              </div>
            </div>
          </div>

          <!-- Error/success messages -->
          <div v-if="regError" style="background:#fef2f2; color:#991b1b; padding:15px; border-radius:8px; margin-bottom:20px;">{{ regError }}</div>
          <div v-if="regSuccess" style="background:#d1fae5; color:#065f46; padding:15px; border-radius:8px; margin-bottom:20px;">{{ regSuccess }}</div>
        </div>
        <div v-else style="text-align:center; padding:60px;">
          <p style="color:var(--text-gray);">Мероприятие не найдено</p>
          <RouterLink to="/events" class="btn btn-outline" style="margin-top:20px; display:inline-block;">Назад</RouterLink>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import { useAuthStore } from '@/stores/auth.js'
import api from '@/api/index.js'

const route = useRoute()
const auth = useAuthStore()
const event = ref(null)
const loading = ref(false)
const isRegistered = ref(false)
const regLoading = ref(false)
const regError = ref('')
const regSuccess = ref('')
const eventDocs = ref([])

const isOpenEvent = computed(() => event.value?.status === 'active' || event.value?.status === 'upcoming')
const canRegister = computed(() => auth.isAuthenticated && auth.user?.role === 'participant' && isOpenEvent.value)

onMounted(async () => {
  loading.value = true
  try {
    const res = await api.get(`/api/events/${route.params.id}/`)
    event.value = res.data
    // Загружаем документы мероприятия
    try {
      const docsRes = await api.get(`/api/documents/?event=${route.params.id}`)
      eventDocs.value = docsRes.data.results || docsRes.data
    } catch {}
    if (auth.isAuthenticated && auth.user?.role === 'participant') {
      try {
        const regs = await api.get('/api/events/my-registrations/')
        const list = regs.data.results || regs.data
        isRegistered.value = list.some(r => r.event === event.value?.id || r.event?.id === event.value?.id)
      } catch {}
    }
  } catch {
    event.value = null
  } finally {
    loading.value = false
  }
})

async function register() {
  regError.value = ''
  regSuccess.value = ''
  regLoading.value = true
  try {
    await api.post(`/api/events/${route.params.id}/register/`)
    isRegistered.value = true
    regSuccess.value = 'Вы успешно зарегистрированы на мероприятие!'
  } catch (e) {
    regError.value = e.response?.data?.detail || 'Ошибка при регистрации'
  } finally {
    regLoading.value = false
  }
}

function formatDate(d) {
  return d ? new Date(d).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' }) : '—'
}
function statusClass(s) {
  return { active: 'status-active', upcoming: 'status-soon', completed: 'status-completed', draft: 'status-pending' }[s] || 'status-pending'
}
function statusLabel(s) {
  return { active: 'Активно', upcoming: 'Скоро', completed: 'Завершено', draft: 'Черновик' }[s] || s
}
function typeLabel(t) { return { olympiad: 'Олимпиада', competition: 'Конкурс' }[t] || t }
function formatLabel(f) { return { online: 'Онлайн', offline: 'Офлайн', hybrid: 'Гибридный' }[f] || f }
function docTypeLabel(t) {
  return { regulation: 'Положение', template: 'Шаблон работы', criteria: 'Критерии оценивания', methodology: 'Метод. материалы', privacy: 'Политика конф.', other: 'Прочее' }[t] || t
}
</script>
