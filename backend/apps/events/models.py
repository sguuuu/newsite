from django.db import models
from django.utils import timezone


class Event(models.Model):
    TYPE_CHOICES = [
        ('olympiad', 'Олимпиада'),
        ('competition', 'Конкурс'),
    ]
    MOVEMENT_CHOICES = [
        ('olympiad_movement', 'Подготовительно-олимпиадное движение'),
        ('career_guidance', 'Профориентационное движение'),
    ]
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('upcoming', 'Предстоящее'),
        ('active', 'Активное'),
        ('completed', 'Завершённое'),
        ('cancelled', 'Отменено'),
    ]
    FORMAT_CHOICES = [
        ('online', 'Онлайн'),
        ('offline', 'Очно'),
        ('hybrid', 'Смешанный'),
    ]

    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    short_description = models.CharField(max_length=500, blank=True, verbose_name='Краткое описание')

    event_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Тип')
    movement_type = models.CharField(
        max_length=30, choices=MOVEMENT_CHOICES,
        default='olympiad_movement', verbose_name='Направление движения'
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Статус'
    )
    format = models.CharField(
        max_length=20, choices=FORMAT_CHOICES, default='online', verbose_name='Формат'
    )

    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    registration_deadline = models.DateField(verbose_name='Дедлайн регистрации')

    max_participants = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='Макс. участников'
    )
    age_min = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Мин. возраст')
    age_max = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Макс. возраст')

    created_by = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='created_events',
        verbose_name='Создал',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    @property
    def is_registration_open(self):
        today = timezone.now().date()
        return self.status in ('upcoming', 'active') and today <= self.registration_deadline

    @property
    def participant_count(self):
        return self.registrations.filter(
            status__in=('registered', 'active', 'completed')
        ).count()


class EventRegistration(models.Model):
    STATUS_CHOICES = [
        ('registered', 'Зарегистрирован'),
        ('active', 'Участвует'),
        ('completed', 'Завершил'),
        ('withdrawn', 'Отказался'),
    ]

    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='registrations',
        verbose_name='Мероприятие'
    )
    participant = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name='registrations',
        verbose_name='Участник'
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='registered', verbose_name='Статус'
    )
    registered_at = models.DateTimeField(auto_now_add=True)
    completion_percentage = models.PositiveSmallIntegerField(
        default=0, verbose_name='Прогресс (%)'
    )

    class Meta:
        verbose_name = 'Регистрация'
        verbose_name_plural = 'Регистрации'
        unique_together = ['event', 'participant']
        ordering = ['-registered_at']

    def __str__(self):
        return f'{self.participant} → {self.event}'


class JuryAssignment(models.Model):
    jury = models.ForeignKey(
        'users.User', on_delete=models.CASCADE,
        related_name='jury_assignments', verbose_name='Жюри',
        limit_choices_to={'role': 'jury'},
    )
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE,
        related_name='jury_assignments', verbose_name='Мероприятие'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Назначение жюри'
        verbose_name_plural = 'Назначения жюри'
        unique_together = ['jury', 'event']

    def __str__(self):
        return f'Жюри {self.jury} → {self.event}'
