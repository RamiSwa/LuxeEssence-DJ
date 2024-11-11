from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="category_images/", blank=True, null=True)  # Optional image field

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]  # Display categories alphabetically by name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:category", args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, related_name="products", on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to="products/%Y/%m/%d/")
    is_active = models.BooleanField(default=True)  # Used to hide or show products
    is_featured = models.BooleanField(default=False)  # Highlight featured products
    related_products = models.ManyToManyField("self", blank=True)  # Related products field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]  # Order by newest products first

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("shop:product_detail", args=[self.slug])

    def get_price(self):
        return self.discount_price if self.discount_price else self.price  # Returns discount price if available
