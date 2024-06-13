from django.db import models
from users.models import User
from datetime import datetime


class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Waiting for executor'),
        ('in_progress', 'In progress'),
        ('completed', 'Completed'),
    )

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks',
                                 limit_choices_to={'user_type': 'customer'})
    employee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tasks',
                                 limit_choices_to={'user_type': 'employee'})
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    report = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.report:
            raise ValueError('Report cannot be empty')
        if self.status == 'completed' and not self.closed_at:
            self.closed_at = datetime.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.customer.username} - {self.status}'
