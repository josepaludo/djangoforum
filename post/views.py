from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.http import Http404

from .models import MainPost, Answer, Post
from .forms import AnswerForm


class MainPostView(TemplateView):

    def get(self, request, user, post_id):
        try:
            post = MainPost.objects.get(id=post_id)
        except MainPost.DoesNotExist:
            try:
                post = Answer.objects.get(id=post_id)
            except Answer.DoesNotExist:
                return redirect(reverse("homepage:index"))

        if post.user.username != user:
            raise Http404("Post not found.")

        context = {
            "mainpost": post,
            "post": post,
            "form": AnswerForm(),
        }
        return render(request, "post/mainpost.html", context)


class MakeAnswer(TemplateView):

    def get(self, request):
        return redirect("/")

    def post(self, request, post_id):
        if not request.user.is_authenticated:
            return redirect(reverse("user:login"))

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return redirect(reverse("homepage:index"))

        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer.objects.create(
                user=request.user,
                content=request.POST["content"],
                related_post=post,
            )
            answer.save()
        
        return redirect(reverse(
            "post:mainpost",
            kwargs={
                "user": post.user,
                "post_id": post.id,
            }
        ))

class VotePost(TemplateView):

    def get(self, request, vote_value, post_id):
        if not request.user.is_authenticated:
            return redirect(reverse("user:login"))

        try:
            post = MainPost.objects.get(id=post_id)
        except MainPost.DoesNotExist:
            try:
                post = Answer.objects.get(id=post_id)
            except Answer.DoesNotExist:
                return redirect(reverse("homepage:index"))

        match vote_value:
            case 1:
                post.downvoters.remove(request.user)
                if request.user not in post.upvoters.all():
                    post.upvoters.add(request.user)
                else:
                    post.upvoters.remove(request.user)
            case 0:
                post.upvoters.remove(request.user)
                if request.user not in post.downvoters.all():
                    post.downvoters.add(request.user)
                else:
                    post.downvoters.remove(request.user)
            case _:
                return Http404("Invalid vote value.")

        return redirect(reverse(
            "post:mainpost",
            kwargs={
                'user': post.user,
                'post_id': post.id,
            }
        ))


class DeletePost(TemplateView):

    def get(self, request, post_id):

        if not request.user.is_authenticated:
            return redirect(reverse('user:login'))

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return redirect(reverse('homepage:index'))

        if post.user == request.user:
            post.delete()
        
        return redirect(reverse('homepage:index'))
