from django.db import models
from django.contrib.auth.models import User

class Hobby(models.Model):
    hobby_name = models.TextField(max_length = 200, )

    def __str__(self):
        return self.hobby_name

class Profile(models.Model):
    profile_picture = models.ImageField(upload_to='media', blank=True)
    description = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.description

class Member(User):

    Gender_Choice = (
    ('M', 'Male'),
    ('F', 'Female'),
    )

    gender = models.CharField(max_length=1, choices = Gender_Choice)
    dob = models.DateField()
    profile = models.OneToOneField(to=Profile, blank=False,null = True, on_delete=models.CASCADE)
    hobbies = models.ManyToManyField(to=Hobby,blank=False)
    # def __str__(self):
    #     return self.dob
