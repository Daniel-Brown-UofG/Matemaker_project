from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class Genre(models.Model):

	name = models.CharField(max_length=64, unique=True)
	views = models.IntegerField(default=0)
	members = models.IntegerField(default=0)
	date = models.DateTimeField('date created',null=True)
	slug = models.SlugField(unique = True)
	creator = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Genre, self).save(*args,**kwargs)
	
	class Meta:
		verbose_name_plural = "Genres"

	def __str__(self): 
		return self.name


class Interest(models.Model):

	genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
	name = models.CharField(max_length=64, unique=True)
	description = models.CharField(max_length=128, unique=False, default='no description')
	views = models.IntegerField(default=0)
	members = models.IntegerField(default=0)
	date = models.DateTimeField('date created',null=True)
	slug = models.SlugField(unique = True)
	creator = models.ForeignKey(User, on_delete=models.DO_NOTHING,null=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Interest, self).save(*args,**kwargs)
		
	def __str__(self): 
		self.slug = slugify(self.name)
		return self.name


class UserProfile(models.Model):
    # This line is required. Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    intersts = models.ManyToManyField(Interest, blank=True)
    
    # The additional attributes we wish to include.
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True, default= 'defaults/default_pp.jpg')


    def __str__(self):
        return self.user.username
