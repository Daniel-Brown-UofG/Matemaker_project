from django.urls import path
from matemaker import views
app_name = 'matemaker'

urlpatterns = [
    path('', views.home, name = 'home'),
    path('contact_us/', views.contact_us, name ='contact_us'),
    path('login/', views.user_login, name='login'),
    path('restricted/', views.restricted, name='restricted'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('genres/', views.genres, name='genres'),
    path('genres/add_genre/', views.add_genre, name='add_genre'),
]