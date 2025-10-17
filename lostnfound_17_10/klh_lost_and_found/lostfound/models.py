from django.db import models
from django.contrib.auth.models import User

class LostFoundItem(models.Model):
    STATUS_CHOICES = (
        ('lost', 'Lost'),
        ('found', 'Found'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='items/', blank=True, null=True)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=5, choices=STATUS_CHOICES)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='items')
    claimed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='claimed_items')
    date_reported = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
