from email.policy import default
from django.db import models
from django.shortcuts import render,get_object_or_404,reverse,render,redirect
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField




# Create your models here.
class Category(models.Model):
    category_name=models.CharField(max_length=100)
    description=models.CharField(max_length=1000,default="text")
    image=models.ImageField(upload_to="categories/images",null=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True)
    updated_at=models.DateTimeField(auto_now=True,null=True)
    
    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()
        
    def __str__(self):
        return self.category_name
    
    def get_image_url(self):
        return f"../media/{self.image}"
    
    def get_imageShow_url(self):
        return f"./media/{self.image}"
    
    @classmethod
    def get_all_categories(cls):
        return cls.objects.all()
    
    @classmethod
    def get_category_object(cls,id):
        return get_object_or_404(cls,pk=id)
    
    
    def get_show_url(self):
        return reverse("category_show",args=[self.id])
    
    @classmethod
    def get_index_url(cls):
        return reverse("categories_index")
    
    def get_edit_url(self):
        return reverse("edit_category",args=[self.id])
    
    def get_delete_url(self):
        return reverse("delete_category",args=[self.id])


