from django.contrib.auth import get_user_model
from django.db import models

from store.constants.enums import RatingChoices


User = get_user_model()


class UserProfileDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio_link = models.CharField(max_length=100, blank=True, null=True)
    profile_pic = models.CharField(max_length=100, blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)


class Item(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey('store.Category', on_delete=models.CASCADE)


class ItemVariants(models.Model):
    item = models.ForeignKey('store.Item', on_delete=models.CASCADE)
    variant = models.CharField(max_length=10)
    price = models.IntegerField()
    available_quantity = models.IntegerField()

    class Meta:
        unique_together = [('item', 'variant')]


class Review(models.Model):
    item = models.ForeignKey('store.Item', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)


class Rating(models.Model):
    item = models.ForeignKey('store.Item', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.CharField(max_length=1, choices=RatingChoices.choices())


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_variant = models.ForeignKey('store.ItemVariants', on_delete=models.CASCADE, related_name="cart_item_variant")
    quantity = models.IntegerField()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.IntegerField()


class OrderItems(models.Model):
    order = models.ForeignKey('store.Order', on_delete=models.CASCADE)
    item_variant = models.ForeignKey('store.ItemVariants', on_delete=models.CASCADE, related_name="order_item_variant")
    quantity = models.IntegerField()
