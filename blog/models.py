from django.db import models
from users.models import User
from ckeditor.fields import RichTextField
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=25)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(unique=True)
    thumbnail = models.ImageField(upload_to="blog/posts/")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = RichTextField(max_length=5000)
    total_views = models.PositiveIntegerField(blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.thumbnail:
            self.compress_thumbnail()

    def compress_thumbnail(self):
        img = Image.open(self.thumbnail.path)
        if img.mode != "RGB":
            img = img.convert("RGB")
        img.save(self.thumbnail.path, quality=60)

    def __str__(self):
        return self.title


class Bookmark(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.title
