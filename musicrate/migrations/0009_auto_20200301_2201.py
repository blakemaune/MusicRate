# Generated by Django 2.2.10 on 2020-03-02 04:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('musicrate', '0008_auto_20200301_2200'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='review',
            unique_together={('reviewer', 'album')},
        ),
    ]
