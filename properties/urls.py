from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('blog/', views.blog, name='blog'),
    path('project/', views.project, name='project'),
    path('properties/', views.properties, name='properties'),
    path('contact/', views.contact, name='contact'),
    path('project/<str:project_slug>', views.project_details, name='project_details'),
    path('project/<str:category_name>', views.project_details, name='project_category'),
    path('properties/<str:property_slug>', views.properties_details, name='properties_details'),
    path('blog-details/<slug:slug>/', views.blog_details, name='blog_details'),
]