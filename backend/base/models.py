from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User

# Create your models here.

class TodoList(models.Model):
    title = models.CharField(max_length=30, validators=[MinLengthValidator(6)])
    description = models.CharField(max_length=30, validators=[MinLengthValidator(6)])
    created_at = models.DateField(auto_now_add=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class Task(models.Model):
    title = models.CharField(max_length=30, validators=[MinLengthValidator(6)])
    description = models.CharField(max_length=30, validators=[MinLengthValidator(6)])
    due_date = models.DateField()
    status = models.BooleanField(default=False)  # Adjust default value if needed
    todo_list = models.ForeignKey(TodoList, on_delete=models.CASCADE)





