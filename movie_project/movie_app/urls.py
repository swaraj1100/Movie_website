from . import views
from django.urls import path,include
from .views import search_results


urlpatterns = [
    path('',views.home,name='home'),
    path('register/',views.register, name='register'),
    path('login/',views.login, name='login'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('movie/', views.movie_list, name='movie_list'),
    path('add/', views.add_movie, name='add_movie'),
    path('edit/<int:pk>/', views.edit_movie, name='edit_movie'),
    path('movie/delete/<int:pk>/', views.delete_movie, name='delete_movie'),
    path('logout/', views.my_logout_view, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('search/', search_results, name='search_results'),
    path('profile/', views.view_profile, name='view_profile'),
    path('movies_by_category/<int:category_id>/', views.movies_by_category, name='movies_by_category'),

]