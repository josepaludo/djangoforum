from django.urls import path

from . import views

app_name = 'homepage'
urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('post/', views.PostView.as_view(), name="post"),
    path('search/', views.Search.as_view(), name="search"),
    path('following/', views.Following.as_view(), name="following"),
]
