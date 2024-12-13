from django.urls import path
from .views import PushApiView, pull_content, index_view

urlpatterns = [
    path("", index_view, name="index"),
    path("push/", PushApiView.as_view(), name="push"),
    path("pull/<id>/", pull_content, name="pull"),
]
