<template>
  <div>
    <!-- Фильтры -->
    <div class="section-card" style="margin-bottom:24px;">
      <div style="display:flex;gap:16px;flex-wrap:wrap;align-items:flex-end;">
        <div class="form-group" style="margin:0;min-width:150px;">
          <label>Год</label>
          <select v-model="year" class="form-input" @change="load">
            <option value="">Все годы</option>
            <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
          </select>
        </div>
        <div class="form-group" style="margin:0;min-width:240px;">
          <label>Мероприятие</label>
          <select v-model="eventId" class="form-input" @change="load">
            <option value="">Все мероприятия</option>
            <option v-for="ev in eventsList" :key="ev.id" :value="ev.id">{{ ev.title }}</option>
          </select>
        </div>
        <button class="btn" style="background:var(--primary-blue);color:white;" @click="load" :disabled="loading">
          {{ loading ? 'Загрузка...' : 'Обновить' }}
        </button>
      </div>
    </div>

    <div v-if="loading" style="text-align:center;padding:60px;color:var(--text-gray);">Загрузка аналитики...</div>

    <template v-else-if="summary">
      <!-- Сводные карточки -->
      <div class="stats-grid" style="margin-bottom:28px;">
        <div class="stat-card">
          <div class="stat-icon" style="background:#dbeafe;color:#1e40af">
            <svg class="icon"><use href="#ic-calendar"/></svg>
          </div>
          <div class="stat-info"><h3>{{ summary.events_total }}</h3><p>Мероприятий</p></div>
        </div>
        <div class="stat-card">
          <div class="stat-icon" style="background:#d1fae5;color:#065f46">
            <svg class="icon"><use href="#ic-users"/></svg>
          </div>
          <div class="stat-info"><h3>{{ summary.registrations_total }}</h3><p>Регистраций</p></div>
        </div>
        <div class="stat-card">
          <div class="stat-icon" style="background:#fef3c7;color:#92400e">
            <svg class="icon"><use href="#ic-upload"/></svg>
          </div>
          <div class="stat-info"><h3>{{ summary.submissions_total }}</h3><p>Работ подано</p></div>
        </div>
        <div class="stat-card">
          <div class="stat-icon" style="background:#ede9fe;color:#5b21b6">
            <svg class="icon"><use href="#ic-check-circle"/></svg>
          </div>
          <div class="stat-info"><h3>{{ summary.evaluated_total }}</h3><p>Проверено</p></div>
        </div>
      </div>

      <!-- Графики: строка 1 -->
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:24px;" class="charts-grid">
        <!-- График по месяцам -->
        <div class="section-card">
          <h2 style="margin-bottom:16px;">Подача работ по месяцам</h2>
          <div v-if="!monthlyChart.length" style="color:var(--text-gray);text-align:center;padding:40px;">Нет данных</div>
          <div v-else style="position:relative;height:220px;">
            <canvas ref="monthlyChartRef"></canvas>
          </div>
        </div>

        <!-- Круговая: проверено / не проверено -->
        <div class="section-card">
          <h2 style="margin-bottom:16px;">Статус работ</h2>
          <div v-if="!summary.submissions_total" style="color:var(--text-gray);text-align:center;padding:40px;">Нет данных</div>
          <div v-else style="position:relative;height:220px;display:flex;align-items:center;justify-content:center;">
            <canvas ref="statusChartRef" style="max-width:220px;"></canvas>
          </div>
          <div style="display:flex;gap:16px;justify-content:center;flex-wrap:wrap;margin-top:12px;font-size:13px;">
            <span style="display:flex;align-items:center;gap:6px;"><span style="width:12px;height:12px;border-radius:3px;background:#10b981;display:inline-block;"></span>Проверено</span>
            <span style="display:flex;align-items:center;gap:6px;"><span style="width:12px;height:12px;border-radius:3px;background:#f59e0b;display:inline-block;"></span>На проверке</span>
            <span style="display:flex;align-items:center;gap:6px;"><span style="width:12px;height:12px;border-radius:3px;background:#e5e7eb;display:inline-block;"></span>Не проверено</span>
          </div>
        </div>
      </div>

      <!-- Детальный блок конкурса (если выбран) -->
      <template v-if="eventId && eventDetail">
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;margin-bottom:24px;" class="charts-grid">
          <!-- Распределение баллов -->
          <div class="section-card">
            <h2 style="margin-bottom:4px;">Распределение баллов</h2>
            <p style="font-size:13px;color:var(--text-gray);margin-bottom:16px;">
              Средний балл: <strong>{{ eventDetail.summary?.avg_score ?? '—' }}</strong>
            </p>
            <div v-if="!eventDetail.score_distribution?.some(r => r.count > 0)" style="color:var(--text-gray);text-align:center;padding:40px;">Нет оценок</div>
            <div v-else style="position:relative;height:220px;">
              <canvas ref="scoreChartRef"></canvas>
            </div>
          </div>

          <!-- Подача по датам -->
          <div class="section-card">
            <h2 style="margin-bottom:16px;">График сдачи работ</h2>
            <div v-if="!eventDetail.submissions_timeline?.length" style="color:var(--text-gray);text-align:center;padding:40px;">Нет данных</div>
            <div v-else style="position:relative;height:220px;">
              <canvas ref="timelineChartRef"></canvas>
            </div>
          </div>
        </div>

        <!-- Этапы мероприятия -->
        <div v-if="eventDetail.stages?.length" class="section-card" style="margin-bottom:24px;">
          <h2 style="margin-bottom:16px;">Этапы мероприятия</h2>
          <div style="display:flex;gap:12px;flex-wrap:wrap;">
            <div v-for="stage in eventDetail.stages" :key="stage.id"
              style="background:#f1f5f9;border-radius:10px;padding:12px 18px;min-width:160px;">
              <div style="font-size:12px;color:var(--text-gray);margin-bottom:4px;">Этап {{ stage.order }}</div>
              <div style="font-weight:600;font-size:14px;">{{ stage.title }}</div>
              <div style="font-size:13px;color:var(--primary-blue);margin-top:4px;">{{ stage.tasks_count }} заданий</div>
            </div>
          </div>
        </div>
      </template>

      <!-- Таблица по мероприятиям -->
      <div class="section-card" style="margin-bottom:24px;">
        <h2 style="margin-bottom:16px;">По мероприятиям</h2>
        <div v-if="!perEvent.length" style="color:var(--text-gray);text-align:center;padding:20px;">Нет данных</div>
        <div v-else style="overflow-x:auto;">
          <table style="width:100%;border-collapse:collapse;font-size:14px;min-width:500px;">
            <thead>
              <tr style="background:#f1f5f9;">
                <th style="text-align:left;padding:10px 12px;font-weight:600;color:var(--text-gray);">Мероприятие</th>
                <th style="text-align:center;padding:10px 8px;font-weight:600;color:var(--text-gray);">Регистраций</th>
                <th style="text-align:center;padding:10px 8px;font-weight:600;color:var(--text-gray);">Работ</th>
                <th style="text-align:center;padding:10px 8px;font-weight:600;color:var(--text-gray);">Проверено</th>
                <th style="text-align:center;padding:10px 8px;font-weight:600;color:var(--text-gray);">Охват</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="ev in perEvent" :key="ev.id" style="border-bottom:1px solid #f1f5f9;cursor:pointer;"
                @click="selectEvent(ev.id)" :style="eventId == ev.id ? 'background:#eff6ff;' : ''">
                <td style="padding:10px 12px;">
                  <div style="font-weight:500;">{{ ev.title }}</div>
                  <div style="font-size:12px;color:var(--text-gray);">{{ ev.start_date }}</div>
                </td>
                <td style="text-align:center;padding:10px 8px;">{{ ev.registrations }}</td>
                <td style="text-align:center;padding:10px 8px;">{{ ev.submissions }}</td>
                <td style="text-align:center;padding:10px 8px;">{{ ev.evaluated }}</td>
                <td style="text-align:center;padding:10px 8px;">
                  <div style="display:flex;align-items:center;gap:6px;justify-content:center;">
                    <div style="flex:1;max-width:60px;height:6px;background:#e5e7eb;border-radius:3px;overflow:hidden;">
                      <div :style="{ width: ev.registrations > 0 ? Math.round(ev.submissions / ev.registrations * 100) + '%' : '0%', height: '100%', background: '#3b82f6', borderRadius: '3px' }"></div>
                    </div>
                    <span :style="{ color: ev.registrations > 0 && ev.submissions / ev.registrations > 0.7 ? '#065f46' : '#92400e', fontWeight: 600, fontSize: '13px' }">
                      {{ ev.registrations > 0 ? Math.round(ev.submissions / ev.registrations * 100) + '%' : '—' }}
                    </span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Выгрузка Excel -->
      <div class="section-card">
        <h2 style="margin-bottom:6px;">Выгрузить в Excel</h2>
        <p style="font-size:13px;color:var(--text-gray);margin-bottom:16px;">Применяются текущие фильтры{{ year ? ' · ' + year : '' }}{{ eventId ? ' · ' + selectedEventTitle : '' }}</p>
        <div style="display:flex;gap:12px;flex-wrap:wrap;">
          <button class="btn btn-outline" @click="exportReport('submissions')" style="display:flex;align-items:center;gap:8px;">
            <svg class="icon icon-sm"><use href="#ic-download"/></svg>Работы участников
          </button>
          <button class="btn btn-outline" @click="exportReport('events')" style="display:flex;align-items:center;gap:8px;">
            <svg class="icon icon-sm"><use href="#ic-download"/></svg>Мероприятия
          </button>
          <button class="btn btn-outline" @click="exportReport('participants')" style="display:flex;align-items:center;gap:8px;">
            <svg class="icon icon-sm"><use href="#ic-download"/></svg>Участники
          </button>
        </div>
      </div>
    </template>

    <div v-else-if="!loading" style="text-align:center;padding:60px;color:var(--text-gray);">
      <p>Нет данных для отображения</p>
      <p v-if="loadError" style="margin-top:10px;color:#ef4444;font-size:13px;">Ошибка: {{ loadError }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
import api from '@/api/index.js'

Chart.register(...registerables)

// Charts instances
const monthlyChartRef = ref(null)
const statusChartRef = ref(null)
const scoreChartRef = ref(null)
const timelineChartRef = ref(null)

let chartMonthly = null
let chartStatus = null
let chartScore = null
let chartTimeline = null

const year = ref('')
const eventId = ref('')
const loading = ref(false)
const summary = ref(null)
const monthlyChart = ref([])
const perEvent = ref([])
const eventsList = ref([])
const eventDetail = ref(null)
const loadError = ref('')

const years = computed(() => {
  const cur = new Date().getFullYear()
  return [cur, cur - 1, cur - 2, cur - 3]
})

const selectedEventTitle = computed(() => {
  const ev = eventsList.value.find(e => e.id == eventId.value)
  return ev?.title || ''
})

async function load() {
  loading.value = true
  eventDetail.value = null
  destroyCharts()
  try {
    const params = new URLSearchParams()
    if (year.value) params.append('year', year.value)
    if (eventId.value) params.append('event_id', eventId.value)
    const r = await api.get('/api/events/analytics/?' + params.toString())
    summary.value = r.data.summary
    monthlyChart.value = r.data.monthly_chart || []
    perEvent.value = r.data.per_event || []
    if (!eventsList.value.length) {
      eventsList.value = perEvent.value.map(e => ({ id: e.id, title: e.title }))
    }
    if (eventId.value) {
      try {
        const rd = await api.get(`/api/events/${eventId.value}/analytics/`)
        eventDetail.value = rd.data
      } catch {}
    }
  } catch (e) {
    summary.value = null
    loadError.value = e?.response?.status
      ? `HTTP ${e.response.status}: ${JSON.stringify(e.response.data)}`
      : (e?.message || String(e))
  } finally {
    loading.value = false   // сначала скрываем загрузку → DOM обновится
  }
  await nextTick()          // ждём пока canvas появится в DOM
  renderCharts()
  if (eventDetail.value) renderDetailCharts()
}

async function loadEventDetail() {
  if (!eventId.value) return
  destroyCharts()
  try {
    const r = await api.get(`/api/events/${eventId.value}/analytics/`)
    eventDetail.value = r.data
  } catch {}
  await nextTick()
  renderCharts()
  if (eventDetail.value) renderDetailCharts()
}

async function selectEvent(id) {
  eventId.value = (eventId.value == id) ? '' : id   // клик по той же строке — снимает выбор
  await load()
}

function renderCharts() {
  // Monthly bar chart
  if (monthlyChartRef.value && monthlyChart.value.length) {
    chartMonthly = new Chart(monthlyChartRef.value, {
      type: 'bar',
      data: {
        labels: monthlyChart.value.map(m => {
          const [y, mo] = m.month.split('-')
          return `${mo}.${y.slice(2)}`
        }),
        datasets: [{
          label: 'Работ подано',
          data: monthlyChart.value.map(m => m.count),
          backgroundColor: 'rgba(59, 130, 246, 0.8)',
          borderRadius: 6,
          borderSkipped: false,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, ticks: { stepSize: 1 }, grid: { color: '#f1f5f9' } },
          x: { grid: { display: false } }
        }
      }
    })
  }

  // Status doughnut
  if (statusChartRef.value && summary.value?.submissions_total) {
    const evaluated = summary.value.evaluated_total || 0
    const total = summary.value.submissions_total || 0
    const reviewing = Math.max(0, total - evaluated)
    chartStatus = new Chart(statusChartRef.value, {
      type: 'doughnut',
      data: {
        labels: ['Проверено', 'Ожидает проверки'],
        datasets: [{
          data: [evaluated, reviewing],
          backgroundColor: ['#10b981', '#f59e0b'],
          borderWidth: 0,
          hoverOffset: 6,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: '65%',
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: ctx => ` ${ctx.label}: ${ctx.raw} (${total > 0 ? Math.round(ctx.raw / total * 100) : 0}%)`
            }
          }
        }
      }
    })
  }
}

