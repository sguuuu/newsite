"""
Тестовые данные для аналитики.
Запуск: python manage.py seed_analytics
"""
import random
from datetime import date, timedelta, datetime
from django.core.management.base import BaseCommand
from django.utils import timezone


FIRST_NAMES = ['Алексей', 'Мария', 'Дмитрий', 'Анна', 'Иван', 'Елена', 'Сергей', 'Ольга',
               'Михаил', 'Наталья', 'Андрей', 'Татьяна', 'Павел', 'Юлия', 'Николай', 'Ирина',
               'Артём', 'Виктория', 'Владимир', 'Светлана', 'Кирилл', 'Екатерина', 'Роман', 'Дарья']
LAST_NAMES  = ['Иванов', 'Петров', 'Сидоров', 'Козлов', 'Новиков', 'Морозов', 'Волков',
               'Попов', 'Лебедев', 'Соколов', 'Смирнов', 'Зайцев', 'Павлов', 'Семёнов',
               'Голубев', 'Виноградов', 'Богданов', 'Кузнецов', 'Медведев', 'Федоров']
SCHOOLS     = ['МБОУ Гимназия №1', 'МБОУ СОШ №15', 'МБОУ Лицей №7', 'МБОУ СОШ №42',
               'МБОУ Гимназия №3', 'МБОУ СОШ №8', 'МБОУ Лицей №12', 'МБОУ СОШ №25']

EVENTS_DATA = [
    {
        'title': 'Олимпиада по финансовой грамотности 2024',
        'event_type': 'olympiad', 'status': 'completed',
        'start': date(2024, 3, 1), 'end': date(2024, 4, 30),
        'deadline': date(2024, 3, 20),
    },
    {
        'title': 'Конкурс «Молодой инвестор» 2024',
        'event_type': 'competition', 'status': 'completed',
        'start': date(2024, 9, 1), 'end': date(2024, 11, 30),
        'deadline': date(2024, 9, 25),
    },
    {
        'title': 'Олимпиада по финансовой грамотности 2025',
        'event_type': 'olympiad', 'status': 'active',
        'start': date(2025, 3, 1), 'end': date(2025, 5, 15),
        'deadline': date(2025, 4, 1),
    },
    {
        'title': 'Конкурс «Финансовый старт» 2025',
        'event_type': 'competition', 'status': 'active',
        'start': date(2025, 2, 10), 'end': date(2025, 4, 30),
        'deadline': date(2025, 3, 15),
    },
    {
        'title': 'Олимпиада «Бюджет и экономика» 2025',
        'event_type': 'olympiad', 'status': 'completed',
        'start': date(2025, 1, 15), 'end': date(2025, 2, 28),
        'deadline': date(2025, 1, 30),
    },
    {
        'title': 'Конкурс «Молодой инвестор» 2025',
        'event_type': 'competition', 'status': 'upcoming',
        'start': date(2025, 9, 1), 'end': date(2025, 11, 30),
        'deadline': date(2025, 9, 20),
    },
]

# Количество участников и работ на каждое мероприятие
EVENT_LOAD = [
    {'participants': 18, 'submit_pct': 0.78, 'eval_pct': 1.0},   # все проверены
    {'participants': 24, 'submit_pct': 0.70, 'eval_pct': 0.90},
    {'participants': 30, 'submit_pct': 0.60, 'eval_pct': 0.50},   # текущее — часть проверена
    {'participants': 20, 'submit_pct': 0.65, 'eval_pct': 0.40},
    {'participants': 15, 'submit_pct': 0.80, 'eval_pct': 1.0},
    {'participants': 5,  'submit_pct': 0.20, 'eval_pct': 0.0},    # предстоящее
]

SCORE_DISTRIBUTION = [
    # (вес, диапазон баллов) — реалистичное нормальное распределение
    (5,  (82, 98)),
    (20, (65, 82)),
    (40, (45, 65)),
    (25, (28, 45)),
    (10, (10, 28)),
]

def random_score():
    bucket = random.choices(SCORE_DISTRIBUTION, weights=[w for w, _ in SCORE_DISTRIBUTION])[0]
    return random.randint(*bucket[1])

