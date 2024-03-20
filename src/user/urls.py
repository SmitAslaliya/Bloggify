from django.urls import path
from .views import UserCreateView,UserLoginView,UserLogoutView,UserChangePassword

urlpatterns = [
    path('create-user',UserCreateView.as_view()),
    path('login',UserLoginView.as_view()),
    path('logout',UserLogoutView.as_view()),
    path('change-password',UserChangePassword.as_view()),
    
]
