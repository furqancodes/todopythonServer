from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Todo
from .serializers import TodoSerializer
from django.http import HttpResponse
from typing_extensions import override

def hello_world(request):
     return HttpResponse("hello worlds")

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.filter(is_deleted=False)
    serializer_class = TodoSerializer

    @override
    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
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

    @action(detail=True, methods=['post'], url_path='update-status')
    def update_status(self, request, pk=None):
        todo = self.get_object()
        new_status = request.data.get('status')

        if new_status is None:
            return Response({'error': 'Status is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            new_status = int(new_status)
        except ValueError:
            return Response({'error': 'Status must be an integer.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_status not in [Todo.NOT_STARTED, Todo.IN_PROGRESS, Todo.COMPLETED]:
            return Response({'error': 'Invalid status value.'}, status=status.HTTP_400_BAD_REQUEST)

        if new_status == Todo.IN_PROGRESS:
            todo.start_date = timezone.now()
            todo.end_date = None
        elif new_status == Todo.COMPLETED:
            if todo.status == Todo.NOT_STARTED:
                todo.start_date = timezone.now()
                todo.end_date = todo.start_date
            else:
                todo.end_date = timezone.now()
        elif new_status == Todo.NOT_STARTED:
            todo.start_date = None
            todo.end_date = None

        todo.status = new_status
        todo.save()

        return Response({'status': 'Task status updated successfully.'}, status=status.HTTP_200_OK)


