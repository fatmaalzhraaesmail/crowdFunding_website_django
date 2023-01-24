from functools import total_ordering
from urllib import request
from django.db.models import Avg, Sum, Count
from multiprocessing import context
from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User


from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from accounts.models import Profile
from django.db.models import Q
from django.utils.timezone import now


import categories


from .forms import DonationForm, EditForm, ImageForm, ProjectForm, CommentForm, ReviewForm
from .models import CommentsReport, Image, Project, Comment, ProjectsReport, Review
from projects.models import Project, Donation
from categories.models import Category
from django.views.generic import DetailView, CreateView, UpdateView

# Create your views here.


def showAllProjects(request):
    projects = Project.objects.all()
    latest_projects = Project.objects.filter().order_by('created_at')[:5]
    featured_projects = Project.objects.filter(is_featured=True)

    categories = Category.get_all_categories()
    images = Image.get_all_images()
    # c = Review.objects.values('project').annotate(rates=Count('rating'))
    # c= Review.objects.annotate(rates=Count('project')).values('project', 'rating')

    c = Review.objects.values('project').annotate(rates=Count('rating')).order_by('project')
    p=c

    
   
   
 
   
    
    # for b in c:
    #    p=b[2]
        
       
        

    return render(request, 'projects/projects.html', context={"projects": projects, "categories": categories, "images": images, "latest_projects": latest_projects, "featured_projects": featured_projects,"p":p,})


@login_required()
def create_project(request):
    categories = Category.objects.all()
    if request.method == "POST":

        form = ProjectForm(request.POST)
        files = request.FILES.getlist("image")
        if form.is_valid():
            f = form.save(commit=False)
            f.owner = request.user
            f.save()

            for i in files:
                Image.objects.create(project=f, image=i)
            return redirect(reverse('projects_index'))

        else:
            print(form.errors)

    else:
        form = ProjectForm()
        imageform = ImageForm()

    return render(request, "projects/createProject.html", {"form": form, "imageform": imageform, "categories": categories})


# def edit_project(request,id):
#     project=get_object_or_404(Project,pk=id)
#     if request.POST:
#         project.Title=request.POST['Title']
#         project.Description=request.POST['Description']
#         project.target=request.POST['target']
#         project.start=request.POST['start']
#         project.end=request.POST['end']
#         project.tags=request.POST['tags']
#         category=Category.get_category_object(request.POST["category_id"])
#         project.save()

#         files = request.FILES.getlist("image")

#         for i in files:
#                 Image.objects.create(project=project, image=i)

#         url= reverse("projects_index")

#         return redirect(url)
#     categories=Category.get_all_categories()

#     return render(request,"pages/edit.html",context={'projects':project,"categories":categories})
    # if request.method == "POST":

    #     form = ProjectForm(request.POST,request.FILES,instance=project)
    #     files = request.FILES.getlist("image")
    #     if form.is_valid():
    #         # f = form.save(commit=False)
    #         # f.owner = request.user
    #         form.save()

    #         for i in files:
    #             Image.objects.create(project=form, image=i)
    #         return HttpResponseRedirect("")

    #     form = ProjectForm(instance=project)
    #     imageform = ImageForm()

    # return render(request, "projects/edit.html", {"form": form, "imageform": imageform,"project":project})

class UpdateProjectView(UpdateView):
    model = Project
    form_class = EditForm
    template_name = 'projects/edit.html'
    success_url = reverse_lazy('projects_index')


def detail(request, id):
	projects = Project.objects.get(id=id)
	categories = Category.get_all_categories()
	reviews = Review.objects.filter(project=id)
	donations = Donation.objects.filter(project=id)
	report_project = ProjectsReport.objects.filter(project=id)
	reporters = ProjectsReport.objects.all()

	delete_warnning = ""
	average = reviews.aggregate(Avg("rating"))["rating__avg"]

	high_rate = reviews.aggregate(Count("rating"))["rating__count"]

	if average == None:
		average = 0
	else:
		average = round(average, 2)

	t = (projects.target*25)/100

	total = donations.aggregate(Sum("quantity"))

	for value in total.values():
		if value == None: value = 0
		else: delete_warnning = "Project continue" if value >= t else "Owner can  delete Project .It not 25% of Target"



		s = Review.objects.annotate(rating_num=Count('rating')).order_by('project')
		
		
       

	
	



          
	
	context={
		"projects":projects,
		"reviews":reviews,
		"donations":donations,
		"average":average,
		"total":total,
		"categories":categories,
		"t":t,
		"high_rate":high_rate,
		"delete_warnning":delete_warnning,
		'report_projects':report_project,
		'reporters':reporters,
        'today' : now().date(),
        'sums':s,
        # 'counts':c,
        # 'chow':chow,

	}
	return render(request,'projects/showProjectDetails.html',context)

