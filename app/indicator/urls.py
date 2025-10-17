from django.urls import path
from . import views

urlpatterns = [
    path('program-indicator/', views.program_indicator, name='program_indicator'),
]
