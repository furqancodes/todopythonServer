from django.db import models
# Create your models here.
class Todo(models.Model):
    NOT_STARTED = 1
    IN_PROGRESS = 2
    COMPLETED = 3

    STATUS_CHOICES = [
        (NOT_STARTED, 'Not Started'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    ]

    heading = models.CharField(max_length=255)
    description = models.TextField(null=True)
    reminder_time = models.DateTimeField(null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=NOT_STARTED)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)