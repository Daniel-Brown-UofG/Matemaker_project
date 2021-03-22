from django.contrib import admin
from matemaker.models import UserProfile, Genre, Interest
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Genre)
admin.site.register(Interest)