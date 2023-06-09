from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('homepage.urls')),
    path('post/', include('post.urls')),
    path('user/', include('user.urls')),
    path('group/', include('group.urls')),
    path('admin/', admin.site.urls),
] + static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
