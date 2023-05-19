from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views.generic import TemplateView, View
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError

from .forms import LoginForm, RegisterForm, ProfileSettingsForm
from .models import Profile
from post.models import MainPost


class Login(TemplateView):

    def get(self, request):
        login_form = LoginForm()
        context = {
            "form": login_form,
        }
        return render(request, "user/login.html", context)

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return(redirect(reverse("homepage:index")))
        else:
            login_form = LoginForm()
            context = {
                "form": login_form,
                "failed": True,
            }
            return render(request, "user/login.html", context)


class Logout(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('homepage:index'))


class Register(TemplateView):

    def get(self, request):
        register_form = RegisterForm()
        context = {
            "form": register_form,
            "names": [user.username for user in User.objects.all()]
        }
        return render(request, "user/register.html", context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if not register_form.is_valid():
            return redirect(reverse("user:register"))

        user = register_form.save()
        profile = Profile.objects.create(
            user=user,
            bio=f"Hi there, I'm {user.username} and this is my profile page!"
        )
        profile.save()

        return redirect(reverse("user:login"))


class ProfileView(TemplateView):

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect(reverse("homepage:index"))

        context = {
            "user": user,
            "posts": MainPost.objects.filter(user=user)
        }
        return render(request, "user/profile.html", context)


class Follow(TemplateView):

    def get(self, request, user_id):
        if not request.user.is_authenticated:
            return redirect(reverse("user:login"))
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect(reverse("homepage:index"))

        if request.user in user.profile.followers.all():
            user.profile.followers.remove(request.user)
        else:
            user.profile.followers.add(request.user)

        return redirect(reverse(
            "user:profile",
            kwargs={
                "username": user
            }
        ))


class Settings(TemplateView):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse("user:login"))
        
        context = {
            "form": ProfileSettingsForm(),
        }
        return render(request, "user/settings.html", context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse("user:login"))

        form = ProfileSettingsForm(request.POST)
        if not form.is_valid():
            return redirect(reverse("user:settings"))

        try:
            request.user.profile.image = request.FILES["image"]
        except MultiValueDictKeyError:
            pass
        request.user.profile.bio = request.POST["bio"]
        request.user.profile.save()

        return redirect(reverse(
            "user:profile",
            kwargs={
                "username": request.user.username,
            }
        ))


class Followers(TemplateView):

    def get(self, request, user_id):

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect(reverse("homepage:index"))
        
        context = {
            "user": user,
            "users": user.profile.followers.all(),
        }
        return render(request, "user/followers.html", context)


class MemberGroups(TemplateView):

    def get(self, request, user_id):

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect(reverse("homepage:index"))
        
        context = {
            "user": user,
            "groups": user.member_groups.all(),
        }
        return render(request, "user/membergroups.html", context)


class AdminGroups(TemplateView):

    def get(self, request, user_id):

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect(reverse("homepage:index"))
        
        context = {
            "user": user,
            "groups": user.admin_groups.all(),
        }
        return render(request, "user/admingroups.html", context)
