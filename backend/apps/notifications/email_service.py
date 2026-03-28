"""
Централизованная отправка email-уведомлений.

Все функции принимают объект пользователя (User) и дополнительные данные.
В режиме разработки (EMAIL_BACKEND=console) письма выводятся в консоль —
реальная отправка начнётся после настройки SMTP в .env.
"""
from django.conf import settings
from django.core.mail import send_mail
from django.utils.html import strip_tags


def _send(recipient_email: str, subject: str, html_body: str) -> None:
    """Базовая отправка одного письма."""
    try:
        send_mail(
            subject=subject,
            message=strip_tags(html_body),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            html_message=html_body,
            fail_silently=False,
        )
    except Exception as exc:
        # Не ломаем основной запрос из-за ошибки отправки
        import logging
        logging.getLogger(__name__).error('Email send error to %s: %s', recipient_email, exc)


# ─── Шаблоны ──────────────────────────────────────────────────────────────────

def _base_template(title: str, body: str) -> str:
    return f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;background:#f8fafc;padding:30px;">
      <div style="background:linear-gradient(135deg,#1e40af,#2563eb);padding:24px 30px;border-radius:12px 12px 0 0;">
        <h1 style="color:white;margin:0;font-size:20px;">Школа финансовой культуры</h1>
        <p style="color:rgba(255,255,255,0.8);margin:4px 0 0;font-size:13px;">СочиГУ · finansy.ru</p>
      </div>
      <div style="background:white;padding:30px;border-radius:0 0 12px 12px;box-shadow:0 4px 15px rgba(0,0,0,0.07);">
        <h2 style="color:#1e3a5f;margin-top:0;">{title}</h2>
        {body}
        <hr style="border:none;border-top:1px solid #e2e8f0;margin:24px 0;">
        <p style="color:#94a3b8;font-size:12px;margin:0;">
          Это автоматическое письмо. Не отвечайте на него.<br>
          © Школа финансовой культуры, Сочинский государственный университет
        </p>
      </div>
    </div>
    """


# ─── Конкретные письма ────────────────────────────────────────────────────────

def send_registration_email(user, event) -> None:
    """Письмо после регистрации на мероприятие."""
    body = f"""
    <p>Здравствуйте, <strong>{user.first_name or user.email}</strong>!</p>
    <p>Вы успешно зарегистрировались на мероприятие:</p>
    <div style="background:#eff6ff;border-left:4px solid #2563eb;padding:16px 20px;border-radius:8px;margin:16px 0;">
      <strong style="color:#1e40af;font-size:16px;">{event.title}</strong><br>
      <span style="color:#64748b;font-size:13px;">
        Тип: {{'olympiad':'Олимпиада','competition':'Конкурс'}}.get(event.event_type, event.event_type)
      </span>
    </div>
    <p><strong>Дата начала:</strong> {event.start_date.strftime('%d.%m.%Y') if event.start_date else '—'}</p>
    <p><strong>Срок подачи заявки:</strong> {event.registration_deadline.strftime('%d.%m.%Y') if event.registration_deadline else '—'}</p>
    <p style="margin-top:20px;">
      <a href="{settings.FRONTEND_URL}/events/{event.id}"
         style="background:#2563eb;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:600;">
        Открыть мероприятие
      </a>
    </p>
    """
    _send(user.email, f'Регистрация на «{event.title}»', _base_template('Регистрация подтверждена ✓', body))


def send_evaluation_email(user, event, score, feedback) -> None:
    """Письмо участнику о выставленной оценке."""
    feedback_block = f"""
    <div style="background:#f8fafc;border:1px solid #e2e8f0;padding:16px;border-radius:8px;margin:16px 0;">
      <strong>Комментарий жюри:</strong>
      <p style="margin:8px 0 0;color:#374151;">{feedback}</p>
    </div>
    """ if feedback else ''

    body = f"""
    <p>Здравствуйте, <strong>{user.first_name or user.email}</strong>!</p>
    <p>Жюри проверило вашу работу по мероприятию <strong>«{event.title}»</strong>.</p>
    <div style="background:#d1fae5;border-left:4px solid #059669;padding:16px 20px;border-radius:8px;margin:16px 0;">
      <span style="color:#065f46;font-size:24px;font-weight:700;">{score} баллов</span>
    </div>
    {feedback_block}
    <p style="margin-top:20px;">
      <a href="{settings.FRONTEND_URL}/dashboard"
         style="background:#2563eb;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:600;">
        Открыть личный кабинет
      </a>
    </p>
    """
    _send(user.email, f'Результаты проверки: «{event.title}»', _base_template('Ваша работа проверена', body))


def send_deadline_reminder_email(user, event, days_left: int) -> None:
    """Напоминание о приближении дедлайна подачи работы."""
    body = f"""
    <p>Здравствуйте, <strong>{user.first_name or user.email}</strong>!</p>
    <p>Напоминаем: до окончания срока подачи работ по мероприятию
       <strong>«{event.title}»</strong> осталось <strong>{days_left} дн.</strong></p>
    <p><strong>Дедлайн:</strong> {event.registration_deadline.strftime('%d.%m.%Y')}</p>
    <p style="margin-top:20px;">
      <a href="{settings.FRONTEND_URL}/events/{event.id}"
         style="background:#d97706;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:600;">
        Подать работу
      </a>
    </p>
    """
    _send(user.email, f'Дедлайн через {days_left} дн.: «{event.title}»',
          _base_template(f'⏰ Напоминание о дедлайне', body))


def send_admin_registration_request_email(admin, new_user) -> None:
    """Уведомление администратору о новой заявке на регистрацию (педагог/жюри)."""
    role_names = {'teacher': 'Педагог', 'jury': 'Жюри'}
    role_label = role_names.get(new_user.role, new_user.role)
    body = f"""
    <p>Здравствуйте, <strong>{admin.first_name or admin.email}</strong>!</p>
    <p>Поступила новая заявка на регистрацию в роли <strong>{role_label}</strong>:</p>
    <div style="background:#eff6ff;border-left:4px solid #2563eb;padding:16px 20px;border-radius:8px;margin:16px 0;">
      <strong style="color:#1e40af;font-size:16px;">{new_user.full_name}</strong><br>
      <span style="color:#64748b;font-size:13px;">Email: {new_user.email}</span><br>
      <span style="color:#64748b;font-size:13px;">Учреждение: {new_user.institution or '—'}</span><br>
      <span style="color:#64748b;font-size:13px;">Должность/класс: {new_user.grade_or_position or '—'}</span>
    </div>
    <p>Для подтверждения или отклонения заявки перейдите в панель администратора:</p>
    <p style="margin-top:20px;">
      <a href="{settings.FRONTEND_URL}/dashboard/admin"
         style="background:#2563eb;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:600;">
        Открыть панель управления
      </a>
    </p>
    """
    _send(
        admin.email,
        f'Новая заявка на регистрацию: {new_user.full_name} ({role_label})',
        _base_template(f'Заявка на регистрацию — {role_label}', body),
    )


def send_password_reset_email(user, reset_link: str) -> None:
    """Письмо со ссылкой для сброса пароля."""
    body = f"""
    <p>Здравствуйте, <strong>{user.first_name or user.email}</strong>!</p>
    <p>Мы получили запрос на сброс пароля для вашей учётной записи.</p>
    <p style="margin-top:20px;">
      <a href="{reset_link}"
         style="background:#2563eb;color:white;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:600;">
        Сбросить пароль
      </a>
    </p>
    <p style="color:#94a3b8;font-size:13px;margin-top:16px;">
      Ссылка действует <strong>1 час</strong>.<br>
      Если вы не запрашивали сброс пароля — просто проигнорируйте это письмо.
    </p>
    """
    _send(user.email, 'Сброс пароля', _base_template('Сброс пароля', body))
