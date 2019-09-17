from django.urls import path

from .views import deposit, withdraw

urlpatterns = [
    path('deposit/', deposit),
    path('withdraw/', withdraw),
]
