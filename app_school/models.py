from django.conf import settings
from django.db import models

from users.models import User

NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название курса')
    photo = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='Превью')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    price = models.PositiveIntegerField(**NULLABLE, verbose_name='Цена')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Владелец')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('title',)


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='Пользователь')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='Курс',
                               related_name='subscriptions')
    subscription = models.BooleanField(default=False, verbose_name='Подписка на обновления')

    def __str__(self):
        return f'{self.user} подписан на курс {self.course}: {self.subscription}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название урока')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    photo = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='Превью')
    link = models.TextField(**NULLABLE, verbose_name='Ссылка на видео')

    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Курс',
                               related_name='lessons')

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Владелец')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('title',)


class Payments(models.Model):
    PAY_CHOICES = (
        ('cash', 'Cash'),
        ('transfer', 'Transfer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='user')
    date_of_payment = models.DateTimeField(auto_now_add=True, **NULLABLE, verbose_name='Дата оплаты')

    paid_course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='Курс',
                                    related_name='course')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, **NULLABLE, verbose_name='Урок',
                                    related_name='lesson')

    payment_amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=50, choices=PAY_CHOICES, verbose_name='Способ оплаты')

    is_paid = models.BooleanField(default=False, verbose_name='Статус оплаты')

    def __str__(self):
        return f'{self.user} ' \
               f'купил {self.paid_course if self.paid_course else self.paid_lesson} ' \
               f'за {self.payment_amount}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('pk',)
