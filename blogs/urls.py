from django.urls import include, path

from blogs.views import BlogDetail, BlogList

urlpatterns = [
    path("blogs/", BlogList.as_view()),
    path("blogs/<slug>/", BlogDetail.as_view()),
]
