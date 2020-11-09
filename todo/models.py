from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Todo(models.Model):
    task = models.CharField(max_length=100)
    desc = models.TextField(blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    completed_time = models.DateTimeField(null=True, blank=True)
    imp = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    # show_priority = models.IntegerField()

    def __str__(self):
        return self.task
    