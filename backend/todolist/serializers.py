from rest_framework import serializers
from django.core.validators import MinLengthValidator
from todolist.models import Task, TodoList

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'description', 'due_date', 'status')

class TodoListSerializer(serializers.ModelSerializer):
    task_list = TaskSerializer(many=True)

    class Meta:
        model = TodoList
        fields = '__all__'
