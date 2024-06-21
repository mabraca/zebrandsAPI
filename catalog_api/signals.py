from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Product, Log

"""
Method log_product_changes automatically logs changes to a Product instance whenever it is created or updated.
This method will be called every time a Product instance is saved.
"""


@receiver(post_save, sender=Product)
def log_product_changes(sender, instance, created, **kwargs):
    if created:
        action = Log.ADD
        action_text = f"Added: {instance.name}, Price: {instance.price}, Brand: {instance.brand}, Active: {instance.is_active}"
    else:
        action = Log.UPDATED
        action_text = f"Updated: {instance.name}, Price: {instance.price}, Brand: {instance.brand}, Active: {instance.is_active}"

    Log.objects.create(
        product=instance,
        user=instance.modified_by,
        action=action,
        changes=action_text,
    )
