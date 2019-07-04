from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import CrearUsuario, ModificarUsuario, VerUsuarios, EliminarUsuario
from .forms import LoginForm

# Aca van todas las rutas de las cuentas
urlpatterns = [
    path('signup/', CrearUsuario.as_view(), name='signup'),
    path('login/', LoginView.as_view(
        template_name='accounts/login.html', authentication_form=LoginForm
        ),
        name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('modificar-usuario/<int:pk>', ModificarUsuario.as_view(), name='modificar-usuario'),
    path('usuarios/', VerUsuarios.as_view(), name='usuarios'),
    path('eliminar-usuario/<int:pk>', EliminarUsuario.as_view(), name='eliminar-usuario'),
]