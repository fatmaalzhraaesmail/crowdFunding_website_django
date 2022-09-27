from django.urls import path
from accounts.forms import  EditUserForm
from accounts.views import  ActivateAccount, EditProfilePageView,ProfilePageForm, SignUpView, PasswordsChangeView, ShowProfilePageView, CreateProfilePageView, UserDeleteView, UserEditView,accountProfile
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt




urlpatterns = [
    path('register/', SignUpView.as_view(), name='register'),
    path('profile/<int:pk>/', ProfilePageForm, name='profile'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='registration/login.html'), name='login'),


    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('profile/',accountProfile),
    path('edit_profile/', UserEditView.as_view(), name='edit_profile'),
    path('<int:pk>/edit_profile_page/', EditProfilePageView.as_view(), name='edit_profile_page'),

    # path('password/', auth_views.PasswordChangeView.as_view(template_name='registration/change-password.html')),
    path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html'),name='change-password'),
    path('password_success', views.password_success, name='password_success'),
    path('<int:pk>/profile/', ShowProfilePageView.as_view(), name='show_profile_page'),
    path('<pk>/delete/', UserDeleteView.as_view(),name='delete_account'),


    path('create_profile_page/', CreateProfilePageView.as_view(), name='create_profile_page'),
    
 path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='password-reset/password_reset.html',
             subject_template_name='password-reset/password_reset_subject.txt',
             email_template_name='password-reset/password_reset_email.html',
             success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='password-reset/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='password-reset/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='password-reset/password_reset_complete.html'
         ),
         name='password_reset_complete'),
    

]