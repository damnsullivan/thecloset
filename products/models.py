from django.db import models
from django.urls import reverse
from django.conf import settings
from storages.backends.gcloud import GoogleCloudStorage
from django.utils.text import slugify


gcs = GoogleCloudStorage()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

    def get_absolute_url(self):
        return reverse('category_detail', args=[self.slug])

class Product(models.Model):
    SIZES = [
        ('XS', 'PP'),
        ('S', 'P'),
        ('M', 'M'),
        ('L', 'G'),
        ('XL', 'GG')
    ]

    COLORS = [
        ('Red', 'Vermelho'),
        ('Blue', 'Azul'),
        ('Green', 'Verde'),
        ('Black', 'Preto'),
        ('White', 'Branco'),
        ('Yellow', 'Amarelo')
    ]

    STARS = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars')
    ]

    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('U', 'Unissex'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(storage=gcs, upload_to='products_images/', blank=True, null=True)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    size = models.CharField(max_length=2, choices=SIZES, default='M')
    color = models.CharField(max_length=10, choices=COLORS, default='Black')
    rating = models.PositiveSmallIntegerField(choices=STARS, default=3)
    brand = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default='U')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    @property
    def is_in_stock(self):
        return self.stock > 0

    @property
    def is_available(self):
        return self.available and self.is_in_stock

    def get_image_url(self):
        if self.image:
            return self.image.url
        return settings.STATIC_URL + 'images/no_image.png'  # Fallback imagem

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
