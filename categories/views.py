from unicodedata import category
from django.shortcuts import render,get_object_or_404,reverse,render,redirect
import categories
from categories.models import Category
from projects.models import Project

# Create your views here.
def categories_index(request):
    categories=Category.get_all_categories()
    return render(request,"categories/index.html",context={"categories":categories})
    
def categories_base(request):
    categories=Category.get_all_categories()
    return render(request,"projects/base.html",context={"categories":categories})

def category_show(request,id):
    categories=Category.get_all_categories()

    category=Category.get_category_object(id)
    return render(request,"categories/showCategoryDetails.html",context={"category":category,"categories":categories})
    
def create_category(request):
    categories=Category.get_all_categories()

    if request.POST:
        category=Category()
        category.category_name=request.POST["category_name"]
        category.description=request.POST["description"]
        if request.FILES:
            category.image=request.FILES["image"]
            category.save()

            return redirect(Category.get_index_url())
    return render(request,"categories/createCategory.html",{"categories":categories})

def delete_category(request,id):
    category=Category.get_category_object(id)
    category.delete()
    return redirect(Category.get_index_url())

def edit_category(request,id):
    categories=Category.get_all_categories()

    category=Category.get_category_object(id)
    if request.POST:
        category.category_name=request.POST["category_name"]
        category.description=request.POST["description"]
        if request.FILES:
            category.image=request.FILES["image"]
        category.save()
    return render(request,"categories/edit.html",context={"category":category,"categories":categories})

def CategoryView(request, cats):
    categories=Category.get_all_categories()
    projects = Project.objects.filter(category=cats.replace('-', ' '))
    return render(request, 'categories/categories.html', {'cats':cats.title().replace('-', ' '), 'projects':projects,'categories':categories})
    