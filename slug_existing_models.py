import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'Matemaker_Project.settings')
import django
django.setup() 
from matemaker.models import Genre, Interest
from django.template.defaultfilters import slugify

def slug_all():
    genres = Genre.objects.all()
    interests = Interest.objects.all()

    for g in genres:
        g.slug = slugify(g.name)
    
    for i in interests:
        i.slug = slugify(i.name)

    return