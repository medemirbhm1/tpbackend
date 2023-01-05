from django.db import models
from django.contrib import admin
from django.dispatch import receiver
import os
from django.contrib.auth.models import AbstractBaseUser



def upload_to(instance, filename):
    return 'posts/{filename}'.format(filename=filename)


class User (AbstractBaseUser):
    password = None
    username = models.CharField(max_length=50,unique = True )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    picture = models.CharField(max_length=200 , blank = True, null=True)
    email = models.EmailField(blank=True,unique=True)
    phone_num = models.CharField(max_length=30 ,blank = True, null=True)
    favorits = models.ManyToManyField('RealEstateAdd')

    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.first_name+' '+self.last_name


class RealEstateAdd(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    type = models.CharField(max_length=100)
    surface = models.FloatField(null=True)
    price = models.FloatField(null=True)
    pub_date = models.DateField(auto_now_add=True)
    localisation = models.CharField(max_length=300)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)
    wilaya = models.CharField(max_length=50)
    commune = models.CharField(max_length=50)
    owner = models.ForeignKey(User,on_delete=models.CASCADE, related_name='ownedReas')
    #Add for later : ImageFiled + Choices for category and type

    def __str__(self):
        return self.title

class Photo(models.Model):
    rea = models.ForeignKey(RealEstateAdd, on_delete=models.CASCADE, related_name='photos', null=True)
    photo = models.ImageField(upload_to=upload_to, default='posts/default.jpg')

@receiver(models.signals.post_delete, sender=Photo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.photo:
        if os.path.isfile(instance.photo.path):
            os.remove(instance.photo.path)

class Offer(models.Model):
    description = models.TextField()
    proposal = models.FloatField()
    offerer = models.ForeignKey(User,on_delete=models.CASCADE, related_name='offers')
    real_estate = models.ForeignKey(RealEstateAdd,on_delete=models.CASCADE, related_name='offers')
    
    def __str__(self):
        return self.description











# Create your models here.
