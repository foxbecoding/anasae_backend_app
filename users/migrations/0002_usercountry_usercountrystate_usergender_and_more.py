# Generated by Django 4.2.2 on 2023-06-06 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCountry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('code', models.CharField(max_length=10)),
                ('is_active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now_add=True, null=True)),
                ('deleted', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserCountryState',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('code', models.CharField(max_length=10)),
                ('is_active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now_add=True, null=True)),
                ('deleted', models.DateTimeField(null=True)),
                ('user_country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='states', to='users.usercountry')),
            ],
        ),
        migrations.CreateModel(
            name='UserGender',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField()),
                ('is_active', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated', models.DateTimeField(auto_now_add=True, null=True)),
                ('deleted', models.DateTimeField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='usergenderchoice',
            name='gender',
        ),
        migrations.RemoveField(
            model_name='usergenderchoice',
            name='is_active',
        ),
        migrations.AddField(
            model_name='usergenderchoice',
            name='user',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, related_name='gender_choice', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='UserGenderChoiceSelected',
        ),
        migrations.AddField(
            model_name='useraddress',
            name='user_country_state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='addresses', to='users.usercountrystate'),
        ),
        migrations.AddField(
            model_name='usergenderchoice',
            name='user_gender',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='choices', to='users.usergender'),
        ),
    ]
