from django.contrib import admin
from .models import Todo

class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'desc', 'imp', 'user', 'created_time', 'completed_time')
    readonly_fields = ('created_time',)

# Register your models here.
admin.site.register(Todo, TodoAdmin)