function renderDetailCharts() {
  if (!eventDetail.value) return

  // Score distribution bar
  if (scoreChartRef.value && eventDetail.value.score_distribution) {
    const dist = eventDetail.value.score_distribution
    if (dist.some(r => r.count > 0)) {
      chartScore = new Chart(scoreChartRef.value, {
        type: 'bar',
        data: {
          labels: dist.map(r => r.range),
          datasets: [{
            label: 'Участников',
            data: dist.map(r => r.count),
            backgroundColor: [
              '#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6'
            ],
            borderRadius: 6,
            borderSkipped: false,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } },
          scales: {
            y: { beginAtZero: true, ticks: { stepSize: 1 }, grid: { color: '#f1f5f9' } },
            x: { grid: { display: false } }
          }
        }
      })
    }
  }

  // Timeline line chart
  if (timelineChartRef.value && eventDetail.value.submissions_timeline?.length) {
    const tl = eventDetail.value.submissions_timeline
    chartTimeline = new Chart(timelineChartRef.value, {
      type: 'line',
      data: {
        labels: tl.map(d => {
          const [, m, day] = d.date.split('-')
          return `${day}.${m}`
        }),
        datasets: [{
          label: 'Работ сдано',
          data: tl.map(d => d.count),
          borderColor: '#8b5cf6',
          backgroundColor: 'rgba(139, 92, 246, 0.12)',
          pointBackgroundColor: '#8b5cf6',
          pointRadius: 4,
          fill: true,
          tension: 0.35,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, ticks: { stepSize: 1 }, grid: { color: '#f1f5f9' } },
          x: { grid: { display: false } }
        }
      }
    })
  }
}

