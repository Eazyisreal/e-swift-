from django.db import models
from PIL import Image

class Project_Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=255)
    location= models.CharField(max_length=255)
    status= models.CharField()
    category = models.ForeignKey(Project_Category,  on_delete=models.CASCADE)
    no_of_block = models.IntegerField()
    no_of_flat = models.IntegerField()
    no_of_floors = models.IntegerField()
    thumbnail = models.ImageField(upload_to='property_images/', null=True, blank=True)
    
    def __str__(self):
        return self.title if self.title else "Untitled Property Listing"

    def save(self, *args, **kwargs):
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
            if img.height > 500 or img.width >500:
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
            if img.height > 500 or img.width >500:
                output_size = (500, 500)
                img.thumbnail(output_size)
                img.save(self.thumbnail.path)

    class Meta:
        ordering = ['-updated', '-created']
        verbose_name = "Property"
        verbose_name_plural = "Properties"
        
        
        