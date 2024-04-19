from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('home_module.urls')),
    path('admin/', admin.site.urls),
    path('user-profile/', include('users.urls')),
    path('user-panel/', include('user_panel.urls')),
    path('content/', include('contents.urls')),
    path('user-activities/', include('user_activities.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
