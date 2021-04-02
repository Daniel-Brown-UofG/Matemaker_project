from django import template
from matemaker.models import Genre
register = template.Library()

@register.inclusion_tag('matemaker/genrelist.html')
def get_genre_list():
    return {'genres': Genre.objects.all()}
