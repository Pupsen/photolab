# Generated by Django 2.1.5 on 2019-01-26 23:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Video', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='name',
        ),
    ]
