from django.urls import path, include, reverse, reverse_lazy
from django.contrib.auth import views as auth_views

from .views import SignUpView

app_name = 'accounts'
urlpatterns = [
    # path("", include("django.contrib.auth.urls"), name="accounts"),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("password_reset/", auth_views.PasswordResetView.as_view(success_url=reverse_lazy('accounts:password_reset_done')), name='password_reset'),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path("password_reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('accounts:password_reset_complete')), name='password_reset_confirm'),
    path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]