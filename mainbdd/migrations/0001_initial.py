# Generated by Django 4.1.4 on 2022-12-20 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RealEstateAdd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('category', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=100)),
                ('surface', models.FloatField()),
                ('price', models.FloatField()),
                ('pub_date', models.DateField(auto_now_add=True)),
                ('localisation', models.CharField(max_length=300)),
                ('wilaya', models.CharField(max_length=50)),
                ('commune', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frist_ame', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('phone_num', models.CharField(max_length=30)),
                ('favorits', models.ManyToManyField(to='mainbdd.realestateadd')),
            ],
        ),
        migrations.AddField(
            model_name='realestateadd',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainbdd.user'),
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('proposal', models.FloatField()),
                ('offerer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainbdd.user')),
                ('real_estate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainbdd.realestateadd')),
            ],
        ),
    ]
