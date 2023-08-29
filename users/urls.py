from django.urls import path
from users import views

urlpatterns = [
    path("register/",views.RegisterView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("userView/", views.UserView.as_view()),
    path("verification/",views.Check_otp_register.as_view()),
    path("forgetPassword/", views.ForgetPassword.as_view()),
    path("resetPassword/", views.ResetPassword.as_view()),

]