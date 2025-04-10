# modules/made_in_leylek/infrastructure/models/products.py
from django.db import models
from django.contrib.postgres.fields import ArrayField
from modules.made_in_leylek.domain.entities import ProductCategory

class Product(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    seller_id = models.UUIDField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=[(tag.value, tag.name) for tag in ProductCategory]
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    quantity = models.PositiveIntegerField(default=0)
    production_date = models.DateTimeField()
    expiration_date = models.DateTimeField(null=True, blank=True)
    tags = ArrayField(
        models.CharField(max_length=50),
        size=10,
        default=list,
        blank=True
    )
    rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['seller_id']),
            models.Index(fields=['category']),
            models.Index(fields=['created_at'])
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.category})"