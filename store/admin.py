from django.contrib import admin

from store import models


admin.site.register(models.Category)
admin.site.register(models.Item)
admin.site.register(models.ItemVariants)
admin.site.register(models.Review)
admin.site.register(models.Rating)
admin.site.register(models.Cart)
admin.site.register(models.Order)
admin.site.register(models.OrderItems)
