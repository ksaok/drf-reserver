from django.db import models

# Create your models here.

class Table(models.Model):
    """Столики"""
    number = models.SmallIntegerField('Номер столика', unique=True)
    places = models.SmallIntegerField('Количество мест')

    def __str__(self):
        return f'Столик №{self.number} на {self.places} мест'

    class Meta:
        verbose_name = ('Стол')
        verbose_name_plural = ('Столы')


class Reserve(models.Model):
    """Резервы столиков"""
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='table')
    start_time = models.DateTimeField('Время резерва')
    end_time = models.DateTimeField('Окончание резерва')
    phone = models.CharField('Телефон клиента', max_length=11)

    def __str__(self):
        return f'Cтолик №{self.table.number} для {self.phone} ({self.start_time}-{self.end_time})'

    class Meta:
        verbose_name = ('Резерв столика')
        verbose_name_plural = ('Резервы столиков')
