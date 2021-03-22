from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):

	name = models.CharField(max_length=64, unique=True)
	views = models.IntegerField(default=0)
	members = models.IntegerField(default=0)
	date = models.DateTimeField('date created',null=True)


	def __str__(self): 
		return self.name


class Interest(models.Model):

	genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
	name = models.CharField(max_length=64, unique=True)
	description = models.CharField(max_length=128, unique=False, default='no description')
	views = models.IntegerField(default=0)
	members = models.IntegerField(default=0)
	date = models.DateTimeField('date created',null=True)

	def __str__(self): 
		return self.name


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    intersts = models.ManyToManyField(Interest)
    
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)


    def __str__(self):
        return self.user.username
