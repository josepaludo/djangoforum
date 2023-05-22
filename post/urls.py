from django.urls import path

from . import views

app_name = "post"
urlpatterns = [
    path('mainpost/<str:user>/<int:post_id>/', views.MainPostView.as_view(), name="mainpost"),
    path('answer/<int:post_id>/', views.MakeAnswer.as_view(), name="makeanswer"),
    path('vote/<int:vote_value>/<int:post_id>/', views.VotePost.as_view(), name="votepost"),
    path('deletepost/<int:post_id>', views.DeletePost.as_view(), name="deletepost"),
]
