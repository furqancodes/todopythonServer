from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Todo
from .serializers import TodoSerializer
from django.http import HttpResponse

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
    
    @action(detail=True, methods=['post'], url_path='set-reminder')
    def set_reminder(self, request, pk=None):
        todo = self.get_object()
        reminder_minutes = request.data.get('reminder_minutes', 0)
        reminder_time = timezone.now() + timezone.timedelta(minutes=reminder_minutes)
        todo.reminder_time = reminder_time
        todo.save()
        return Response({'status': 'reminder set'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='move')
    def move(self, request, pk=None):
        todo = self.get_object()
        if todo.status != Todo.COMPLETED:
            todo.status += 1
            if todo.status == Todo.IN_PROGRESS:
                todo.start_date = timezone.now()
            elif todo.status == Todo.COMPLETED:
                todo.end_date = timezone.now()
            todo.save()
            return Response({'status': 'task moved'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'task already completed'}, status=status.HTTP_400_BAD_REQUEST)


