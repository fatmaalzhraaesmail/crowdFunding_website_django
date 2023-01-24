from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('',views.showAllProjects,name='projects_index'),
    path('create/',views.create_project,name='create_project'),
    path('details/<int:id>/',views.detail,name="show_project"),
    path('project/edit/<int:pk>', views.UpdateProjectView.as_view(), name='edit_project'),
    path('<int:id>/report_project', views.report_project, name = 'report_project'),
    path('<int:id>/report_comment', views.report_comment, name = 'report_comment'),
    # path('report/id', views.report_comment, name='report_comment'),


    path('<int:id>/comment', views.create_comment, name = 'add_comment'),

    # path("<int:id>",views.show_project,name='show_project'),
    path("delete/<int:id>",views.delete_project,name='delete_project'),
    # path("edit/<int:id>",views.edit_project,name='edit_project'),
    # path('project/<int:pk>/comment/', views.AddCommentView.as_view(), name="add_comment"),
    path('<int:id>/donate', views.add_donate, name = 'add_donation'),

    # path('project/<int:pk>/donate/', views.DonationView.as_view(), name="add_donation"),
    path('addrating/<int:id>/',views.add_rating,name="add_rating"),
    path('deleterating/<int:project_id>/<int:review_id>',views.delete_rating,name="delete_rating"),
    path('deletereport/<int:project_id>/<int:report_id>',views.delete_report,name="delete_report"),
    path('delete_comment/<int:project_id>/<int:comment_id>',views.delete_comment,name="delete_comment"),
    path('delete_report_comment/<int:comment_id>/<int:report_id>',views.delete_report_comment,name="delete_report_comment"),
    
    path('search', views.search, name='search')


]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
