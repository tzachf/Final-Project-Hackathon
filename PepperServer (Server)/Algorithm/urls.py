from django.urls import path
from . import views


urlpatterns = [
    path('', views.analyzeMovement, name='analyze'),
]
