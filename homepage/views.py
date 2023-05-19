from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.models import User

from post.forms import MainPostForm
from post.models import MainPost, Post, Answer
from group.models import Group
from user.models import Profile


class Index(TemplateView):

    def get(self, request):
        context = {
            "posts": MainPost.objects.all(),
            "is_post": False,
        }
        return render(request, "homepage/index.html", context)


class PostView(TemplateView):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse("user:login"))
        context = {
            "form": MainPostForm(),
            "is_post": True,
            "user_groups": request.user.member_groups.all(),
        }
        return render(request, "homepage/index.html", context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse("user:login"))

        form = MainPostForm(request.POST)
        if not form.is_valid():
            return redirect(reverse("homepage:post"))

        try:
            group_id = int(request.POST['group'])
            group = Group.objects.get(id=group_id)
        except ValueError:
            group = None
        except Group.DoesNotExist:
            return redirect(reverse("homepage:post"))

        if group and request.user not in group.members.all():
            return redirect(reverse(
                "group:grouppage",
                kwargs={
                    "group_id": group.id,
                }
            ))

        post = MainPost.objects.create(
            user=request.user,
            title=request.POST["title"],
            content=request.POST["content"],
            group=group,
        )
        post.save()

        return redirect(reverse(
            "post:mainpost",
            kwargs={
                "user": post.user.username,
                "post_id": post.id,
            }
        ))


class Search(TemplateView):

    def get(self, request):
        context = {
        }
        return render(request, "homepage/search.html", context)

    def post(self, request):

        query = request.POST["query"]
        search_params = {
            "postTitle": MainPost.objects.filter(title__icontains=query),
            "postContentMain": MainPost.objects.filter(content__icontains=query), 
            "postContentAnswer": Answer.objects.filter(content__icontains=query), 
            "userName": User.objects.filter(username__icontains=query), 
            "userBio": User.objects.filter(profile__bio__icontains=query), 
            "groupName": Group.objects.filter(name__icontains=query), 
            "groupDescription": Group.objects.filter(description__icontains=query),
        }
        context = {**search_params, "query": query}

        return render(request, "homepage/search.html", context)


class Following(TemplateView):


    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse("user:login"))

        followings = request.user.followings.all()
        followings_posts = MainPost.objects.filter(user__profile__in=followings)

        groups = request.user.member_groups.all()
        group_posts = MainPost.objects.filter(group__in=groups)

        context = {
            "posts": followings_posts | group_posts,
            "following": True,
        }
        return render(request, "homepage/index.html", context)
