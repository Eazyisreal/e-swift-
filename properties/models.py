from django.db import models
from authentication.models import CustomUser
from PIL import Image
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

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
    image = models.ImageField(upload_to='agent_images', null=True, blank=True)


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
        img = Image.open(self.thumbnail.path)

        # When image height is greater than its width
        if img.height > img.width:
            # make square by cutting off equal amounts top and bottom
            left = 0
            right = img.width
            top = (img.height - img.width)/2
            bottom = (img.height + img.width)/2
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.thumbnail.path)

        # When image width is greater than its height
        elif img.width > img.height:
            # make square by cutting off equal amounts left and right
            left = (img.width - img.height)/2
            right = (img.width + img.height)/2
            top = 0
            bottom = img.height
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.thumbnail.path)

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Project"
        verbose_name_plural = "Projects"


class Property(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    property_type = models.CharField(max_length=100)
    category = models.ForeignKey(Property_Category,  on_delete=models.CASCADE)
    price = models.IntegerField()
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
        img = Image.open(self.thumbnail.path)

        # When image height is greater than its width
        if img.height > img.width:
            # make square by cutting off equal amounts top and bottom
            left = 0
            right = img.width
            top = (img.height - img.width)/2
            bottom = (img.height + img.width)/2
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.thumbnail.path)

        # When image width is greater than its height
        elif img.width > img.height:
            # make square by cutting off equal amounts left and right
            left = (img.width - img.height)/2
            right = (img.width + img.height)/2
            top = 0
            bottom = img.height
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 500 or img.width > 500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.thumbnail.path)

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
        img = Image.open(self.associated_property_image.path)

        # When image height is greater than its width
        if img.height > img.width:
            # make square by cutting off equal amounts top and bottom
            left = 0
            right = img.width
            top = (img.height - img.width)/2
            bottom = (img.height + img.width)/2
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 500 or img.width > 500:
                output_size = (8000, 8000)
                img.thumbnail(output_size)
                img.save(self.associated_property_image.path)

        # When image width is greater than its height
        elif img.width > img.height:
            # make square by cutting off equal amounts left and right
            left = (img.width - img.height)/2
            right = (img.width + img.height)/2
            top = 0
            bottom = img.height
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 300 or img.width > 300:
                output_size = (8000, 8000)
                img.thumbnail(output_size)
                img.save(self.associated_property_image.path)

        # When image width is greater than its height
        elif img.width > img.height:
            # make square by cutting off equal amounts left and right
            left = (img.width - img.height)/2
            right = (img.width + img.height)/2
            top = 0
            bottom = img.height
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 200 or img.width > 200:
                output_size = (8000, 8000)
                img.thumbnail(output_size)
                img.save(self.associated_property_image.path)

        # When image width is greater than its height
        elif img.width > img.height:
            # make square by cutting off equal amounts left and right
            left = (img.width - img.height)/2
            right = (img.width + img.height)/2
            top = 0
            bottom = img.height
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 100 or img.width > 100:
                output_size = (8000, 8000)
                img.thumbnail(output_size)
                img.save(self.associated_property_image.path)


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    associated_project_image = models.ImageField(
        upload_to='project_images/', null=True, blank=True, validators=[
            FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'svg', 'avif'])
        ])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.associated_project_image.path)

        # When image height is greater than its width
        if img.height > img.width:
            # make square by cutting off equal amounts top and bottom
            left = 0
            right = img.width
            top = (img.height - img.width)/2
            bottom = (img.height + img.width)/2
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 500 or img.width > 500:
                output_size = (8000, 8000)
                img.thumbnail(output_size)
                img.save(self.associated_project_image.path)

        # When image width is greater than its height
        elif img.width > img.height:
            # make square by cutting off equal amounts left and right
            left = (img.width - img.height)/2
            right = (img.width + img.height)/2
            top = 0
            bottom = img.height
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 300 or img.width > 300:
                output_size = (8000, 8000)
                img.thumbnail(output_size)
                img.save(self.associated_project_image.path)

        # When image width is greater than its height
        elif img.width > img.height:
            # make square by cutting off equal amounts left and right
            left = (img.width - img.height)/2
            right = (img.width + img.height)/2
            top = 0
            bottom = img.height
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 200 or img.width > 200:
                output_size = (8000, 8000)
                img.thumbnail(output_size)
                img.save(self.associated_project_image.path)

        # When image width is greater than its height
        elif img.width > img.height:
            # make square by cutting off equal amounts left and right
            left = (img.width - img.height)/2
            right = (img.width + img.height)/2
            top = 0
            bottom = img.height
            img = img.crop((left, top, right, bottom))
            # Resize the image to 300x300 resolution
            if img.height > 100 or img.width > 100:
                output_size = (8000, 8000)
                img.thumbnail(output_size)
                img.save(self.associated_project_image.path)


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

    def __str__(self):
        return self.title