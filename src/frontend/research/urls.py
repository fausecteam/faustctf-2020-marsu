from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from django.views.generic.base import RedirectView

from .views import signup

urlpatterns = [
    path('', RedirectView.as_view(pattern_name='researcher:view'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/register', signup, name='register'),
    path('accounts/profile/', RedirectView.as_view(pattern_name='researcher:view')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('r/', include('readinglist.urls')),
    path('p/', include('project.urls')),
    path('u/', include('researcher.urls')),    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
