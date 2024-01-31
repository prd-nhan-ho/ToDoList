import json
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from todolist import settings
from todolist.serializers import TodoListSerializer, TaskSerializer
from todolist.models import Task, TodoList
import jwt
from itertools import islice

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getToDoList(request):
    result = request.headers['Authorization'].split(' ')
    decodePayload = jwt.decode(result[1], settings.SECRET_KEY, algorithms=['HS256'])
    userId=decodePayload['user_id']
    user=User.objects.get(id=userId)
    toDoList = TodoList.objects.filter(owner=user)
    serializer = TodoListSerializer(toDoList, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def getToDoListDetail(request, listId):
    result = request.headers['Authorization'].split(' ')
    decodePayload = jwt.decode(result[1], settings.SECRET_KEY, algorithms=['HS256'])
    userId=decodePayload['user_id']
    user=User.objects.get(id=userId)

    toDoList = TodoList.objects.filter(owner=user, id=listId).prefetch_related('task_list').first()

    if not toDoList:
            return Response({"error": "ENTITY_NOT_FOUND"})
    else:
            if request.method == 'GET':
                serializer = TodoListSerializer(toDoList)
                return Response(serializer.data)
            
            if request.method == 'PUT':
                serializer = TodoListSerializer(toDoList, data=request.data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response({"error": "INTERNAL_SERVER_ERROR"}) 
            
            if request.method == 'DELETE':
                count = toDoList.delete()

                if count is not None:
                     return Response({'msg': 'Delete successfully'})
                else:
                     return Response({'error': 'INTERNAL_SERVER_ERROR'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createTodoList(request):
    result = request.headers['Authorization'].split(' ')
    decodePayload = jwt.decode(result[1], settings.SECRET_KEY, algorithms=['HS256'])
    print(decodePayload)
    userId=decodePayload['user_id']
    user=User.objects.get(id=userId)
    toDoList = TodoList.objects.create(title=request.data['title'], description=request.data['description'], owner=user)
    serializer = TodoListSerializer(toDoList, many=False)
    print(serializer)
    return Response(serializer.data)

@api_view(['POST'])
def delete_everything(self):
    TodoList.objects.all().delete()
    return Response('clean')

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def addTasks(request, listId):
    result = request.headers['Authorization'].split(' ')
    decodePayload = jwt.decode(result[1], settings.SECRET_KEY, algorithms=['HS256'])
    userId=decodePayload['user_id']
    user=User.objects.get(id=userId)
    toDoList = TodoList.objects.filter(owner=user, id=listId)
    data = request.data
    batch_size=len(request.data)
    objs = (Task(title=data[i]['title'],
                  description=data[i]['description'],
                  due_date=data[i]['due_date'],
                  status=False,
                  todo_list=toDoList[i]
                  ) for i in range(batch_size))

    if not toDoList:
        return Response({"error": "ENTITY_NOT_FOUND"})
    else:
        while True:
            batch = list(islice(objs, batch_size))
            if not batch:
                break

            Task.objects.bulk_create(batch, batch_size)
        serializer = TodoListSerializer(toDoList, many=True)
        return Response(serializer.data)
    
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def taskHandler(request, taskId):
    result = request.headers['Authorization'].split(' ')
    decodePayload = jwt.decode(result[1], settings.SECRET_KEY, algorithms=['HS256'])
    userId=decodePayload['user_id']
    user=User.objects.get(id=userId)

    task = Task.objects.filter(id=taskId).first()

    if not task:
            return Response({"error": "ENTITY_NOT_FOUND"})
    else:
            if request.method == 'GET':
                serializer = TaskSerializer(task)
                return Response(serializer.data)
            
            if request.method == 'PUT':
                serializer = TaskSerializer(task, data=request.data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    return Response({"error": "INTERNAL_SERVER_ERROR"}) 
            
            if request.method == 'DELETE':
                count = TaskSerializer.delete()

                if count is not None:
                     return Response({'msg': 'Delete successfully'})
                else:
                     return Response({'error': 'INTERNAL_SERVER_ERROR'})