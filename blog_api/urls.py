from django.urls import path
from . import views
from drf_spectacular.views import SpectacularRedocView, SpectacularSwaggerView

app_name = 'blog_api'

urlpatterns = [
    path('<int:pk>/', views.PostDetailAPIView.as_view(), name='api_post_detail'),
    path('', views.PostsAPIView.as_view(), name='api_post_list'),
    path('user/<int:id>/', views.UserPostListApiView.as_view(), name='api_user_post_list'),
    path('schema/', views.MySpectacularAPIView.as_view(), name='schema'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='blog_api:schema'), name='redoc'),
    path('schema/swagger_ui/', SpectacularSwaggerView.as_view(url_name='blog_api:schema'), name='swagger-ui'),
]
