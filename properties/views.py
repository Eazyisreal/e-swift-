from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')

def blog(request):
    return render(request, 'blog.html')

def project(request):
    return render(request, 'project.html')

def properties(request):
    return render(request, 'properties.html')