import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'Matemaker_Project.settings')
import django
django.setup() 

from matemaker.models import Genre, Interest
from django.utils import timezone
def populate():

    esports= [
        {'name': 'CS:GO', 'description':'Most popular fps esports in the world'},
        {'name':'Dota2','description':'Holds record of the highest prize pool of moba esports in the world'},
        {'name':'Overwatch','description':'Basically combination of csgo and dota2'} ]
    sports = [{'name':'Soccer','description':'Use your feet'},
        {'name':'Basketball','description':'Use your hands'},
        {'name':'Football','description':'Use both feet and hands'} ]

    genres = {'Esports': {'interests': esports},'Sports': {'interests': sports}}

    for genre, genre_data in genres.items():
        g = add_genre(genre)
        for i in genre_data['interests']:
            add_interest(g, i['name'], i['description'])

    for g in Genre.objects.all():
        for i in Interest.objects.filter(genre=g):
            print(f'- {g}: {i}')

def add_interest(genre,name,des):
    i = Interest.objects.get_or_create(genre=genre, name=name, description=des)[0] 
    i.date = timezone.now()
    p=i.save()
    return i

def add_genre(name):
    g = Genre.objects.get_or_create(name=name)[0] 
    g.save()
    g.date = timezone.now()
    return g

if __name__=='__main__':
    print('Starting Matemaker population script...') 
    populate()


















