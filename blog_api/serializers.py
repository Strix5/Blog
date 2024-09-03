from rest_framework import serializers
from blog.models import Posts


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id',
                  'author',
                  'title',
                  'text',
                  'created',
                  'status',
                  'slug']
        model = Posts
