# Generated by Django 3.2.12 on 2022-12-28 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainbdd', '0016_user_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
