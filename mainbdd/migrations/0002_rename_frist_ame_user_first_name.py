# Generated by Django 4.1.4 on 2022-12-20 23:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainbdd', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='frist_ame',
            new_name='first_name',
        ),
    ]
