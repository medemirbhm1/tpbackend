# Generated by Django 3.2.12 on 2022-12-28 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainbdd', '0014_auto_20221227_1645'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
