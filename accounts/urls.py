from django.urls import path
from . import views

# Este código es el archivo de configuración de rutas (URLs) 
# del módulo o aplicación accounts en Django. Se encarga de conectar 
# la dirección web que escribe el usuario en el navegador con la función 
# que la procesa (login_view).

app_name = 'accounts'

urlpatterns = [
        path("", views.home_view, name="home"),# Define la página principal del módulo.
        path("login/", views.login_view, name= "login"), #Define la página de inicio de sesión.
        path("logout/", views.logout_view, name="logout"), # usuario debe acceder para cerrar sesión
]