from django.urls import path
from .views import RegisterAdminView,AdminUserDetailView,LoginView,LogoutView,PasswordConfirmView,PasswordResetView,OTPConfirmationView



urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/admin/', RegisterAdminView.as_view(), name='register-admin'),
    path('users/', AdminUserDetailView.as_view(), name='user-list'),
    path('users/<uuid:pk>/', AdminUserDetailView.as_view(), name='user-detail'),
    path("resetpassword/", PasswordResetView.as_view(), name="resetpassword"),
    path("confirmpassword/", PasswordConfirmView.as_view(), name="resetpassword"),
    path("confirmotp/", OTPConfirmationView.as_view(), name="confirmotp"),
]
