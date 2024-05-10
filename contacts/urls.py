from django.urls import path
from .views import ContactsView

urlpatterns = [
    path('contacts/add/',ContactsView.as_view()),
]
