from contextvars import Context
from multiprocessing import context
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from project1.forms import ProjectForm
from .models import Project,Review,Tag
from .forms import ProjectForm, ReviewForm
from .utils import searchProjects, paginateProjects

List=[
    {
        'id': '1',
        'type': 'two wheeler',
        'name':'tvs'
    },
    {
        'id':'2',
        'type':'four wheeler',
        'name': 'nexon'
    },
    {
        'id':'3',
        'type':'heavy vehicle',
        'name':'ashokleyland'
    }
]

def project2(request):
    
    projects = searchProjects(request)

    page_projects, custom_range = paginateProjects(request,projects,3)
    
    
    Context = {

        'projects' : page_projects,
        'custom_range': custom_range,
    }
    

    return render(request,'project1/project1.html',Context)

def project3(request,pk):
    proj_obj= Project.objects.get(id=pk)

    tags = proj_obj.tags.all()

    reviews = proj_obj.review_set.all()

    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = proj_obj
            review.owner = request.user.profile
            review.save()

            proj_obj.getVoteCount

            messages.success(request,'your review was submitted successfully')
            return redirect('project1:project3', pk=proj_obj.id)
        else:
            messages.error(request,'Some error Occured')    

    context={'pro': proj_obj, 'tags':tags, 'reviews':reviews, 'form':form,
    
    }
    return render(request,'project1/project2.html',context)

@login_required(login_url='users:login')
def createproject(request):
    profile = request.user.profile

    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST,request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('users:account')

    context = { 'form' : form, }
    return render(request, 'project1/project-form.html', context)

@login_required(login_url='users:login')
def updateproject(request,pk):
    profile = request.user.profile
    projobject = profile.project_set.get(id=pk)
    form = ProjectForm(instance=projobject)

    if request.method == 'POST':
        form = ProjectForm(request.POST,instance=projobject)
        if form.is_valid():
            form.save()
            messages.success(request,'project updated successfully')
            return redirect('users:account')

    context = { 'form' : form, }
    return render(request, 'project1/project-form.html', context)

@login_required(login_url='users:login')
def deleteproject(request,pk):
    profile = request.user.profile

    projobject=profile.project_set.get(id=pk)

    if request.method == 'POST':
        projobject.delete()
        messages.success(request,'project deleted successfully')
        return redirect('users:account')

    context = {'object':projobject}
    return render(request, 'delete-template.html', context)                 

# Create your views here.
