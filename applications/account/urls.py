from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    # path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('activate/<str:activation_code>/', views.ActivationView.as_view()),
]
