from django.db import models


class Document(models.Model):
    TYPE_CHOICES = [
        ('regulation', 'Положение'),
        ('privacy', 'Политика конфиденциальности'),
        ('methodology', 'Методические материалы'),
        ('template', 'Шаблон работы'),
        ('criteria', 'Критерии оценивания'),
        ('other', 'Прочее'),
    ]

    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    file = models.FileField(upload_to='documents/', verbose_name='Файл')
    original_filename = models.CharField(max_length=255, verbose_name='Исходное имя файла')
    file_size = models.PositiveIntegerField(verbose_name='Размер (байты)')

    doc_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Тип')

    # Опционально: привязка к мероприятию
    event = models.ForeignKey(
        'events.Event', null=True, blank=True, on_delete=models.SET_NULL,
        related_name='documents', verbose_name='Мероприятие'
    )

    uploaded_by = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, verbose_name='Загрузил'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    download_count = models.PositiveIntegerField(default=0, verbose_name='Скачиваний')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title

    @property
    def file_size_display(self):
        size = self.file_size
        if size < 1024:
            return f'{size} Б'
        elif size < 1024 ** 2:
            return f'{size / 1024:.1f} КБ'
        return f'{size / 1024 ** 2:.1f} МБ'
