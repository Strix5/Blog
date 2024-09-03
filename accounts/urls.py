from django.urls import path
from django.contrib.auth.views import LogoutView

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.NewLoginView.as_view(redirect_authenticated_user=True, template_name='registration/login.html')
         , name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='users-profile'),
    path('change_password/', views.ChangePasswordView.as_view(), name='change_password'),
]
