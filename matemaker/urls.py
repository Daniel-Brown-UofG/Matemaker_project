from django.urls import path
from matemaker import views
app_name = 'matemaker'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('contact_us/', views.contact_us, name ='contact_us'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('signout/', views.signout, name='signout'),
    path('register/', views.register, name='register'),
    path('genres/', views.genres, name='genres'),
    path('genres/add_genre/', views.add_genre, name='add_genre'),
    path('genres/<slug:genre_name>/', views.genre, name='genre'),
    path('genres/<slug:genre_name>/<slug:interest_name>/', views.interest, name='interest'),
    path('genres/<slug:genre_name>/<slug:interest_name>/join/', views.join, name='join'),
    path('genres/<slug:genre_name>/<slug:interest_name>/leave/', views.leave, name='leave'),
    path('genres/<slug:genre_name>/<slug:interest_name>/like/', views.like, name='like'),
    path('add_interest/<slug:genre_name>/', views.add_interest, name='add_interest'),
    path('user/<slug:user_profile>/', views.profile_page, name="profile"),
    path('edit_profile/<slug:user_profile>/', views.edit_profile, name="edit_profile"),

]
