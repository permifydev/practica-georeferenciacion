from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# función en Django que procesa e inicia la sesión de un usuario 
# cuando completa el formulario de login.

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("/")

    return render(request, "accounts/login.html")

# Este código funciona como un panel de inicio (Home) 
# que redirige o muestra un diseño distinto según el rol del usuario.

@login_required
def home_view(request):

    if request.user.is_staff:
        return render(request, "accounts/admin_home.html")

    return render(request, "accounts/user_home.html")



# Este código se encarga de cerrar la sesión del usuario 
# actual en tu aplicación web y luego enviarlo a la pantalla de inicio de sesión.

def logout_view(request):
    logout(request)
    return redirect("/login/")