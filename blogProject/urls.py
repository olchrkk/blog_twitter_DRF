from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.models import User
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls')),
    path('api/', include('api.urls')),
    path('upload/', include('upload.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
