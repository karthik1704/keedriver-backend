from django.urls import path
from .views import ContactCreateView

urlpatterns = [
    path('contacts/add/',ContactCreateView.as_view()),
]
