from django.contrib import admin

# Register your models here.
from app.models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'job_type', 'description']
    fields = ['title', 'job_type', 'description', 'image']
