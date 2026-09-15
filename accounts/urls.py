from django.urls import path
from . import views


app_name = "accounts"


urlpatterns = [

    path(
        "",
        views.home_view,
        name="home"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        "aplicaciones/<str:seccion>/",
        views.aplicaciones_home,
        name="aplicaciones_home"
    ),

]