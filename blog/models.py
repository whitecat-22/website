from django.db import models

# Create your models here.
from accounts.models import CustomUser
from django.utils import timezone

from markdownx.models import MarkdownxFiled


class Post(models.Model):
    """ブログ モデル"""
    user = models.ForeignKey(CustomUser, verbose_name='User', on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(verbose_name='Title',max_length=255)
    content = MarkdownxField(verbose_name='Content' help_text='Markdown形式で記述してください。')
    created_at = models.DateTimeField(verbose_name='Created_at', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated_at', auto_now=True)
    published_at = models.DateTimeField(verbose_name='Published_at', blank=True, null=True)
    is_public = models.BooleanField(verbose_name='Is_public', default=False)
#    image = models.ImageField(upload_to='post_images/', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Blog'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.is_public and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ContentImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    content_image = models.ImageField(upload_to='post_content_images/')


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=50)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

    def approve(self):
        self.approved = True
        self.save()

    def __str__(self):
        return self.text


#class Reply(models.Model):
#    comment = models.ForeignKey(
#        Comment, on_delete=models.CASCADE, related_name='replies')
#    author = models.CharField(max_length=50)
#    text = models.TextField()
#    timestamp = models.DateTimeField(auto_now_add=True)
#    approved = models.BooleanField(default=False)
#
#    def approve(self):
#        self.approved = True
#        self.save()
#
#    def __str__(self):
#        return self.text
