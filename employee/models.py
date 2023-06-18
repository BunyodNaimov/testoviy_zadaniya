from django.db import models
from django.utils.translation import gettext_lazy as _


class EmployeeDirectory(models.Model):
    class LevelType(models.TextChoices):
        LEADER = 'leader'
        MANAGER = 'manager'
        MARKETING_SPECIALIST = 'marketing_specialist'
        SYSTEM_ADMINISTRATOR = 'system_administrator'
        EMPLOYEE = 'employee'

    first_name = models.CharField(_('First name'), max_length=255)
    last_name = models.CharField(_('Last name'), max_length=255)
    surname = models.CharField(_('Surname'), max_length=255, null=True)
    job_title = models.CharField(max_length=255, choices=LevelType.choices, default=LevelType.EMPLOYEE)
    employment_date = models.DateField(auto_now_add=True)
    salary = models.FloatField()
    image = models.ImageField(null=True, blank=True, upload_to='media/')
    boss = models.ForeignKey(
        'self', on_delete=models.PROTECT, related_name='boss_level', null=True, blank=True
    )

    def __str__(self):
        return f'{self.last_name} {self.first_name}'
