from django import template
from django.db.models import Count, Q
from ..models import Posts

register = template.Library()


@register.simple_tag()
def total_posts():
    return Posts.published_objects.count()


@register.inclusion_tag('blog/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Posts.published_objects.order_by('-published')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    return Posts.published_objects.annotate(total_comments=Count('comments', filter=Q(comments__active=True)))\
            .exclude(total_comments=0).order_by('-published')[:count]
