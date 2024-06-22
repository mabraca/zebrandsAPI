from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from zebrands import settings
from .models import Product, Log


@receiver(post_save, sender=Product)
def send_product_update_email(sender, instance, created, **kwargs):
    admins = User.objects.filter(is_staff=True)
    update_fields = kwargs.get('update_fields') or set()

    if not created:  # Send email if product is updated, not created
        if 'visit_count' in update_fields:
            return
        subject = f'Product updated: {instance.name}'
        message = (f'The product {instance.name} has been modified with fields \n '
                   f'Price: {instance.price}, Brand: {instance.brand}, Active: {instance.is_active}')
        from_email = settings.EMAIL_HOST_USER
        for admin in admins:
            to_email = [admin.email]
            send_mail(subject, message, from_email, to_email)
