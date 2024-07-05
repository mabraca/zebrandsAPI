from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint


# Create your models here.


class Product(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    visit_count = models.IntegerField(default=0)
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Channel(models.Model):
    name = models.CharField(max_length=255)

class ChannelProducts(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['channel', 'product'], name='channel_products_unique')
        ]

    def __str__(self):
        return self.channel.name + " " + self.product.name + " " + str(self.price)


class Log(models.Model):
    ADD = 1
    UPDATED = 2
    Status = (
        (ADD, "Added product"),
        (UPDATED, "Updated product")
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.IntegerField(choices=Status)
    changes = models.TextField(blank=True)

    def __str__(self):

        return f"{self.get_action_display()} by {self.user.username} on {self.timestamp}"

