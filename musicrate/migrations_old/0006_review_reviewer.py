# Generated by Django 2.2.10 on 2020-03-02 03:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musicrate', '0005_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='reviewer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='musicrate.Profile'),
            preserve_default=False,
        ),
    ]
