# Generated by Django 4.0.4 on 2022-05-20 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('connection', '0003_accountdetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='accountmodel',
            name='account_id',
        ),
    ]