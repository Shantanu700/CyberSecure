# Generated by Django 5.0 on 2024-11-08 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NeuraSecure_app', '0009_alter_comment_post_alter_comment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='date',
            field=models.DateField(max_length=50),
        ),
    ]