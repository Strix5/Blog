from django.contrib.sitemaps import Sitemap
from .models import Posts


class PostsSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Posts.published_objects.all()

    def lastmod(self, obj):
        return obj.updated
