from django.urls import path
from .views import profile, index

from . import views

app_name = 'crypto'

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('profile/', profile.as_view(), name='profile'),
]
