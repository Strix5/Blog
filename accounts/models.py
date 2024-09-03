from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)

    image = models.ImageField(default='default.png', upload_to='profile_images')
    inf = models.TextField()

    def __str__(self):
        return f'Account of {self.user}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        image = Image.open(self.image.path)

        if image.height > 100 or image.width > 100:
            image.thumbnail((100, 100))
            image.save(self.image.path)
