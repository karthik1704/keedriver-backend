from django.urls import include, path

from blogs.views import BlogDetail, BlogList, BlogPinsList

urlpatterns = [
    path("blogs/", BlogList.as_view()),
    path("blogs/pins/", BlogPinsList.as_view()),
    path("blogs/<slug>/", BlogDetail.as_view()),
]
