from django.urls import path
from . import views

urlpatterns = [
    path('create_character/<str:name>/', views.create_character, name='create_character'),
    path('get_character/<str:name>/', views.get_character, name='get_character'),
    path('create_characters/', views.create_characters, name='create_characters'),
    # Add more paths for other operations
]
