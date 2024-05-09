from django.urls import path
from . import views

urlpatterns = [
    path('homepage/' , views.homepage, name="homepage"),
    path('ClientDataEntry/' , views.ClientDataEntry, name="ClientDataEntry"),
    path('Results/' , views.Results, name="Results"),
    path('Results/<prediction>/', views.Results, name='Results'),
]