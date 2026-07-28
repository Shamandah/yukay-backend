from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="menu_items",
    )

    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)

    description = models.TextField()

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )

    image = models.ImageField(
        upload_to="menu/",
        blank=True,
        null=True,
    )

    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)

    preparation_time = models.PositiveIntegerField(
        default=15,
        help_text="Preparation time in minutes",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Create your models here.
