from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about', views.about, name='about'),
    path('blog', views.blog, name='blog'),
    path('project', views.project, name='project'),
    path('properties', views.properties, name='properties'),
]