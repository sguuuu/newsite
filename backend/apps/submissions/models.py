from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Submission(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('submitted', 'Подана'),
        ('under_review', 'На проверке'),
        ('evaluated', 'Оценена'),
    ]

    event = models.ForeignKey(
        'events.Event', on_delete=models.CASCADE,
        related_name='submissions', verbose_name='Мероприятие'
    )
    stage = models.ForeignKey(
        'events.EventStage', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='submissions', verbose_name='Этап'
    )
    participant = models.ForeignKey(
        'users.User', on_delete=models.CASCADE,
        related_name='submissions', verbose_name='Участник'
    )
    jury = models.ForeignKey(
        'users.User', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='assigned_submissions', verbose_name='Назначенное жюри'
    )

    file = models.FileField(upload_to='submissions/%Y/%m/', verbose_name='Файл работы')
    original_filename = models.CharField(max_length=255, verbose_name='Исходное имя файла')
    file_size = models.PositiveIntegerField(verbose_name='Размер файла (байты)')

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Статус'
    )
    submitted_at = models.DateTimeField(null=True, blank=True, verbose_name='Дата подачи')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'
        unique_together = ['event', 'stage', 'participant']
        ordering = ['-submitted_at']

    def __str__(self):
        return f'Работа {self.participant} на {self.event}'


class Evaluation(models.Model):
    submission = models.OneToOneField(
        Submission, on_delete=models.CASCADE,
        related_name='evaluation', verbose_name='Работа'
    )
    jury = models.ForeignKey(
        'users.User', on_delete=models.CASCADE,
        related_name='evaluations', verbose_name='Жюри'
    )

    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Балл'
    )
    feedback = models.TextField(blank=True, verbose_name='Комментарий жюри')

    # Критерии оценивания
    criteria_completeness = models.BooleanField(default=False, verbose_name='Полнота ответа')
    criteria_accuracy = models.BooleanField(default=False, verbose_name='Точность данных')
    criteria_examples = models.BooleanField(default=False, verbose_name='Примеры и иллюстрации')
    criteria_grammar = models.BooleanField(default=False, verbose_name='Грамотность изложения')

    is_draft = models.BooleanField(default=True, verbose_name='Черновик')
    evaluated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Оценка'
        verbose_name_plural = 'Оценки'

    def __str__(self):
        return f'Оценка {self.score} баллов для {self.submission}'


class EventResult(models.Model):
    PLACE_CHOICES = [
        (1, '1 место'),
        (2, '2 место'),
        (3, '3 место'),
        (0, 'Участник'),
    ]

    event = models.ForeignKey(
        'events.Event', on_delete=models.CASCADE,
        related_name='results', verbose_name='Мероприятие'
    )
    participant = models.ForeignKey(
        'users.User', on_delete=models.CASCADE,
        related_name='results', verbose_name='Участник'
    )
    submission = models.ForeignKey(
        Submission, on_delete=models.CASCADE,
        related_name='result', verbose_name='Работа'
    )

    place = models.PositiveSmallIntegerField(choices=PLACE_CHOICES, verbose_name='Место')
    final_score = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name='Итоговый балл'
    )
    certificate_issued = models.BooleanField(default=False, verbose_name='Сертификат выдан')
    published_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
        unique_together = ['event', 'participant']
        ordering = ['place', '-final_score']

    def __str__(self):
        return f'{self.participant} — {self.place} место на {self.event}'
