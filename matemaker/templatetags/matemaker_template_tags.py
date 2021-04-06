from django import template
from matemaker.models import Genre, Interest, UserProfile, Post
register = template.Library()

@register.inclusion_tag('matemaker/genrelist.html')
def get_genre_list():
    return {'genres': Genre.objects.all()}

@register.inclusion_tag('matemaker/interestlist.html')
def get_interest_list(current_genre):
    genre = Genre.objects.get(name=current_genre)

    interests = Interest.objects.filter(genre=genre)
    return {'interests': interests}

@register.inclusion_tag('matemaker/memberlist.html')
def get_member_list(current_interest):
    interest = Interest.objects.get(name=current_interest)

    members = UserProfile.objects.filter(intersts=interest)
    return {'members': members}

@register.inclusion_tag('matemaker/postslist.html')
def get_post_list(current_interest, current_genre):
    interest = Interest.objects.get(name=current_interest)
    genre = Genre.objects.get(name=current_genre)
    posts = Post.objects.filter(interest=interest)
    return {'posts': posts, 'interest':interest, 'genre': genre}