from django.urls import path, reverse
from django.views.generic.base import TemplateView
from django.contrib.auth.views import PasswordChangeView

from . import views

app_name = 'researcher'
urlpatterns = [
    path('', TemplateView.as_view(template_name='researcher/profile.xml'), name='view'),
    path('edit/', views.edit, name='edit'),
    path('password/', PasswordChangeView.as_view(success_url=''), name='password'),
    path('get/friends/', views.get_friends, name='get-friends'),
]
