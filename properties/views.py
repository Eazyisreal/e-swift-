from django.shortcuts import render, get_object_or_404
from .models import *
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

def blog(request):
    return render(request, 'blog.html')

def blog_details(request):
    return render(request, 'blog_details.html')

def project(request):
    projects = Project.objects.all().order_by('-id')
    context = {'projects': projects}
    return render(request, 'project.html', context)

def project_details(request, project_slug):
    project = get_object_or_404(Project,slug=project_slug)
    images = project.projectimage_set.all()
    context = {'project': project, 'images': images}
    return render(request, 'project_details.html', context)

def properties(request):
    return render(request, 'properties.html')

def properties_details(request):
    return render(request, 'properties_details.html')

def contact(request):
    return render(request, 'contact.html')

