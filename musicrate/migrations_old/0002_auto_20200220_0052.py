# Generated by Django 2.2.10 on 2020-02-20 06:52

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('musicrate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='review',
            name='updated',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
