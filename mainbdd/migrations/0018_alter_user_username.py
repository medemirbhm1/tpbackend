# Generated by Django 3.2.12 on 2022-12-29 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainbdd', '0017_alter_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
    ]
