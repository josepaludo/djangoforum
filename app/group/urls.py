from django.urls import path

from . import views

app_name = 'group'
urlpatterns = [
    path('', views.GroupIndex.as_view(), name="groupindex"),
    path('page/<int:group_id>/', views.GroupPage.as_view(), name="grouppage"),
    path('create/', views.CreateGroup.as_view(), name="creategroup"),
    path('browse/', views.BrowseGroups.as_view(), name="browsegroups"),
    path('discover/', views.DiscoverGroups.as_view(), name="discovergroups"),
    path(
        'members/<int:group_id>/',
        views.GroupMembers.as_view(),
        name="groupmembers"
    ),
    path(
        'admins/<int:group_id>/',
        views.GroupAdmins.as_view(),
        name="groupadmins"
    ),
    path(
        'groupsettings/<int:group_id>/<str:link_id>/',
        views.GroupSettings.as_view(),
        name="groupsettings"
    ),
    path(
        'managemembers/<int:group_id>/<str:username>/<int:code>/',
        views.ManageMembers.as_view(),
        name="managemembers"),
    path(
        'joinleave/<int:group_id>/<int:joinleave_code>/',
        views.JoinLeaveGroup.as_view(),
        name="joinleavegroup"
    ),
    path(
        'invitehandler/<int:group_id>/',
        views.InviteHandler.as_view(),
        name="invitehandler"
    ),
    path(
        'joinbyinvitation/<str:link_id>/',
        views.JoinByInvitation.as_view(),
        name="joinbyinvitation"
    ),
]
