from django.db import models


NULLABLE = {'null': True, 'blank': True}


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название курса')
    photo = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='Превью')
    description = models.TextField(**NULLABLE, verbose_name='Описание')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название урока')
    description = models.TextField(**NULLABLE, verbose_name='Описание')
    photo = models.ImageField(upload_to='course/', **NULLABLE, verbose_name='Превью')
    link = models.TextField(**NULLABLE, verbose_name='Ссылка на видео')

    course = models.ForeignKey(Course, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Курс')

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
