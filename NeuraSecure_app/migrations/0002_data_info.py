# Generated by Django 5.0 on 2024-10-21 19:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NeuraSecure_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data_info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_liked', models.BooleanField(default=False)),
                ('num_likes', models.CharField(max_length=5)),
                ('comment', models.CharField(max_length=255)),
                ('data', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='NeuraSecure_app.data')),
            ],
        ),
    ]
