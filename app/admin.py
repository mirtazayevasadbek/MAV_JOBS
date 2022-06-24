from django.contrib import admin

# Register your models here.
from app.models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['id', 'company_name', 'job_title', 'description']
    fields = ['company_name', 'job_title', 'description', 'image', 'Company_phone_number', 'Company_email',
              'Company_address',
              'Company_contact_person', 'comments', 'tasks', 'salary']
