from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.review_list, name='review_list'), # Homepage -- list of all reviews
    path('review/<int:pk>/', views.review_detail, name='review_detail'), # Detail view of single review
    path('review/<int:pk>/edit/', views.review_edit, name='review_edit'), # Edit an existing review
    path('review/new/', views.review_new, name='review_new'), # Create a new review
    path('review/new/<str:pk>/', views.review_new, name='review_new'), # Create a new review
    path('search/', views.search, name='search'), # Create a new review
    path('album/<str:pk>', views.album_detail, name='album_detail'), # Detail view of single album
    path('user/<str:user>/', views.user_detail, name='user_detail'),
    path('user/<str:user>/follow/', views.user_follow, name='user_follow'),
    path('artist/<slug:artist>/', views.artist_detail, name='artist_detail'),
    # Signup, login and logout urls
    path('signup/', views.create_user, name='new_user'), # Sign up for an account
    path('login/', auth_views.LoginView.as_view(template_name='musicrate/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='musicrate/logout.html'), name='logout'),
]