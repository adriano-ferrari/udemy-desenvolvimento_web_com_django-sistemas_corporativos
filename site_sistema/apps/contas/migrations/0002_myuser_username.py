# Generated by Django 4.2.2 on 2024-10-13 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='username',
            field=models.CharField(blank=True, max_length=100, unique=True),
        ),
    ]