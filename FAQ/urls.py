from django.urls import path
from .views import FAQCreateView

urlpatterns = [
    path('faq/',FAQCreateView.as_view()),
]
