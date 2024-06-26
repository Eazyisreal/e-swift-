from django.db import models
from cloudinary.models import CloudinaryField
from django.utils.text import slugify
from authentication.models import CustomUser


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
    image = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.name
    
    

class Project(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price = models.IntegerField()
    status = models.CharField(max_length=100)
    category = models.ForeignKey(Project_Category, on_delete=models.CASCADE)
    no_of_block = models.IntegerField()
    no_of_flat = models.IntegerField()
    no_of_floors = models.IntegerField()
    thumbnail = CloudinaryField('image', null=True, blank=True)
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

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Project"
        verbose_name_plural = "Projects"

class Property(models.Model):
    AVAILABILITY_CHOICES = [
        ('Selling', 'Selling'),
        ('Rent', 'Rent'),
    ]
    availability = models.CharField(max_length=12, choices=AVAILABILITY_CHOICES)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    property_type = models.CharField(max_length=100)
    category = models.ForeignKey(Property_Category, on_delete=models.CASCADE)
    price = models.IntegerField()
    living_room = models.IntegerField()
    dining = models.IntegerField()
    no_of_bedrooms = models.IntegerField()
    no_of_bathrooms = models.IntegerField()
    no_of_floors = models.IntegerField()
    thumbnail = CloudinaryField('image', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    features = models.CharField(max_length=255)
    associated_agent = models.ManyToManyField(Agent)
    slug = models.SlugField(unique=True, max_length=255, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else "Untitled Property Listing"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Property"
        verbose_name_plural = "Properties"

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    associated_property_image = CloudinaryField('image', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    associated_project_image = CloudinaryField('image', null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    phone = models.IntegerField()
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}'s Message"
    
class ProjectContactMessage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_messages')
    name = models.CharField(max_length=255)
    phone = models.IntegerField()
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contact Message about {self.project}"

class InspectionBooking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_inspection')
    name = models.CharField(max_length=255)
    phone = models.IntegerField()
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inspection Booking for {self.property}"

class Property_Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.property} by {self.user.email}'

class Project_Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review for {self.project} by {self.user.email}'

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class Blog(models.Model):
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20)
    description = models.CharField(max_length=1000)
    content = models.TextField(default='')
    image = CloudinaryField('image', null=True, blank=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
    
class Staff(models.Model):
    name= models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = CloudinaryField('image', null=True, blank=True)
    phone = models.IntegerField()
    email = models.EmailField()
    
    
    def __str__(self):
        return f'{self.name} - {self.position}'

    