from django.contrib import admin

from employee.models import EmployeeDirectory


# admin.site.register(EmployeeDirectory)

@admin.register(EmployeeDirectory)
class EmployeeDirectoryAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'job_title', 'employment_date', 'salary', 'boss', 'image']
