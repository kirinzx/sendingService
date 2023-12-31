# Generated by Django 4.2.6 on 2023-11-27 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientstuff', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientFilter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=255, null=True)),
                ('mob_operator_code', models.IntegerField(null=True)),
            ],
            options={
                'unique_together': {('tag', 'mob_operator_code')},
            },
        ),
        migrations.CreateModel(
            name='Sending',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('message_text', models.TextField()),
                ('end_date', models.DateTimeField()),
                ('celery_id', models.CharField(max_length=255, null=True)),
                ('client_filter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sending.clientfilter')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now=True)),
                ('send_status', models.SmallIntegerField(choices=[(-1, 'Ошибка'), (0, 'Создано'), (1, 'Доставлено')], default=0)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientstuff.client')),
                ('sending', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sending.sending')),
            ],
        ),
    ]
