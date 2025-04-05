from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('handicrafts', 'Ремесла'),
        ('agriculture', 'Сельхозпродукция'),
        ('textiles', 'Текстиль'),
        ('food', 'Продукты питания')
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_auction = models.BooleanField(default=False)
    auction_end = models.DateTimeField(null=True, blank=True)
    main_image = models.ImageField(upload_to='products/')


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')