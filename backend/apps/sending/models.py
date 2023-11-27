from typing import Any
from django.db import models
from apps.clientstuff.models import Client
from celery.result import AsyncResult
from django.db.models import Q
from config.celery import app as celery_app
from django.utils import timezone

class ClientFilter(models.Model):
    tag = models.CharField(max_length=255, null=True)
    mob_operator_code = models.CharField(max_length=3, null=True)

    class Meta:
        unique_together = [('tag', 'mob_operator_code')]

class Sending(models.Model):
    start_date = models.DateTimeField()
    message_text = models.TextField()
    end_date = models.DateTimeField()
    client_filter = models.ForeignKey(ClientFilter, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.message_text}. Начало: {self.start_date}. Конец: {self.end_date}'

    def start_sending(self):
        Message.objects.filter(sending=self.pk).delete()
        from .tasks import send, stop_sending
        tag = self.client_filter.tag
        mob_operator_code = self.client_filter.mob_operator_code

        q = Q()

        if tag: q &= Q(tag=tag)

        if mob_operator_code: q &= Q(mob_operator_code=mob_operator_code)

        clients = Client.objects.filter(q)

        flagToEta = False

        if self.start_date > timezone.now():
            flagToEta = True
        
        for client in clients:

            if timezone.now() >= self.end_date:
                return

            msg = Message.objects.create(sending=self,client=client)
            args = [msg.pk, client.phone_number, self.message_text]
            if flagToEta:
                task = send.apply_async(
                    args=args,
                    eta=self.start_date
                )

            else:
                task = send.apply_async(
                    args=args
                )

            stop_task = stop_sending.apply_async(
                args=[task.task_id],
                eta=self.end_date
            )

            msg.celery_id = task.task_id
            msg.revoke_celery_id = stop_task.task_id
            msg.save()

    def save(self, *args,**kwargs):
        self.clean()
        super(Sending, self).save(*args, **kwargs)

        self.start_sending()

    def clean(self):

        if self.start_date >= self.end_date:
            raise ValueError(
                'Дата начала не может быть позже даты конца или соответствовать ей'
            )

        if timezone.now() >= self.end_date:
            raise ValueError(
                'Дата конца не может быть раньше настоящего времени или соответствовать ему'
            )

class Message(models.Model):
    class SendStatus(models.IntegerChoices):
        ERROR = -1, "Ошибка"
        CREATED = 0, "Создано"
        SENT = 1, "Доставлено"
    created_date = models.DateTimeField(auto_now=True)
    send_status = models.SmallIntegerField(choices=SendStatus.choices, default=0)
    sending = models.ForeignKey(Sending, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    celery_id = models.CharField(max_length=255,null=True)
    revoke_celery_id = models.CharField(max_length=255,null=True)

    def __str__(self) -> str:
        return f'Рассылка: {self.sending.pk}. Клиент: {self.client}'
    
    class Meta:
        unique_together = [('sending','client')]

    def delete(self, using: Any = ..., keep_parents: bool = ...) -> tuple[int, dict[str, int]]:
        if self.celery_id:
            task = AsyncResult(self.celery_id)

            if not task.ready():
                celery_app.control.revoke(self.celery_id, terminate=True)

        if self.revoke_celery_id:
            task = AsyncResult(self.revoke_celery_id)

            if not task.ready():
                celery_app.control.revoke(self.revoke_celery_id, terminate=True)

        return super().delete(using, keep_parents)