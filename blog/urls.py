from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.published_post, name='published_post'),
    path('tag/<slug:slug_tag>/', views.published_post, name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),
    path('search/', views.post_search, name='post_search')
]
