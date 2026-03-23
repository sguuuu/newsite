<template>
  <div>
    <AppHeader />

    <!-- Hero -->
    <section class="hero">
      <div class="container">
        <div class="hero-content">
          <h1 class="hero-title">Школа финансовой культуры</h1>
          <p class="hero-subtitle">Платформа для проведения олимпиад и конкурсов по финансовой грамотности</p>
          <div class="hero-actions">
            <div class="action-card" @click="router.push('/events?type=olympiad')">
              <h3>Олимпиады</h3>
              <p>Проверьте свои знания в области финансов и экономики</p>
              <button class="btn btn-primary">Участвовать</button>
            </div>
            <div class="action-card" @click="router.push('/events?type=competition')">
              <h3>Конкурсы</h3>
              <p>Представьте свои финансовые проекты и идеи</p>
              <button class="btn btn-primary">Участвовать</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- About -->
    <section class="section">
      <div class="container">
        <div class="about-grid">
          <div class="about-text">
            <h2 class="section-title" style="text-align:left; margin-bottom: 20px;">О платформе</h2>
            <p>Школа финансовой культуры — это образовательная платформа Сочинского государственного университета для проведения всероссийских олимпиад и конкурсов по финансовой грамотности.</p>
            <p>Мы создаём условия для развития финансовых компетенций у школьников и студентов, помогаем педагогам организовать образовательный процесс, а экспертам — объективно оценивать работы участников.</p>
            <ul class="features-list">
              <li>
                <svg class="icon" aria-hidden="true"><use href="#ic-check"/></svg>
                Онлайн-регистрация и участие в мероприятиях
              </li>
              <li>
                <svg class="icon" aria-hidden="true"><use href="#ic-check"/></svg>
                Система проверки работ профессиональными экспертами
              </li>
              <li>
                <svg class="icon" aria-hidden="true"><use href="#ic-check"/></svg>
                Электронные сертификаты и дипломы победителям
              </li>
              <li>
                <svg class="icon" aria-hidden="true"><use href="#ic-check"/></svg>
                Персональный кабинет для каждого участника
              </li>
            </ul>
          </div>
          <img
            src="/images/barsik-telescope.png"
            alt="Барсик СочиГУ"
            class="about-img barsik-animate-d1"
          />
        </div>
      </div>
    </section>

    <!-- Events -->
    <section class="section section-light">
      <div class="container">
        <h2 class="section-title">Актуальные мероприятия</h2>
        <div v-if="loading" style="text-align:center; padding: 40px; color: var(--text-gray);">Загрузка...</div>
        <div v-else-if="events.length" class="events-grid">
          <div v-for="event in events" :key="event.id" class="event-card" @click="router.push('/events/' + event.id)" style="cursor:pointer">
            <div class="event-date">{{ formatDate(event.start_date) }}</div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px;">
              <div class="event-badge" :class="statusClass(event.status)">{{ statusLabel(event.status) }}</div>
              <div class="event-badge" style="background:#eff6ff;color:#1e40af;">{{ typeLabel(event.event_type) }}</div>
            </div>
            <h3>{{ event.title }}</h3>
            <p>{{ event.short_description }}</p>
            <button class="btn btn-outline" @click.stop="router.push('/events/' + event.id)">Подробнее</button>
          </div>
        </div>
        <div v-else style="text-align:center; padding: 40px; color: var(--text-gray);">Нет активных мероприятий</div>
        <div style="text-align:center; margin-top: 40px;">
          <RouterLink to="/events" class="btn btn-outline">Все мероприятия</RouterLink>
        </div>
      </div>
    </section>

    <!-- Footer -->
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
              <li><RouterLink to="/auth">Вход / Регистрация</RouterLink></li>
            </ul>
          </div>
          <div class="footer-column">
            <h4>Контакты</h4>
            <p>info@finansy.ru</p>
            <p>+7 (862) 123-45-67</p>
            <p>г. Сочи, ул. Советская, 26а</p>
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
import { ref, onMounted } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import api from '@/api/index.js'

const router = useRouter()
const events = ref([])
const loading = ref(false)

onMounted(async () => {
  loading.value = true
  try {
    const res = await api.get('/api/events/?status=active&page_size=3')
    events.value = res.data.results || res.data
  } catch {
    events.value = []
  } finally {
    loading.value = false
  }
})

function formatDate(date) {
  if (!date) return ''
  return new Date(date).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' })
}

function statusClass(s) {
  return { active: 'status-active', upcoming: 'status-soon', completed: 'status-completed', draft: 'status-pending' }[s] || 'status-pending'
}

function statusLabel(s) {
  return { active: 'Активно', upcoming: 'Скоро', completed: 'Завершено', draft: 'Черновик', cancelled: 'Отменено' }[s] || s
}

function typeLabel(t) {
  return { olympiad: 'Олимпиада', competition: 'Конкурс' }[t] || t
}
</script>
