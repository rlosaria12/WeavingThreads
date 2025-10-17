from django.urls import path
from .views import indicator_list_view

urlpatterns = [
    path('indicators/', indicator_list_view, name='indicator-list'),
]
