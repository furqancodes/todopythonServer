# your_app/tasks.py
from celery import shared_task
from django.utils import timezone
from ..models import Todo

@shared_task
def check_reminders():
    current_time = timezone.now()
    due_todos = Todo.objects.filter(reminder_time__lte=current_time,  is_deleted=False)

    for todo in due_todos:
        print(f"Reminder: '{todo.heading}' task's reminder time has reached.")
        todo.reminder_time = None
        todo.save()
