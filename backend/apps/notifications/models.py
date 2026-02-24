from django.db import models


class Notification(models.Model):
    TYPE_CHOICES = [
        ('registration', 'Регистрация на мероприятие'),
        ('submission', 'Подача работы'),
        ('evaluation', 'Результаты оценки'),
        ('deadline', 'Напоминание о дедлайне'),
        ('assignment', 'Назначение жюри'),
        ('system', 'Системное'),
    ]

    recipient = models.ForeignKey(
        'users.User', on_delete=models.CASCADE,
        related_name='notifications', verbose_name='Получатель'
    )
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    message = models.TextField(verbose_name='Сообщение')
    notif_type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, default='system', verbose_name='Тип'
    )
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} → {self.recipient}'
