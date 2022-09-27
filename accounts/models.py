from django.db import models
from email.policy import default
from django.db import models
from django.shortcuts import render,get_object_or_404,reverse,render,redirect
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField

class Profile(models.Model):
    user = models.OneToOneField(User, primary_key=True,on_delete=models.CASCADE)
    job = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="accounts/images/")
    # phone = PhoneNumberField(blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    country = CountryField(null=True,blank=True,)
    birth_date = models.DateField(null=True, blank=True,)


    def __str__(self):
        return f'{self.user} {self.user.id}'

    def get_absolute_url(self):
        return reverse('projects_index')

    def get_image_url(self):
        return f"../media/{self.profile_pic}"          
