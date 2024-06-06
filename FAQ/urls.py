from django.urls import path
from .views import FAQCreateView, FAQDetail

urlpatterns = [
    path('faq/',FAQCreateView.as_view()),
    path('faqs/<int:pk>/', FAQDetail.as_view()),
]
