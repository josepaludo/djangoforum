from uuid import UUID
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView
from django.db.models import Count
from django.contrib.auth.models import User

from .forms import GroupForm
from .models import Group, InviteLink
from post.models import MainPost
from post.forms import MainPostForm


class GroupPage(TemplateView):

    def get(self, request, group_id):
        group = Group.objects.get(id=group_id)
        context = {
            "form": MainPostForm(),
            "group": group,
            "posts": MainPost.objects.filter(group=group)
        }
        return render(request, "group/grouppage.html", context)


class GroupIndex(TemplateView):

    def get(self, request):
        context = {
        }
        return render(request, "group/groupindex.html", context)


class BrowseGroups(TemplateView):

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse("user:login"))
        context = {
            "groups": Group.objects.filter(members=request.user)
        }
        return render(request, "group/browsegroups.html", context)


class DiscoverGroups(TemplateView):

    def get(self, request):
        groups = Group.objects.annotate(num_members=Count('members'))
        context = {
            "groups": groups.order_by("-num_members"), 
        }
        return render(request, "group/discovergroups.html", context)


class CreateGroup(TemplateView):

    def get(self, request):
        context = {
            "form": GroupForm(),
        }
        return render(request, "group/creategroup.html", context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse("user:login"))
        
        form = GroupForm(request.POST)
        if not form.is_valid():
            return redirect(reverse("group:creategroup"))

        new_group = Group.objects.create(
            name=request.POST["name"],
            description=request.POST["description"],
            creator=request.user,
        )
        new_group.save()
        new_group.admins.add(request.user)
        new_group.members.add(request.user)

        return redirect(reverse(
            "group:grouppage",
            kwargs={
                "group_id": new_group.id,
            }
        ))


class JoinLeaveGroup(TemplateView):

    def get(self, request, group_id, joinleave_code):
        if not request.user.is_authenticated:
            return redirect(reverse("user:login"))

        group = Group.objects.get(id=group_id)
        match joinleave_code:
            case 1:
                if request.user not in group.blockeds.all():
                    group.members.add(request.user)
            case 0:
                group.members.remove(request.user)
                group.admins.remove(request.user)

        return redirect(reverse(
            "group:grouppage",
            kwargs={
                "group_id": group_id,
            }
        ))


class GroupMembers(TemplateView):

    def get(self, request, group_id):
        if not request.user.is_authenticated:
            return redirect(reverse("user:login"))
        
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return redirect(reverse("homepage:index"))

        context = {
            "users": User.objects.filter(member_groups=group),
            "group": group,
        }
        return render(request, "group/groupmembers.html", context)


class GroupAdmins(TemplateView):

    def get(self, request, group_id):
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return redirect(reverse("homepage:index"))

        context = {
            "users": User.objects.filter(admin_groups=group),
            "group": group,
        }
        return render(request, "group/groupadmins.html", context)


class ManageMembers(TemplateView):

    def get(self, request, group_id, username, code):
        if not request.user.is_authenticated:
            return redirect(reverse("user:login"))
        
        try:
            group = Group.objects.get(id=group_id)
            user = User.objects.get(username=username)
        except (Group.DoesNotExist, User.DoesNotExist):
            return redirect(reverse("homepage:index"))
        request_user_is_creator = request.user == group.creator

        if user == group.creator or \
            request.user not in group.admins.all() or \
            user not in group.members.all() or \
            (user in group.admins.all() and not request_user_is_creator):

            code = "Unauthorized"

        match code:
            case 0:
                group.admins.add(user)
            case 1:
                if request_user_is_creator:
                    group.admins.remove(user)
            case 2:
                group.members.remove(user)
            case 3:
                group.admins.remove(user)
                group.members.remove(user)
                group.blockeds.add(user)

        return redirect(reverse(
            "group:groupmembers",
            kwargs={
                "group_id": group.id,
            }
        ))
        

class GroupSettings(TemplateView):

    def get(self, request, group_id, link_id):
        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return redirect(reverse("homepage:index"))

        if request.user not in group.admins.all():
            return redirect(reverse(
                "group:groupmembers",
                kwargs={
                    "group_id": group.id,
                }
            ))

        context = {
            "group": group,
            "form": GroupForm(),
            "invalid_names": [group.name for group in Group.objects.all()],
            "link_id": link_id if link_id != 0 else None,
        }
        return render(request, "group/groupsettings.html", context)


class InviteHandler(TemplateView):

    def get(self, request, group_id):

        now = datetime.now()
        for link in InviteLink.objects.all():
            one_day_passed = now - link.created_at > timedelta(hours=24)
            if one_day_passed:
                link.delete()

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return redirect(reverse("homepage:index"))

        if request.user not in group.admins.all():
            return redirect(reverse("homepage:index"))

        link = InviteLink.objects.create(
            group=group,
        )
        return redirect(reverse(
            "group:groupsettings",
            kwargs={
                "group_id": group.id,
                "link_id": str(link.id),
            }
        ))


class JoinByInvitation(TemplateView):

    def get(self, request, link_id):
        if not request.user.is_authenticated:
            return redirect(reverse("user:login"))

        id = UUID(link_id)
        try:
            invite_link = InviteLink.objects.get(id=id)
        except InviteLink.DoesNotExist:
            print("something went very very wrong")
            return redirect(reverse("homepage:index"))

        group = invite_link.group
        group.blockeds.remove(request.user)
        group.members.add(request.user)
        invite_link.delete()

        return redirect(reverse(
            "group:grouppage",
            kwargs={
                "group_id": group.id,
            }
        ))
