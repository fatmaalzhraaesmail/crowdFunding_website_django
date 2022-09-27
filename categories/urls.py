from django.urls import path
from categories.views import CategoryView, categories_index,category_show
from . import views
from django.contrib import admin

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
        path("index/",views.categories_index,name="categories_index"),
        path("<int:id>",views.category_show,name="category_show"),
        path("create/",views.create_category,name="create_category"),
        path("edit/<int:id>",views.edit_category,name="edit_category"),
        path("delete/<int:id>",views.delete_category,name="delete_category"),
        path('category/<str:cats>/', CategoryView, name='category'),


  
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)