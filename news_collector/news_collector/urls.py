from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:room_name>/', views.chat_room, name='chat_room'),
]
urlpatterns = [
    ...
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
]
