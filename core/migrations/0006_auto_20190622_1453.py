# Generated by Django 2.2.1 on 2019-06-22 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_request'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='category',
            field=models.CharField(choices=[('NEWORD', 'NEWORDER')], default='NEWORD', max_length=7),
        ),
    ]
