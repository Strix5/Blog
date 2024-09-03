# from django.core.paginator import Paginator
# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.views import SpectacularAPIView

from blog.models import Posts
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly


class StandardSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class PostsAPIView(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['author']
    search_fields = ['text', 'title', 'author__username']

    pagination_class = StandardSetPagination


class PostDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer

    permission_classes = (IsAuthorOrReadOnly, )


class UserPostListApiView(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        user = self.kwargs['id']
        return Posts.objects.filter(author=user)


class MySpectacularAPIView(LoginRequiredMixin, SpectacularAPIView):
    login_url = '/accounts/login/?next=/blog_api/schema/'