@login_required	
def delete_project(request,id):
    project=get_object_or_404(Project,pk=id) 
    project.delete()
    
    url= reverse("projects_index")

    return redirect(url) 


def edit_project(request,id):
    project=get_object_or_404(Project,pk=id)
    if request.POST:
        project.Title=request.POST['Title']
        project.Description=request.POST['Description']
        category=Category.get_category_object(request.POST["category_id"])
        project.category=category
        if(request.FILES):
            imagename=request.FILES["image"]
            project.image=imagename       
            print(imagename,type(imagename))
        project.save()
        url= reverse("projects_index")

        return redirect(url)
    
    return render(request,"projects/edit.html")

# class AddCommentView(CreateView):
#     model = Comment
#     form_class = CommentForm
#     template_name = 'projects/showProjectDetails.html'
#     # fields = '__all__'
#     def form_valid(self, commForm):
#         commForm.instance.project_id = self.kwargs['pk']
#         commForm.instance.user =self.request.user
#         return super().form_valid(commForm)

#     success_url = reverse_lazy('projects_index')



def create_comment(request, id):
    project = Project.objects.get(id=id)
    if request.method == 'POST':
        if request.POST['body']:
            comment = Comment()
            comment.body = request.POST['body']
            comment.name = request.POST['name']
            comment.project = project
            comment.user = request.user
            comment.save()
    return redirect("show_project" ,id)


def delete_comment(request,project_id,comment_id):
	if request.user.is_authenticated:
		project = Project.objects.get(id=project_id)
		comment = Comment.objects.get(project=project, id=comment_id)

		if request.user == comment.user:
			comment.delete()
		return redirect("show_project" ,project_id)

	else:
		return redirect("login")
    
def add_donate(request, id):
    project = Project.objects.get(id=id)

    if request.method == 'POST':
        donation = Donation.objects.create(
            quantity=request.POST['quantity'],
            project=project,
            user=request.user
        )
    return redirect("show_project" ,id)
# class DonationView(CreateView):
#    model=Donation
#    form_class=DonationForm
#    template_name= 'projects/addDonation.html'
#    def form_valid(self, form):
#         form.instance.project_id = self.kwargs['pk']
#         form.instance.user =self.request.user
#         return super().form_valid(form)

#    success_url = reverse_lazy('projects_index')



def report_project(request, id):
    if request.method == 'POST':
        report_project = ProjectsReport.objects.create(
            why=request.POST['report'],
            project_id=id,
            user=request.user
        )

    return redirect("show_project" ,id)




def delete_report(request,project_id,report_id):
	if request.user.is_authenticated:
		project = Project.objects.get(id=project_id)
		report = ProjectsReport.objects.get(project=project, id=report_id)

		if request.user == report.user:
			report.delete()
		return redirect("show_project" ,project_id)

	else:
		return redirect("login")

def delete_report_comment(request,comment_id,report_id):
	if request.user.is_authenticated:

		commentt = Comment.objects.get(id=comment_id)
		report = CommentsReport.objects.get(comment=commentt, id=report_id)

		if request.user == report.user:
			report.delete()
		return redirect("show_project" ,id)

	else:
		return redirect("login")

def report_comment(request, id):
       user=request.user
       comment=get_object_or_404(Comment,pk=request.POST["comment_id"])

       if CommentsReport.objects.filter(comment_id=request.POST['comment_id'], user=request.user).count()==0:

        if request.method == 'POST':
            report_com = CommentsReport.objects.create(

                comment_id=request.POST['comment_id'],
                user=request.user
               
            )
            return HttpResponseRedirect(reverse('show_project', args=[str(id)]))
        
      
        else:
             flag="you report this comment before"
             return redirect('show_project',id)







def add_rating(request,id):
	if request.user.is_authenticated:
		project = Project.objects.get(id=id)

		if request.method == "POST":
			form = ReviewForm(request.POST or None)
			if form.is_valid():
				data = form.save(commit=False)
				# data.comment = request.POST["comment"]
				data.rating = request.POST["rating"]
				data.user = request.user
				data.project = project
				data.save()
				return redirect("show_project",id)
		else:
			form = ReviewForm()

		return render(request,'projects/showProjectDetails.html',{'form':form})

	else:
		return redirect("login")


def delete_rating(request,project_id,review_id):
	if request.user.is_authenticated:
		project = Project.objects.get(id=project_id)
		review = Review.objects.get(project=project, id=review_id)
		if request.user == review.user:
			review.delete()
		return redirect("show_project",project_id)
	else:
		return redirect("login")

def search(request):

    results = []

    if request.method == "GET":

        query = request.GET.get('user-query')

        if query == '':

            query = 'None'

        results = Project.objects.filter(Q(Title__icontains=query) | Q(tags__icontains=query)  )

    return render(request, 'projects/search.html', {'query': query, 'results': results})


















































