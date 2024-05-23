from django.urls import path
from .views import ReviewByTripId,ReviewCreateTripId

urlpatterns = [
    path('review/<int:pk>',ReviewByTripId.as_view()),
    path('review/create/<int:pk>',ReviewCreateTripId.as_view()),

]