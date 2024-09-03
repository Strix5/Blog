from django.db import models
from django.utils import timezone

# Default model for Users in project
from django.contrib.auth.models import User
from django.shortcuts import reverse

# from taggit.mangers import TaggableManger


# Manager to get all posts from model POSTS where status is PUBLISHED
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Posts.Status.PUBLISHED)


class Posts(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=128)
    slug = models.SlugField(max_length=250, unique_for_date='published')
    text = models.TextField(max_length=2048)
    # Connect model POSTS to auth.models.USER
    author = models.ForeignKey(to=User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')

    # Created time and status
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    # If you want to have (Default manager) and (Special-oriented manager) working at the same time
    # then you must add 'objects = models.Manager()'
    objects = models.Manager()  # Default Manager
    published_objects = PublishedManager()  # Special oriented Manager. Collects all posts that have been published
    # tags = TaggableManger()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.published.year,
                                                 self.published.month,
                                                 self.published.day,
                                                 self.slug,])

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-published',)
        indexes = [
            models.Index(fields=['-published',])
        ]


class Comment(models.Model):
    post = models.ForeignKey(to=Posts, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f'''Comment by {self.name} on {self.post}'''
