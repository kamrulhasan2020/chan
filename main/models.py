from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings


def unique_slugify(instance, slug):
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug + get_random_string(length=5)
    return unique_slug


class User(AbstractUser):
    bio = models.CharField(max_length=200)
    profile_picture = models.ImageField(upload_to='profile_pictures')
    joined = models.DateTimeField(auto_now_add=True)


class Board(models.Model):
    board_name = models.CharField(max_length=100, unique=True)
    banner = models.ImageField(upload_to='banners')

    def __str__(self):
        return self.board_name

    def get_absolute_url(self):
        return reverse('main:board', args=[self.board_name])


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to='post_images')
    slug = models.SlugField(unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('main:post', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.title))
        super().save(*args, **kwargs)


class Comment(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='comment_images')
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    class Meta:
        ordering = ['-created']



