from contextlib import nullcontext
from email.policy import default
from operator import truediv
from django.db import models
from categories.models import Category
import datetime
from django.shortcuts import render,get_object_or_404,reverse,render,redirect
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg, Count
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Project(models.Model):
    Title=models.CharField(max_length=100)
    Description=models.CharField(max_length=1000)
    target=models.IntegerField(default=100)
    # image=models.ImageField(upload_to="projects/images",null=True)
    # image2=models.ImageField(upload_to="projects/images",null=True)
    # image3=models.ImageField(upload_to="projects/images",null=True)
    start=models.DateField(default=datetime.date.today)
    end=models.DateField( default=datetime.date.today)
    tags=models.CharField(max_length=100, null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    category=models.ForeignKey(Category,null=True,on_delete=models.CASCADE,related_name='category_projects')
    averagerating=models.FloatField(default=0)
    is_featured=models.BooleanField(default=False)

    
    def get_total(self):
        return (self.target * 25)/100
    
   
           
    def __str__(self):
     return self.Title + ' | ' + str(self.id)+ ' | ' + str(self.owner)
    

    @classmethod
    def get_all_projects(cls):
     return cls.objects.all()  
    @classmethod
    def get_project_object(cls,id):
        return get_object_or_404(cls,pk=id) 

class Image(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='images_project')
    image=models.ImageField(upload_to="projects/images",null=True)

    def __str__(self):
     return self.project.Title 

    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()

    @classmethod
    def get_all_images(cls):
     return cls.objects.all()    
        
    
        
    def get_image_url(self):
        return f"../media/{self.image}"
        
    def get_imageShow_url(self):
        return f"/media/{self.image}"
        



class Comment(models.Model):
    project = models.ForeignKey(Project, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,default="")
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.project.Title, self.name,self.user.username)  

    def total_reports(self):
        return self.report.count()      

class Donation(models.Model):
    quantity = models.IntegerField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='pdonation')
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.project.Title,self.user.username)    

    def get_total1(self):
        return (self.project.target * 25)/100      


class ProjectsReport(models.Model):
    why = models.TextField(max_length=3000)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CommentsReport(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE,related_name='comments_report')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return '%s - %s' % (self.comment.id,self.user.username) 





class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='reviewss')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    rating = models.FloatField(default=0)

    def __str__(self):
        return self.user.username + ' | ' + str(self.project.id)+ ' | ' + str(self.project.Title)


    
    
                   
# class Comment(models.Model):
#     project = models.ForeignKey(Project, related_name="comments", on_delete=models.CASCADE)
#     name = models.CharField(max_length=255)
#     body = models.TextField(null=True)
#     date_added = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return '%s - %s' % (self.project.Title, self.name)    

  







# class Review(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.TextField(max_length=1000)
#     rating = models.FloatField(default=0)

#     def __str__(self):
#         return self.user.username


          