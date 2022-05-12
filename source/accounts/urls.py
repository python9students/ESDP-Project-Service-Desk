from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

# from accounts.views import MyLoginView

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]
