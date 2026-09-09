from django.urls import path
from .views import cesfam_view


urlpatterns = [
    path("", cesfam_view, name="cesfam"),
]