from django.shortcuts import render
from django.http import HttpResponse
from todoapp.models import Todo
from rest_framework import viewsets
from .models import Todo
from .serializers import TodoSerializer
from rest_framework.response import Response
from rest_framework import status

def hello_world(request):
     return HttpResponse("hello worlds")

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.filter(is_deleted=False)
    serializer_class = TodoSerializer

    def destroy(self):
        instance = self.get_object()
        instance.is_deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

