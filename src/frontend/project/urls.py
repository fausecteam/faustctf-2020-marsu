from django.urls import path

from . import views

app_name = 'project'
urlpatterns = [
    path('view/<int:project>/',    views.view_project, name='view'),
    path('create/',    views.create, name='create'),
    path('create/pad',    views.create_pad, name='create-pad'),
    path('add/pad',    views.add_pad, name='add-pad'),
]
