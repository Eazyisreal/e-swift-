from django.contrib import admin
from .models import *

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ('title', 'price',  'location')
    search_fields = ('title', 'associated_agent__name') 

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'thumbnail', 'price', 'property_type', 'category', 'location', 'availability')
        }),
        ('Additional Information', {
            'fields': ('living_room', 'dinning' ,'no_of_bedrooms', 'no_of_bathrooms', 'no_of_floors', 'features', 'associated_agent', 'slug')
        }),
    )
    
    prepopulated_fields = {'slug': ('title',)} 
    
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = [ 'associated_property_image']

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    list_display = ('title', 'price',  'location')
    search_fields = ('title', 'status') 

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'thumbnail', 'price', 'category', 'status', 'location')
        }),
        ('Additional Information', {
            'fields': ('no_of_block', 'no_of_flat', 'no_of_floors', 'slug')
        }),
    )
    
    prepopulated_fields = {'slug': ('title',)} 
    
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = [ 'associated_project_image']

    
admin.site.register(Agent)
admin.site.register(Blog)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Project_Review)
admin.site.register(Property_Review)
admin.site.register(InspectionBooking)
admin.site.register(NewsletterSubscription)
admin.site.register(Project,ProjectAdmin)
admin.site.register(Project_Category)
admin.site.register(ProjectImage, ProjectImageAdmin)
admin.site.register(PropertyImage,PropertyImageAdmin)
admin.site.register(ContactMessage)
admin.site.register(Property_Category)