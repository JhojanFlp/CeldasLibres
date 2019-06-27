from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import SignUpView
from .forms import LoginForm

# Aca van todas las rutas de las cuentas
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(
        template_name='accounts/login.html', authentication_form=LoginForm
        ),
        name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]