def random_date_in_range(start: date, end: date) -> date:
    delta = (end - start).days
    if delta <= 0:
        return start
    return start + timedelta(days=random.randint(0, delta))


class Command(BaseCommand):
    help = 'Создаёт тестовые данные для аналитики'

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model
        from apps.events.models import Event, EventRegistration, JuryAssignment, EventStage, EventTask
        from apps.submissions.models import Submission, Evaluation
        from apps.notifications.models import Notification

        User = get_user_model()

        # ── Базовые пользователи ──────────────────────────────────────────────
        self.stdout.write('Создание базовых пользователей...')

        admin, _ = User.objects.get_or_create(email='admin@finansy.ru', defaults={
            'first_name': 'Иван', 'last_name': 'Петров',
            'role': 'admin', 'is_staff': True, 'is_superuser': True,
        })
        admin.set_password('admin123'); admin.save()

        teacher, _ = User.objects.get_or_create(email='teacher@finansy.ru', defaults={
            'first_name': 'Мария', 'last_name': 'Сидорова', 'role': 'teacher',
            'institution': 'МБОУ Гимназия №1', 'grade_or_position': 'Учитель экономики',
        })
        teacher.set_password('teacher123'); teacher.save()

        jury_user, _ = User.objects.get_or_create(email='jury@finansy.ru', defaults={
            'first_name': 'Елена', 'last_name': 'Козлова', 'role': 'jury',
            'institution': 'НИУ ВШЭ', 'grade_or_position': 'Доцент кафедры финансов',
        })
        jury_user.set_password('jury123'); jury_user.save()

        # ── Участники ─────────────────────────────────────────────────────────
        self.stdout.write('Создание участников...')
        participants = []
        # Сначала основной тестовый участник
        p0, _ = User.objects.get_or_create(email='student@finansy.ru', defaults={
            'first_name': 'Алексей', 'last_name': 'Иванов', 'role': 'participant',
            'institution': 'МБОУ Гимназия №1', 'grade_or_position': '10А',
            'teacher': teacher, 'status': 'active',
        })
        p0.set_password('student123'); p0.save()
        participants.append(p0)

        for i in range(49):
            fn = random.choice(FIRST_NAMES)
            ln = random.choice(LAST_NAMES)
            email = f'student{i+1}@finansy.ru'
            p, _ = User.objects.get_or_create(email=email, defaults={
                'first_name': fn, 'last_name': ln, 'role': 'participant',
                'institution': random.choice(SCHOOLS),
                'grade_or_position': f'{random.randint(8,11)}{"АБВГ"[i%4]}',
                'teacher': teacher if i % 3 == 0 else None,
                'status': 'active',
            })
            participants.append(p)

        self.stdout.write(f'  Участников: {len(participants)}')

        # ── Мероприятия ───────────────────────────────────────────────────────
        self.stdout.write('Создание мероприятий...')
        events = []
        for edata in EVENTS_DATA:
            ev, created = Event.objects.get_or_create(
                title=edata['title'],
                defaults={
                    'description': f'Описание: {edata["title"]}',
                    'short_description': edata['title'],
                    'event_type': edata['event_type'],
                    'movement_type': 'olympiad_movement',
                    'status': edata['status'],
                    'format': 'online',
                    'start_date': edata['start'],
                    'end_date': edata['end'],
                    'registration_deadline': edata['deadline'],
                    'created_by': admin,
                },
            )
            events.append(ev)
            if created:
                # Добавляем этапы
                s1 = EventStage.objects.create(
                    event=ev, order=1, title='Отборочный этап',
                    start_date=edata['start'], end_date=edata['start'] + timedelta(days=20),
                )
                s2 = EventStage.objects.create(
                    event=ev, order=2, title='Финальный этап',
                    start_date=edata['start'] + timedelta(days=21), end_date=edata['end'],
                )
                EventTask.objects.create(stage=s1, order=1, title='Теоретическое задание', max_score=50,
                    description='Ответьте на вопросы по финансовой грамотности.')
                EventTask.objects.create(stage=s1, order=2, title='Решение задач', max_score=50,
                    description='Решите практические задачи по личным финансам.')
                EventTask.objects.create(stage=s2, order=1, title='Проектная работа', max_score=100,
                    description='Подготовьте и защитите проектную работу.')

            # Назначаем жюри
            JuryAssignment.objects.get_or_create(jury=jury_user, event=ev)

        self.stdout.write(f'  Мероприятий: {len(events)}')

        # ── Регистрации, работы и оценки ─────────────────────────────────────
        self.stdout.write('Создание регистраций, работ и оценок...')
        submissions_created = 0
        evaluations_created = 0

        for ev_idx, (ev, load) in enumerate(zip(events, EVENT_LOAD)):
            pool = random.sample(participants, min(load['participants'], len(participants)))
            n_submit = int(len(pool) * load['submit_pct'])

            # Даты подачи — равномерно в окне мероприятия
            sub_window_start = ev.start_date
            sub_window_end   = min(ev.end_date, date.today())
            if sub_window_end <= sub_window_start:
                sub_window_end = sub_window_start + timedelta(days=1)

            for p_idx, p in enumerate(pool):
                # Регистрация
                EventRegistration.objects.get_or_create(
                    event=ev, participant=p,
                    defaults={'status': 'active' if ev.status in ('active', 'upcoming') else 'completed',
                              'completion_percentage': random.randint(20, 100)},
                )

                if p_idx >= n_submit:
                    continue  # без работы

                # Уже есть работа?
                if Submission.objects.filter(event=ev, participant=p).exists():
                    sub = Submission.objects.get(event=ev, participant=p)
                else:
                    sub_date = random_date_in_range(sub_window_start, sub_window_end)
                    sub_dt = timezone.make_aware(
                        datetime.combine(sub_date, datetime.min.time().replace(
                            hour=random.randint(8, 20), minute=random.randint(0, 59)
                        ))
                    )
                    sub = Submission.objects.create(
                        event=ev, participant=p,
                        file='submissions/test_work.pdf',
                        original_filename='work.pdf',
                        file_size=random.randint(100_000, 5_000_000),
                        status='submitted',
                        submitted_at=sub_dt,
                        jury=jury_user,
                    )
                    submissions_created += 1

                # Оценка
                n_eval = int(n_submit * load['eval_pct'])
                if p_idx < n_eval and not hasattr(sub, '_eval_done'):
                    if not Evaluation.objects.filter(submission=sub).exists():
                        score = random_score()
                        Evaluation.objects.create(
                            submission=sub,
                            jury=jury_user,
                            score=score,
                            feedback=self._feedback(score),
                            is_draft=False,
                            criteria_completeness=score >= 60,
                            criteria_accuracy=score >= 50,
                            criteria_examples=score >= 55,
                            criteria_grammar=score >= 40,
                        )
                        sub.status = 'evaluated'
                        sub.save(update_fields=['status'])
                        evaluations_created += 1

        self.stdout.write(f'  Работ создано:  {submissions_created}')
        self.stdout.write(f'  Оценок создано: {evaluations_created}')

        self.stdout.write(self.style.SUCCESS('\nТестовые данные для аналитики созданы!\n'))
        self.stdout.write('Учётные данные:')
        self.stdout.write('  Администратор: admin@finansy.ru     / admin123')
        self.stdout.write('  Педагог:       teacher@finansy.ru  / teacher123')
        self.stdout.write('  Участник:      student@finansy.ru  / student123')
        self.stdout.write('  Жюри:          jury@finansy.ru     / jury123')

    def _feedback(self, score):
        if score >= 80:
            return 'Отличная работа! Тема раскрыта полно, выводы обоснованы, примеры актуальны.'
        if score >= 60:
            return 'Хорошая работа. Основная идея понятна, но некоторые тезисы требуют доработки.'
        if score >= 40:
            return 'Удовлетворительно. Работа выполнена, однако содержит фактические неточности.'
        return 'Работа требует существенной доработки. Тема раскрыта недостаточно.'
