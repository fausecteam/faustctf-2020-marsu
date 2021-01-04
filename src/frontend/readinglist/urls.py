

from django.urls import path


from . import views

app_name = 'readinglist'

urlpatterns = [
    path('',    views.index, name='index'),
    path('add', views.add,   name='add'),
    path('list', views.listpapers, name='list'),
    path('list/<username>', views.listpapers, name='list'),
    path('detail/<source>/<path:handle>', views.detail,   name='detail'),    
]
