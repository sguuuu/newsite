<template>
  <div>
    <AppHeader />

    <section class="page-hero">
      <div class="container">
        <h1 class="page-hero-title">Документы и положения</h1>
        <p class="page-hero-subtitle">Нормативные документы, положения, критерии оценивания и другие материалы</p>
      </div>
    </section>

    <section class="section">
      <div class="container">

        <!-- Filter -->
        <div class="filter-tabs" style="margin-bottom:30px; flex-wrap:wrap;">
          <button class="filter-tab" :class="{ active: activeType === '' }" @click="activeType = ''">Все</button>
          <button v-for="t in docTypes" :key="t.value" class="filter-tab" :class="{ active: activeType === t.value }" @click="activeType = t.value">{{ t.label }}</button>
        </div>

        <div v-if="loading" style="text-align:center; padding:60px; color:var(--text-gray);">Загрузка...</div>

        <template v-else-if="filtered.length">
          <!-- Если не выбран тип — показываем по группам -->
          <template v-if="!activeType">
            <div v-for="group in groupedDocs" :key="group.type" style="margin-bottom:40px;">
              <h2 style="font-size:18px; font-weight:600; color:var(--text-dark); margin-bottom:16px; padding-bottom:8px; border-bottom:2px solid var(--primary-blue);">
                {{ typeLabel(group.type) }}
                <span style="font-size:14px; font-weight:400; color:var(--text-gray); margin-left:8px;">{{ group.docs.length }}</span>
              </h2>
              <div style="display:grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap:16px;">
                <div v-for="doc in group.docs" :key="doc.id" class="event-card" style="display:flex; flex-direction:column;">
                  <div style="display:flex; align-items:center; gap:15px; margin-bottom:15px;">
                    <div style="width:48px; height:48px; background:#eff6ff; border-radius:10px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                      <svg class="icon icon-lg" style="color:var(--primary-blue)"><use href="#ic-file"/></svg>
                    </div>
                    <div style="flex:1; min-width:0;">
                      <h3 style="font-size:15px; margin-bottom:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{{ doc.title }}</h3>
                      <span v-if="doc.event_title" style="font-size:11px; color:var(--text-gray);">{{ doc.event_title }}</span>
                    </div>
                  </div>
                  <p v-if="doc.description" style="color:var(--text-gray); font-size:14px; flex:1; margin-bottom:15px;">{{ doc.description }}</p>
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-top:auto;">
                    <span style="color:var(--text-gray); font-size:12px;">{{ doc.file_size_display }} • {{ doc.download_count }} скач.</span>
                    <a :href="'/api/documents/' + doc.id + '/download/'" class="btn btn-outline" style="padding:8px 16px; font-size:14px;">
                      <svg class="icon icon-sm" style="vertical-align:-2px; margin-right:4px;"><use href="#ic-download"/></svg>
                      Скачать
                    </a>
                  </div>
                </div>
              </div>
            </div>
          </template>

          <!-- Если выбран конкретный тип — список без группировки -->
          <div v-else style="display:grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap:20px;">
            <div v-for="doc in filtered" :key="doc.id" class="event-card" style="display:flex; flex-direction:column;">
              <div style="display:flex; align-items:center; gap:15px; margin-bottom:15px;">
                <div style="width:48px; height:48px; background:#eff6ff; border-radius:10px; display:flex; align-items:center; justify-content:center; flex-shrink:0;">
                  <svg class="icon icon-lg" style="color:var(--primary-blue)"><use href="#ic-file"/></svg>
                </div>
                <div style="flex:1; min-width:0;">
                  <h3 style="font-size:15px; margin-bottom:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">{{ doc.title }}</h3>
                  <span v-if="doc.event_title" style="font-size:11px; color:var(--text-gray);">{{ doc.event_title }}</span>
                </div>
              </div>
              <p v-if="doc.description" style="color:var(--text-gray); font-size:14px; flex:1; margin-bottom:15px;">{{ doc.description }}</p>
              <div style="display:flex; justify-content:space-between; align-items:center; margin-top:auto;">
                <span style="color:var(--text-gray); font-size:12px;">{{ doc.file_size_display }} • {{ doc.download_count }} скач.</span>
                <a :href="'/api/documents/' + doc.id + '/download/'" class="btn btn-outline" style="padding:8px 16px; font-size:14px;">
                  <svg class="icon icon-sm" style="vertical-align:-2px; margin-right:4px;"><use href="#ic-download"/></svg>
                  Скачать
                </a>
              </div>
            </div>
          </div>
        </template>

        <div v-else style="text-align:center; padding:60px; color:var(--text-gray);">Документов не найдено</div>
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
import { useRoute, RouterLink } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import api from '@/api/index.js'

const route = useRoute()
const docs = ref([])
const loading = ref(false)
const activeType = ref(route.query.type || '')

const docTypes = [
  { value: 'regulation', label: 'Положения' },
  { value: 'privacy', label: 'Политика конфиденциальности' },
  { value: 'methodology', label: 'Методические материалы' },
  { value: 'template', label: 'Шаблоны' },
  { value: 'criteria', label: 'Критерии оценивания' },
  { value: 'other', label: 'Прочее' },
]

const typeLabels = {
  regulation: 'Положения',
  privacy: 'Политика конфиденциальности',
  methodology: 'Методические материалы',
  template: 'Шаблоны работ',
  criteria: 'Критерии оценивания',
  other: 'Прочее',
}

const filtered = computed(() =>
  activeType.value ? docs.value.filter(d => d.doc_type === activeType.value) : docs.value
)

const groupedDocs = computed(() => {
  const order = ['regulation', 'criteria', 'template', 'methodology', 'privacy', 'other']
  const map = {}
  for (const doc of docs.value) {
    if (!map[doc.doc_type]) map[doc.doc_type] = []
    map[doc.doc_type].push(doc)
  }
  return order.filter(t => map[t]?.length).map(t => ({ type: t, docs: map[t] }))
})

onMounted(async () => {
  loading.value = true
  try {
    const res = await api.get('/api/documents/')
    docs.value = res.data.results || res.data
  } catch {
    docs.value = []
  } finally {
    loading.value = false
  }
})

function typeLabel(t) { return typeLabels[t] || t }
</script>
