from django.db import models
import pytz


class Client(models.Model):
    phone_number = models.PositiveBigIntegerField(unique=True, error_messages={
        'unique': 'Данный номер телефона уже зарегистрирован'
    })
    mob_operator_code = models.CharField(max_length=3)
    tag = models.CharField(max_length=255, null=True)
    timezone = models.CharField(max_length=255)

    def __str__(self) -> str:
        return str(self.phone_number)
    
    def clean(self):
        if not (70000000000 <= self.phone_number <= 79999999999):
            raise ValueError(
                'Некорректный формат номера телефона'
            )
        
        if self.mob_operator_code != str(self.phone_number)[1:4]:
            raise ValueError(
                "Код оператора не совпадает с тем, что написан в номере телефона"
            )
        
        if not self.timezone in pytz.all_timezones:
            raise ValueError(
                'Переданный часовой пояс не соответствует ни одному из известных нам. Возможно, вы передали его в неправильном формате? Вот пример: Europe/Moscow'
            )

    def save(self, *args, **kwargs):
        self.clean()
        super(Client, self).save(*args,**kwargs)