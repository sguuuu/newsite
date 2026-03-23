"""
Команда для отправки напоминаний о приближении дедлайна.

Использование:
    python manage.py send_deadline_reminders

Запускать через cron каждый день в 9:00:
    0 9 * * * /path/to/venv/bin/python /path/to/manage.py send_deadline_reminders

Или через systemd timer / любой планировщик задач.
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Отправляет email-напоминания участникам за 7 и 1 день до дедлайна'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            nargs='+',
            type=int,
            default=[7, 1],
            help='За сколько дней до дедлайна отправлять напоминание (по умолчанию: 7 1)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Только показать, кому будут отправлены письма, без реальной отправки',
        )

    def handle(self, *args, **options):
        from apps.events.models import Event, EventRegistration
        from apps.notifications.models import Notification
        from apps.notifications.email_service import send_deadline_reminder_email

        today = timezone.now().date()
        days_list = options['days']
        dry_run = options['dry_run']
        total_sent = 0

        for days_ahead in days_list:
            target_date = today + timedelta(days=days_ahead)

            # Мероприятия с дедлайном ровно через days_ahead дней
            events = Event.objects.filter(
                registration_deadline__date=target_date,
                status__in=['active', 'upcoming'],
            )

            for event in events:
                # Участники, которые зарегистрировались, но ещё не сдали работу
                registrations = EventRegistration.objects.filter(
                    event=event,
                    status__in=['registered', 'active'],
                ).select_related('participant')

                # Исключаем тех, кто уже имеет поданную/оценённую работу
                submitted_participant_ids = event.submissions.filter(
                    status__in=['submitted', 'under_review', 'evaluated']
                ).values_list('participant_id', flat=True)

                for reg in registrations:
                    user = reg.participant
                    if user.id in submitted_participant_ids:
                        continue

                    self.stdout.write(
                        f'  {"[DRY-RUN] " if dry_run else ""}→ {user.email} | '
                        f'{event.title} | через {days_ahead} дн.'
                    )

                    if not dry_run:
                        # Системное уведомление
                        Notification.objects.get_or_create(
                            recipient=user,
                            notif_type='deadline',
                            title=f'Дедлайн через {days_ahead} дн.: «{event.title}»',
                            defaults={
                                'message': f'До срока подачи работ по «{event.title}» осталось {days_ahead} дн.'
                            }
                        )
                        # Email
                        send_deadline_reminder_email(user, event, days_ahead)

                    total_sent += 1

        action = 'Найдено' if dry_run else 'Отправлено'
        self.stdout.write(self.style.SUCCESS(f'{action} напоминаний: {total_sent}'))
