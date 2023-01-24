from django.contrib import admin
from . models import Image, Project
from . models import Category
# from accounts.models import Profile
# Register your models here.
# admin.site.register(Project)
admin.site.register(Category)




class PhotoAdmin(admin.StackedInline):
    model = Image


class ProjectFilter(admin.ModelAdmin):
    inlines = [PhotoAdmin]

    class Meta:
        model = Project 
    list_display=[ "id","Title",
    "Description",
    "target",
    "start",
    "end",
    "tags",
    "created_at",
    "is_featured"]
    list_filter= ["is_featured"]



admin.site.register(Image)
admin.site.register(Project,ProjectFilter)



