<template>
  <div>
    <AppHeader />

    <!-- Hero -->
    <section style="background:var(--gradient-hero); padding:60px 0; color:white; text-align:center;">
      <div class="container">
        <h1 style="font-size:40px; font-weight:700; margin-bottom:15px;">О Школе финансовой культуры</h1>
        <p style="font-size:18px; opacity:0.9; max-width:700px; margin:0 auto;">Образовательная платформа Сочинского государственного университета</p>
      </div>
    </section>

    <!-- Mission -->
    <section class="section">
      <div class="container">
        <div class="about-grid">
          <div class="about-text">
            <h2 style="font-size:30px; color:var(--primary-dark); margin-bottom:20px;">Наша миссия</h2>
            <p>Школа финансовой культуры создана для развития финансовой грамотности и формирования устойчивых финансовых компетенций у молодого поколения России.</p>
            <p>Мы объединяем участников, педагогов и экспертов на единой платформе, обеспечивая прозрачность и объективность всех образовательных мероприятий.</p>
            <ul class="features-list" style="margin-top:20px;">
              <li><svg class="icon"><use href="#ic-check"/></svg>Всероссийский охват участников</li>
              <li><svg class="icon"><use href="#ic-check"/></svg>Профессиональная экспертиза</li>
              <li><svg class="icon"><use href="#ic-check"/></svg>Прозрачная система оценки</li>
              <li><svg class="icon"><use href="#ic-check"/></svg>Официальные сертификаты и дипломы</li>
            </ul>
          </div>
          <img
            src="/images/barsik-wave.png"
            alt="Барсик СочиГУ"
            class="about-img barsik-animate-d1"
          />
        </div>
      </div>
    </section>

    <!-- Benefits -->
    <section class="section section-light">
      <div class="container">
        <h2 class="section-title">Для кого платформа</h2>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:30px;">
          <div style="background:white; padding:35px; border-radius:16px; box-shadow:0 4px 15px rgba(0,0,0,0.07); text-align:center;">
            <div style="width:70px; height:70px; background:#eff6ff; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 20px;">
              <svg class="icon icon-xl" style="color:var(--primary-blue)"><use href="#ic-user"/></svg>
            </div>
            <h3 style="margin-bottom:12px; color:var(--primary-dark);">Участникам</h3>
            <p style="color:var(--text-gray); line-height:1.7;">Регистрируйтесь на олимпиады и конкурсы, загружайте работы онлайн, получайте обратную связь от экспертов и официальные дипломы.</p>
          </div>
          <div style="background:white; padding:35px; border-radius:16px; box-shadow:0 4px 15px rgba(0,0,0,0.07); text-align:center;">
            <div style="width:70px; height:70px; background:#f0fdf4; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 20px;">
              <svg class="icon icon-xl" style="color:#065f46"><use href="#ic-users"/></svg>
            </div>
            <h3 style="margin-bottom:12px; color:var(--primary-dark);">Педагогам</h3>
            <p style="color:var(--text-gray); line-height:1.7;">Управляйте списком учеников, отслеживайте их участие и результаты, получайте сводную статистику по классу или группе.</p>
          </div>
          <div style="background:white; padding:35px; border-radius:16px; box-shadow:0 4px 15px rgba(0,0,0,0.07); text-align:center;">
            <div style="width:70px; height:70px; background:#fffbeb; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 20px;">
              <svg class="icon icon-xl" style="color:#92400e"><use href="#ic-scale"/></svg>
            </div>
            <h3 style="margin-bottom:12px; color:var(--primary-dark);">Экспертам жюри</h3>
            <p style="color:var(--text-gray); line-height:1.7;">Проверяйте работы по чётким критериям, давайте развёрнутую обратную связь и публикуйте результаты в режиме реального времени.</p>
          </div>
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
import AppHeader from '@/components/AppHeader.vue'
import { RouterLink } from 'vue-router'
</script>
