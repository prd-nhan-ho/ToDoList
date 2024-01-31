# Generated by Django 4.0.10 on 2024-01-30 03:51

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='displayName',
        ),
        migrations.AddField(
            model_name='user',
            name='display_name',
            field=models.CharField(default='', max_length=30, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=30, unique=True, validators=[django.core.validators.MinLengthValidator(6)]),
        ),
        migrations.CreateModel(
            name='TodoList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(6)])),
                ('description', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(6)])),
                ('created_at', models.DateField(auto_now_add=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.user')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(6)])),
                ('description', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(6)])),
                ('due_date', models.DateField()),
                ('status', models.BooleanField(default=False)),
                ('todo_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.todolist')),
            ],
        ),
    ]
