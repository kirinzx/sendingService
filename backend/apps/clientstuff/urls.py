from django.urls import path
from .views import CreateClientView, DestroyUpdateClientView


urlpatterns = [
    path('client/', CreateClientView.as_view()),
    path('client/<int:phone_number>', DestroyUpdateClientView.as_view()),
]