function destroyCharts() {
  [chartMonthly, chartStatus, chartScore, chartTimeline].forEach(c => { if (c) { c.destroy() } })
  chartMonthly = chartStatus = chartScore = chartTimeline = null
}

async function exportReport(type) {
  const params = new URLSearchParams({ type })
  if (year.value) params.append('year', year.value)
  if (eventId.value) params.append('event_id', eventId.value)
  try {
    const r = await api.get('/api/events/analytics/export/?' + params.toString(), {
      responseType: 'blob'
    })
    const url = URL.createObjectURL(r.data)
    const a = document.createElement('a')
    a.href = url
    const cd = r.headers['content-disposition'] || ''
    const match = cd.match(/filename="?([^"]+)"?/)
    a.download = match ? match[1] : `report_${type}.xlsx`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  } catch (e) {
    alert('Ошибка при выгрузке: ' + (e?.message || 'неизвестная ошибка'))
  }
}

onMounted(async () => {
  try {
    const r = await api.get('/api/events/')
    eventsList.value = (r.data.results || r.data).map(e => ({ id: e.id, title: e.title }))
  } catch {}
  await load()
})

onUnmounted(() => { destroyCharts() })
</script>

<style scoped>
@media (max-width: 700px) {
  .charts-grid { grid-template-columns: 1fr !important; }
}
</style>
