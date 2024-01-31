"""todolist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from todolist import views

router = routers.DefaultRouter()

urlpatterns = [
    path('auth/', include('user.urls')),
    path('to-do-list/', views.createTodoList, name="createToDoList"),
    path('to-do-list/<str:listId>/', views.getToDoListDetail, name="getToDoListDetail"),
    path('to-do-list/<str:listId>/tasks', views.addTasks, name="addTasks"),
    path('to-do-lists/', views.getToDoList, name="createToDoList"),
    path('clean-to-do/', views.delete_everything, name="cleanToDo"),
    path('task/', views.createTodoList, name="createToDoList"),
    path('task/<str:taskId>/', views.taskHandler, name="taskHandler"),
]

urlpatterns += router.urls