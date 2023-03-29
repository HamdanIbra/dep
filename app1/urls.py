from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('registration', views.registration),
    path('wall', views.wall),
    path('login', views.login),
    path('logout', views.logout),
    path('create_message', views.create_message),
    path('create_comment', views.create_comment),
    path('delete_message', views.delete_message),
    path('delete_comment', views.delete_comment),
]