from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ActivateView, MeView

urlpatterns = [
    path(r'register', RegisterView.as_view(), name="user-register"),
    path(r'activate/', ActivateView.as_view(), name="user-activation"),
    path(r'login', LoginView.as_view(), name="user-login"),
    path(r'logout', LogoutView.as_view(), name="user-logout"),
    path(r'me', MeView.as_view(), name="me")

]
