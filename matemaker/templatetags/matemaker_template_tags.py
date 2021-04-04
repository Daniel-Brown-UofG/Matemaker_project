from django import template
from matemaker.models import Genre, Interest
register = template.Library()

@register.inclusion_tag('matemaker/genrelist.html')
def get_genre_list():
    return {'genres': Genre.objects.all()}

@register.inclusion_tag('matemaker/interestlist.html')
def get_interest_list(current_genre):
    genre = Genre.objects.get(name=current_genre)

    interests = Interest.objects.filter(genre=genre)
    return {'interests': interests}