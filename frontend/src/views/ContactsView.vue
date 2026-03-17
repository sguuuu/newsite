<template>
  <div>
    <AppHeader />

    <section style="background:var(--gradient-hero); padding:60px 0; color:white; text-align:center;">
      <div class="container">
        <img src="/images/barsik-letter.png" alt="Барсик СочиГУ" class="barsik-hero-img barsik-animate" />
        <h1 style="font-size:40px; font-weight:700; margin-bottom:15px;" class="barsik-animate-d1">Контакты</h1>
        <p style="font-size:18px; opacity:0.9;" class="barsik-animate-d2">Свяжитесь с нами любым удобным способом</p>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap:30px; margin-bottom:60px;">
          <div style="background:white; padding:35px; border-radius:16px; box-shadow:0 4px 15px rgba(0,0,0,0.07); text-align:center;">
            <div class="contact-icon" style="background:#eff6ff;">
              <svg class="icon" style="width:36px;height:36px;"><use href="#ic-mail"/></svg>
            </div>
            <h3 style="margin-bottom:10px; color:var(--primary-dark);">Email</h3>
            <p style="color:var(--text-gray);">info@finansy.ru</p>
            <p style="color:var(--text-gray);">support@finansy.ru</p>
          </div>
          <div style="background:white; padding:35px; border-radius:16px; box-shadow:0 4px 15px rgba(0,0,0,0.07); text-align:center;">
            <div class="contact-icon" style="background:#f0fdf4;">
              <svg class="icon" style="width:36px;height:36px;"><use href="#ic-phone"/></svg>
            </div>
            <h3 style="margin-bottom:10px; color:var(--primary-dark);">Телефон</h3>
            <p style="color:var(--text-gray);">+7 (862) 123-45-67</p>
            <p style="color:var(--text-gray);">Пн–Пт: 9:00–18:00</p>
          </div>
          <div style="background:white; padding:35px; border-radius:16px; box-shadow:0 4px 15px rgba(0,0,0,0.07); text-align:center;">
            <div class="contact-icon" style="background:#fffbeb;">
              <svg class="icon" style="width:36px;height:36px;"><use href="#ic-location"/></svg>
            </div>
            <h3 style="margin-bottom:10px; color:var(--primary-dark);">Адрес</h3>
            <p style="color:var(--text-gray);">354000, г. Сочи,</p>
            <p style="color:var(--text-gray);">ул. Советская, 26а</p>
          </div>
        </div>

        <!-- Contact form -->
        <div style="max-width:600px; margin:0 auto; background:white; padding:40px; border-radius:16px; box-shadow:0 4px 20px rgba(0,0,0,0.08);">
          <h2 style="font-size:26px; color:var(--primary-dark); margin-bottom:25px;">Написать нам</h2>
          <form @submit.prevent="sendMessage">
            <div class="form-row">
              <div class="form-group">
                <label>Имя</label>
                <input v-model="form.name" type="text" class="form-input" placeholder="Ваше имя" required>
              </div>
              <div class="form-group">
                <label>Email</label>
                <input v-model="form.email" type="email" class="form-input" placeholder="your@email.com" required>
              </div>
            </div>
            <div class="form-group">
              <label>Тема</label>
              <input v-model="form.subject" type="text" class="form-input" placeholder="Тема обращения" required>
            </div>
            <div class="form-group">
              <label>Сообщение</label>
              <textarea v-model="form.message" class="form-input" rows="5" placeholder="Ваше сообщение..." style="resize:vertical;" required></textarea>
            </div>
            <div v-if="sent" style="background:#d1fae5; color:#065f46; padding:12px; border-radius:8px; margin-bottom:15px;">Сообщение отправлено! Мы свяжемся с вами в ближайшее время.</div>
            <button type="submit" class="btn" style="background:var(--primary-blue); color:white; width:100%;">Отправить</button>
          </form>
        </div>

        <!-- FAQ -->
        <div style="max-width:700px; margin:60px auto 0;">
          <h2 class="section-title" style="margin-bottom:30px;">Частые вопросы</h2>
          <div v-for="(item, i) in faq" :key="i" style="background:white; border-radius:12px; margin-bottom:12px; box-shadow:0 2px 8px rgba(0,0,0,0.05); overflow:hidden;">
            <button @click="item.open = !item.open" style="width:100%; text-align:left; padding:20px 25px; border:none; background:none; cursor:pointer; display:flex; justify-content:space-between; align-items:center; font-size:15px; font-weight:600; color:var(--text-dark);">
              {{ item.q }}
              <span style="font-size:20px; color:var(--primary-blue);">{{ item.open ? '−' : '+' }}</span>
            </button>
            <div v-if="item.open" style="padding:0 25px 20px; color:var(--text-gray); line-height:1.7;">{{ item.a }}</div>
          </div>
        </div>
      </div>
    </section>

    <footer class="footer">
      <div class="container">
        <div class="footer-bottom">
          <p>© {{ new Date().getFullYear() }} Школа финансовой культуры. Сочинский государственный университет.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import AppHeader from '@/components/AppHeader.vue'

const sent = ref(false)
const form = reactive({ name: '', email: '', subject: '', message: '' })

function sendMessage() {
  // Здесь будет реальная отправка через API
  sent.value = true
  Object.assign(form, { name: '', email: '', subject: '', message: '' })
  setTimeout(() => { sent.value = false }, 5000)
}

const faq = reactive([
  { q: 'Как зарегистрироваться на мероприятие?', a: 'Создайте аккаунт на платформе, войдите в личный кабинет и нажмите "Записаться" на странице нужного мероприятия.', open: false },
  { q: 'Как загрузить работу?', a: 'После регистрации на мероприятие в вашем личном кабинете появится раздел "Мои работы". Там вы можете загрузить файл с работой в форматах PDF, DOC, DOCX.', open: false },
  { q: 'Когда будут объявлены результаты?', a: 'Результаты публикуются в личном кабинете участника после завершения проверки работ всеми экспертами жюри. Вы также получите уведомление на email.', open: false },
  { q: 'Как получить сертификат?', a: 'Электронный сертификат участника формируется автоматически и доступен для скачивания в разделе "Результаты" вашего личного кабинета.', open: false }
])
</script>
