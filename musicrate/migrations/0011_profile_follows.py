# Generated by Django 2.2.10 on 2020-03-05 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicrate', '0010_remove_review_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follows',
            field=models.ManyToManyField(related_name='followed_by', to='musicrate.Profile'),
        ),
    ]
