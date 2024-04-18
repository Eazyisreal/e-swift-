from django.db import models
from authentication.models import CustomUser
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from .utils.image_utils import save_resized_image



class Project_Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Project Categories'

    def __str__(self):
        return self.name


class Property_Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Property Categories'

    def __str__(self):
        return self.name


class Agent(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    email = models.EmailField(max_length=255)
    image = models.ImageField(upload_to='project_images/', null=True, blank=True,    validators=[
        FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'svg', 'avif'])
    ])
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        save_resized_image(self.image)

class Project(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.IntegerField()
    status = models.CharField(max_length=100)
    category = models.ForeignKey(Project_Category,  on_delete=models.CASCADE)
    no_of_block = models.IntegerField()
    no_of_flat = models.IntegerField()
    no_of_floors = models.IntegerField()
    thumbnail = models.ImageField(upload_to='project_images/', null=True, blank=True,    validators=[
        FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'svg', 'avif'])
    ])
    date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else "Untitled Property Listing"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        save_resized_image(self.thumbnail)

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class Property(models.Model):
    AVAILABILITY_CHOICES = [
        ('Selling', 'Selling'),
        ( 'Rent', 'Rent'),
    ]
    availability = models.CharField(max_length=12, choices=AVAILABILITY_CHOICES)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    property_type = models.CharField(max_length=100)
    category = models.ForeignKey(Property_Category,  on_delete=models.CASCADE)
    price = models.IntegerField()
    living_room = models.IntegerField()
    dinning = models.IntegerField()
    no_of_bedrooms = models.IntegerField()
    no_of_bathrooms = models.IntegerField()
    no_of_floors = models.IntegerField()
    thumbnail = models.ImageField(
        upload_to='property_images/', null=True, blank=True,   validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'svg', 'avif'])
        ])
    date = models.DateTimeField(auto_now_add=True)
    features = models.CharField(max_length=255)
    associated_agent = models.ManyToManyField(Agent)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else "Untitled Property Listing"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        save_resized_image(self.thumbnail)
        
       

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Property"
        verbose_name_plural = "Properties"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    associated_property_image = models.ImageField(
        upload_to='property_images/', null=True, blank=True, validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'svg', 'avif'])
        ])


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        save_resized_image(self.associated_property_image)

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    associated_project_image = models.ImageField(
        upload_to='project_images/', null=True, blank=True, validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'svg', 'avif'])
        ])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        save_resized_image(self.associated_project_image)
      
class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    phone = models.IntegerField()
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class InspectionBooking(models.Model):
    name = models.CharField(max_length=255)
    phone = models.IntegerField()
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"


class Property_Review(models.Model):
    properties = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}'s Review"


class Project_Review(models.Model):
    properties = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}'s Review"


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Blog(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20)
    description = models.CharField(max_length=1000)
    content = models.TextField(default='')
    image = models.ImageField(
        upload_to='blogpost_images/', null=True, blank=True, validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'svg', 'avif'])
        ])
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        save_resized_image(self.image)
        
    
    def __str__(self):
        return self.title
