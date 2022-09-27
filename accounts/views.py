from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView

from projects.models import Donation, Image, Project, Review
from .forms import  EditUserForm, PasswordChangingForm, ProfilePageForm, SignUpForm, ProfilePageForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404,reverse,redirect
from django.views import generic
from django.views.generic import DetailView, CreateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from accounts.models import Profile
from categories.models import Category
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import login, logout
from django.db.models import Avg,Sum
from django.views.generic.edit import DeleteView



from .tokens import account_activation_token

# Sign Up View
class SignUpView(View):
    form_class = SignUpForm
    template_name = 'registration/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False # Deactivate account till it is confirmed
            user.save()
            profile = Profile(user=user)
            profile.save()
            

            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.success(request, ('Please Confirm your email to complete registration.'))

            return redirect('login')

        return render(request, self.template_name, {'form': form})


from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.email_confirmed = True
            user.profile.save()
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('login')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('login')


# # Edit Profile View
# class ProfileView(UpdateView):
#     model = User
#     form_class = ProfileForm
#     success_url = reverse_lazy('home')
#     template_name = 'commons/profile.html'




def log_out(request):
    logout(request)
    return redirect(reverse('accounts/login'))

def accountProfile(request):
    url=reverse("create_profile_page")
    return redirect(url)

class CreateProfilePageView(CreateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = 'registration/create_user_profile_page.html'
    # fields = '__all__'
    def form_valid(self, form):
        form.instance.user= self.request.user

        return super().form_valid(form)

class EditProfilePageView(generic.UpdateView):
    model = Profile
    template_name = 'registration/edit_profile_page.html'
    fields = ['job', 'profile_pic', 'facebook_url', 'twitter_url', 'instagram_url','country','birth_date']
    success_url = reverse_lazy('projects_index')



class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        user = self.request.user


        projects = Project.objects.filter(owner=user)
        reviews = Review.objects.filter(user=user)
        donations=Donation.objects.filter(user=user)
        categories=Category.objects.all()

        images=Image.get_all_images()


        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)

        page_user = get_object_or_404(User, id=self.kwargs['pk'])

        


        context["page_user"] = page_user
        context["projects"]=projects
        context["reviews"]=reviews
        context["donations"]=donations
        # context["pdonation"]=pdonation
        context["categories"]=categories
        # context["average"]=average
        # context["total"]=total
        # context["p"]=p
        # context["s"]=s
        # context["delete_flag"]=p.delete_flag 

        
        return context



class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    # form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')
    # success_url = reverse_lazy('home')

def password_success(request):
    return render(request, 'registration/password_success.html', {})




class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
    form_class = EditUserForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('projects_index')

    def get_object(self):
        return self.request.user


class UserDeleteView(DeleteView):
    model = Profile
     
    success_url =reverse_lazy('projects_index')
     
    template_name = "registration/confirm_delete.html"





















































