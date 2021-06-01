  
from django.urls import path

from .views.users.users_favorited import user_favorited_list

urlpatterns = [
    path('reports/user_favorited', user_favorited_list),
]