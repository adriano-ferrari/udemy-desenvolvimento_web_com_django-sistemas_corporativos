# Generated by Django 4.2.2 on 2024-10-13 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0003_alter_myuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='force_change_password',
            field=models.BooleanField(default=False),
        ),
    ]