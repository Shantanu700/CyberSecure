# Generated by Django 5.0 on 2024-10-21 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NeuraSecure_app', '0002_data_info'),
    ]

    operations = [
        migrations.AddField(
            model_name='data',
            name='comment',
            field=models.CharField(default=None, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='data',
            name='is_liked',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='data',
            name='num_likes',
            field=models.CharField(default=None, max_length=5),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Data_info',
        ),
    ]
