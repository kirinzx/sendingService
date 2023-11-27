from celery import shared_task
from celery.result import AsyncResult
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import requests
from .models import Sending, Message
from config.celery import app as celery_app
from django.db.models import F, Case, When, Value, Sum, Count
from django.db.models.functions import Coalesce
from django.utils import timezone
from decouple import config
import json

@shared_task
def send(msgId, phone, text):
    jwt = config('JWT_API')
    connect_timeout, read_timeout = 5.0, 30.0
    response = requests.post(
        f'https://probe.fbrq.cloud/v1/send/{msgId}',
        timeout=(connect_timeout, read_timeout),
        headers={
            'Authorization':f'Bearer {jwt}'
        },
        json={
            'id': msgId,
            'phone': phone,
            'text': text
        }
    )

    if 200 <= response.status_code < 300:
        Message.objects.filter(id=msgId).update(send_status=Message.SendStatus.SENT)

    else:
        Message.objects.filter(id=msgId).update(send_status=Message.SendStatus.ERROR)

@shared_task
def stop_sending(task_id):
    res = AsyncResult(task_id)

    if not res.ready():
        celery_app.control.revoke(task_id, terminate=True)

@shared_task
def send_info_to_email():
    now_time = timezone.now().strftime("%Y-%m-%d")
    message = render_to_string('email.html',
            {
                'now_time': now_time,
            }
        )
    email = EmailMessage('Статистика по рассылкам',message, from_email='semen.vrazhkin@yandex.ru',to=[config('EMAIL_TO_GET_STATS')])

    data = Message.objects.select_related('sending').values('sending').annotate(
                total_messages=Count('sending'),
                sent=Coalesce(Sum(Case(When(send_status=Message.SendStatus.SENT, then=1))), Value(0)),
                error=Coalesce(Sum(Case(When(send_status=Message.SendStatus.ERROR, then=1))), Value(0)),
                created=Coalesce(Sum(Case(When(send_status=Message.SendStatus.CREATED, then=1))), Value(0))
            ).values('sending','total_messages','sent','error','created',message_text=F('sending__message_text'))

    email.attach(f'stat_{now_time}.json', json.dumps(list(data), ensure_ascii=False).encode('utf-8'), 'application/json')
    email.send()