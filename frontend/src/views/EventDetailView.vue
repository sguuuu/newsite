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

          <!-- Этапы мероприятия -->
          <div v-if="isRegistered && stages.length" style="margin-bottom:30px;">
            <div style="display:flex; align-items:center; gap:12px; margin-bottom:16px;">
              <h2 style="font-size:22px; color:var(--primary-dark); margin:0;">Этапы</h2>
              <span v-if="event.sequential_stages" style="font-size:12px; background:#eff6ff; color:var(--primary-blue); padding:3px 10px; border-radius:20px; font-weight:600;">Последовательный доступ</span>
            </div>

            <!-- Заблокированные этапы (только при sequential_stages) -->
            <div v-if="event.sequential_stages && lockedStages.length" style="margin-bottom:12px;">
              <div v-for="stage in lockedStages" :key="'locked-'+stage.id"
                   style="background:#f1f5f9; border:1px dashed #cbd5e1; border-radius:12px; padding:20px; margin-bottom:10px; opacity:0.7;">
                <div style="display:flex; align-items:center; gap:10px;">
                  <span style="font-size:20px;">🔒</span>
                  <div>
                    <div style="font-weight:600; color:#64748b;">Этап {{ stage.order }}: {{ stage.title }}</div>
                    <div style="font-size:13px; color:#94a3b8; margin-top:2px;">
                      Доступен после сдачи предыдущего этапа{{ stage.start_date ? ' · с ' + formatDate(stage.start_date) : '' }}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Доступные этапы -->
            <div v-for="stage in stages" :key="stage.id"
                 style="background:white; padding:24px; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.05); margin-bottom:16px;">
              <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:14px; flex-wrap:wrap; gap:10px;">
                <div>
                  <div style="font-weight:700; font-size:17px; color:var(--primary-dark);">Этап {{ stage.order }}: {{ stage.title }}</div>
                  <div v-if="stage.start_date" style="font-size:13px; color:var(--text-gray); margin-top:4px;">
                    {{ formatDate(stage.start_date) }} — {{ formatDate(stage.end_date) }}
                  </div>
                </div>
                <span v-if="stageSubmissions[stage.id]" :style="submissionBadgeStyle(stageSubmissions[stage.id].status)" style="font-size:12px; padding:4px 12px; border-radius:20px; font-weight:600;">
                  {{ submissionStatusLabel(stageSubmissions[stage.id].status) }}
                </span>
              </div>
              <p v-if="stage.description" style="color:var(--text-gray); font-size:14px; margin-bottom:16px;">{{ stage.description }}</p>

              <!-- Задания этапа -->
              <div v-if="stage.tasks && stage.tasks.length" style="margin-bottom:16px;">
                <div style="font-weight:600; font-size:14px; margin-bottom:10px; color:var(--primary-dark);">Задания:</div>
                <div v-for="task in stage.tasks" :key="task.id"
                     style="display:flex; justify-content:space-between; align-items:center; padding:12px 16px; background:#f8fafc; border-radius:8px; margin-bottom:8px;">
                  <div>
                    <div style="font-weight:500; font-size:14px;">{{ task.order }}. {{ task.title }}</div>
                    <div v-if="task.description" style="font-size:12px; color:var(--text-gray); margin-top:2px;">{{ task.description }}</div>
                  </div>
                  <div style="display:flex; align-items:center; gap:10px; flex-shrink:0;">
                    <span style="font-size:12px; color:var(--text-gray);">{{ task.max_score }} балл.</span>
                    <a v-if="task.file" :href="task.file" target="_blank"
                       style="font-size:12px; padding:4px 10px; background:var(--primary-blue); color:white; border-radius:6px; text-decoration:none;">
                      Скачать
                    </a>
                  </div>
                </div>
              </div>

              <!-- Загрузка работы по этапу -->
              <div v-if="!stageSubmissions[stage.id] || stageSubmissions[stage.id].status === 'draft'"
                   style="border-top:1px solid #e2e8f0; padding-top:14px;">
                <div style="font-weight:600; font-size:14px; margin-bottom:10px;">Загрузить работу:</div>
                <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
                  <input type="file" @change="e => onStageFileChange(e, stage.id)"
                         style="font-size:13px; flex:1; min-width:200px;"
                         accept=".pdf,.doc,.docx,.xls,.xlsx,.zip,.rar,.txt,.png,.jpg,.jpeg">
                  <button @click="submitStageWork(stage.id)" :disabled="!stageFiles[stage.id] || stageUploading[stage.id]"
                          style="padding:8px 20px; background:var(--primary-blue); color:white; border:none; border-radius:8px; font-size:14px; font-weight:600; cursor:pointer; white-space:nowrap;">
                    {{ stageUploading[stage.id] ? 'Отправляем...' : 'Сдать работу' }}
                  </button>
                </div>
                <div v-if="stageErrors[stage.id]" style="color:#991b1b; font-size:13px; margin-top:8px;">{{ stageErrors[stage.id] }}</div>
                <div v-if="stageSuccess[stage.id]" style="color:#065f46; font-size:13px; margin-top:8px;">{{ stageSuccess[stage.id] }}</div>
              </div>
              <div v-else style="border-top:1px solid #e2e8f0; padding-top:14px; font-size:14px; color:#065f46;">
                ✓ Работа сдана{{ stageSubmissions[stage.id].submitted_at ? ' · ' + formatDate(stageSubmissions[stage.id].submitted_at) : '' }}
              </div>
            </div>
          </div>

          <!-- Error/success messages -->
          <div v-if="regError" style="background:#fef2f2; color:#991b1b; padding:15px; border-radius:8px; margin-bottom:20px;">{{ regError }}</div>
          <div v-if="regSuccess" style="background:#d1fae5; color:#065f46; padding:15px; border-radius:8px; margin-bottom:20px;">{{ regSuccess }}</div>

          <!-- Требуются документы -->
          <div v-if="needsDocs" style="background:#fffbeb; border:1px solid #fcd34d; border-radius:12px; padding:20px; margin-bottom:20px;">
            <div style="font-weight:700; color:#92400e; margin-bottom:8px;">Регистрация принята — требуются документы</div>
            <p style="color:#78350f; font-size:14px; margin-bottom:14px;">
              Для завершения регистрации загрузите необходимые документы в личном кабинете участника:
              <span v-if="event.requires_application"> заявку на участие</span><span v-if="event.requires_application && event.requires_parental_consent">, </span><span v-if="event.requires_parental_consent">согласие родителей</span>.
            </p>
            <RouterLink to="/dashboard/participant" style="display:inline-block; padding:10px 20px; background:#f59e0b; color:white; border-radius:8px; font-weight:600; text-decoration:none;">
              Перейти в кабинет и загрузить →
            </RouterLink>
          </div>
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

