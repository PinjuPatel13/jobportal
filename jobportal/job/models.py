from django.db import models
from django.contrib.auth.models import User

class StudentUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True) 
    last_name = models.CharField(max_length=100, null=True, blank=True) 
    mobile = models.CharField(max_length=15, null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    Type = models.CharField(max_length=15,default="student")
    email = models.CharField(max_length=30 , null=True, blank=True)
    
    def __str__(self):
        return self.user.username


class Recruiter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True) 
    last_name = models.CharField(max_length=100, null=True, blank=True) 
    company = models.CharField(max_length=100,null = True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    image = models.FileField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    Type = models.CharField(max_length=15,default="Recruiter")
    status = models.CharField(max_length=15,null=True)
    email = models.CharField(max_length=30 , null=True, blank=True)
    def __str__(self):
        return self.user.username



class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter,on_delete=models.CASCADE)
    start_data = models.DateField()
    End_data = models.DateField()
    job_title = models.CharField(max_length=100)
    job_salary = models.FloatField(max_length=20)
    Image = models.FileField(max_length=100)
    job_description = models.TextField(max_length=300)
    job_location = models.CharField(max_length=100)
    job_experience = models.CharField(max_length=100)
    Skills = models.CharField(max_length=100)
    Creationdata = models.DateField()
    def __str__(self):
        return self.job_title


class Apply(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE)
    student = models.ForeignKey(StudentUser,on_delete=models.CASCADE)
    resume = models.FileField(null = True)
    applydate = models.DateField()
    
    def __str__(self):
        return self.id
    
