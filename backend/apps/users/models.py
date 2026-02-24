from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('teacher', 'Педагог'),
        ('participant', 'Участник'),
        ('jury', 'Жюри'),
    ]
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('blocked', 'Заблокирован'),
        ('pending', 'Ожидает подтверждения'),
    ]

    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=100, blank=True, verbose_name='Отчество')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')

    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='participant', verbose_name='Роль'
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Статус'
    )

    institution = models.CharField(max_length=255, blank=True, verbose_name='Учреждение')
    grade_or_position = models.CharField(
        max_length=100, blank=True, verbose_name='Класс / Должность'
    )

    # Связь педагог–ученик
    teacher = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='students',
        verbose_name='Педагог',
        limit_choices_to={'role': 'teacher'},
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    last_activity = models.DateTimeField(null=True, blank=True, verbose_name='Последняя активность')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return f'{self.last_name} {self.first_name} ({self.get_role_display()})'

    @property
    def full_name(self):
        parts = [self.last_name, self.first_name]
        if self.patronymic:
            parts.append(self.patronymic)
        return ' '.join(parts)

    @property
    def initials(self):
        result = ''
        if self.first_name:
            result += self.first_name[0].upper()
        if self.last_name:
            result += self.last_name[0].upper()
        return result
