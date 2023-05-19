from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    path('login/', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    path('register/', views.Register.as_view(), name="register"),
    path('profile/<str:username>/', views.ProfileView.as_view(), name="profile"),
    path('follow/<int:user_id>/', views.Follow.as_view(), name="follow"),
    path('settings/', views.Settings.as_view(), name="settings"),
    path('followers/<int:user_id>/', views.Followers.as_view(), name="followers"),
    path('membergroups/<int:user_id>/', views.MemberGroups.as_view(), name="membergroups"),
    path('admingroups/<int:user_id>/', views.AdminGroups.as_view(), name="admingroups"),
]