const stages = ref([])
const lockedStages = ref([])
const stageSubmissions = ref({})
const stageFiles = ref({})
const stageUploading = ref({})
const stageErrors = ref({})
const stageSuccess = ref({})

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
        const reg = list.find(r => r.event === event.value?.id || r.event?.id === event.value?.id)
        isRegistered.value = !!reg
      } catch {}
      // Загружаем этапы (бэкенд добавляет is_accessible для участников)
      try {
        const stagesRes = await api.get(`/api/events/stages/?event=${route.params.id}`)
        const allStages = stagesRes.data.results || stagesRes.data
        stages.value = allStages.filter(s => s.is_accessible !== false)
        lockedStages.value = allStages.filter(s => s.is_accessible === false)
      } catch {}
      // Загружаем сданные работы участника по этапам
      try {
        const subsRes = await api.get(`/api/submissions/?event=${route.params.id}`)
        const subs = subsRes.data.results || subsRes.data
        subs.forEach(s => { if (s.stage) stageSubmissions.value[s.stage] = s })
      } catch {}
    }
  } catch {
    event.value = null
  } finally {
    loading.value = false
  }
})

const needsDocs = ref(false)

async function register() {
  regError.value = ''
  regSuccess.value = ''
  regLoading.value = true
  try {
    const res = await api.post(`/api/events/${route.params.id}/register/`)
    isRegistered.value = true
    if (res.data?.status === 'pending_docs') {
      needsDocs.value = true
      regSuccess.value = ''
    } else {
      regSuccess.value = 'Вы успешно зарегистрированы на мероприятие!'
    }
  } catch (e) {
    regError.value = e.response?.data?.detail || 'Ошибка при регистрации'
  } finally {
    regLoading.value = false
  }
}

function onStageFileChange(e, stageId) {
  stageFiles.value[stageId] = e.target.files[0] || null
}

async function submitStageWork(stageId) {
  const file = stageFiles.value[stageId]
  if (!file) return
  stageUploading.value[stageId] = true
  stageErrors.value[stageId] = ''
  stageSuccess.value[stageId] = ''
  try {
    const fd = new FormData()
    fd.append('event', route.params.id)
    fd.append('stage', stageId)
    fd.append('file', file)
    const existing = stageSubmissions.value[stageId]
    let res
    if (existing) {
      res = await api.patch(`/api/submissions/${existing.id}/`, fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    } else {
      res = await api.post('/api/submissions/', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
    }
    // Сразу подаём работу (submit)
    await api.post(`/api/submissions/${res.data.id}/submit/`)
    stageSubmissions.value[stageId] = { ...res.data, status: 'submitted' }
    stageSuccess.value[stageId] = 'Работа успешно сдана!'
    // Перезагружаем этапы чтобы обновить доступность
    const stagesRes = await api.get(`/api/events/stages/?event=${route.params.id}`)
    const allStages = stagesRes.data.results || stagesRes.data
    stages.value = allStages.filter(s => s.is_accessible !== false)
    lockedStages.value = allStages.filter(s => s.is_accessible === false)
  } catch (e) {
    stageErrors.value[stageId] = e.response?.data?.detail || Object.values(e.response?.data || {}).flat().join(' ') || 'Ошибка загрузки'
  } finally {
    stageUploading.value[stageId] = false
  }
}

function submissionStatusLabel(s) {
  return { draft: 'Черновик', submitted: 'Подана', under_review: 'На проверке', evaluated: 'Оценена' }[s] || s
}
function submissionBadgeStyle(s) {
  const map = {
    draft: 'background:#f1f5f9;color:#64748b',
    submitted: 'background:#dbeafe;color:#1d4ed8',
    under_review: 'background:#fef3c7;color:#92400e',
    evaluated: 'background:#d1fae5;color:#065f46',
  }
  return map[s] || ''
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
