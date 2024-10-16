from django.conf import settings
from django.db import models
from django.utils import timezone


class PublishedManager(models.Manager):
    """Custom manager to filter published posts."""
    def get_queryset(self):
        return super().get_queryset().filter(status=BlogPost.Status.PUBLISHED)



class Category(models.Model):
    """Model for blog post categories."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name



class BlogPost(models.Model):
    """Main Post model for blog posts."""
    
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish', unique=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts'
    )
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='posts',
        null=True, 
        blank=True
    )
    featured_image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    
    # SEO fields
    meta_title = models.CharField(max_length=150, null=True, blank=True)
    meta_description = models.TextField(max_length=300, null=True, blank=True)
    excerpt = models.TextField(max_length=500, null=True, blank=True)


    # Managers
    objects = models.Manager()  # The default manager.
    published = PublishedManager()  # Custom manager to get published posts.


    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title



