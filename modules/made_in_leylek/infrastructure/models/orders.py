# modules/made_in_leylek/infrastructure/models/orders.py
from django.db import models
from django.contrib.postgres.fields import JSONField
from modules.made_in_leylek.domain.entities import OrderStatus

class Order(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    user_id = models.UUIDField()
    items = JSONField()
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    status = models.CharField(
        max_length=20,
        choices=[(tag.value, tag.name) for tag in OrderStatus],
        default=OrderStatus.PENDING.value
    )
    delivery_info = JSONField()
    tracking_number = models.CharField(max_length=50, null=True, blank=True)
    buyer_comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['status']),
            models.Index(fields=['created_at'])
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.status}"