from django.db import models
from django.contrib.auth.models import User

class StudentUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    Type = models.CharField(max_length=15,default="student")
    
    
    def __str__(self):
        return self.user.username
