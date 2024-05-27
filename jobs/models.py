from django.db import models
from django.contrib.auth.models import User
class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class JobApplication(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"