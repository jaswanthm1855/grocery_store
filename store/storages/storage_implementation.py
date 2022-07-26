from typing import Dict, List
from store import models
from store.custom_exceptions import ItemDoesNotExistException
from store.interactors.storage_interface import StorageInterface


class StorageImplementation(StorageInterface):

    @staticmethod
    def _get_user_obj_for_id(user_id: int):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user_obj = User.objects.get(id=user_id)

        return user_obj

    def get_item_details(self, item_id: int) -> Dict:
        try:
            item = models.Item.objects.get(id=item_id)
        except models.Item.DoesNotExist:
            raise ItemDoesNotExistException()
        return {
            "item_id": item.id,
            "name": item.name,
            "description": item.description,
            "category_id": item.category.id,
            "category_name": item.category.name
        }

    def get_item_ratings(self, item_id: int) -> List[Dict]:
        item_ratings = models.Rating.objects.filter(
            item_id=item_id).values("user_id", "rating")
        return list(item_ratings)

    def get_item_reviews(self, item_id: int) -> List[Dict]:
        item_reviews = models.Review.objects.filter(
            item_id=item_id).values("user_id", "description")
        return list(item_reviews)

    def get_item_variants(self, item_id: int) -> List:
        item_variants = models.ItemVariants.objects.filter(item_id=item_id)

        item_variant_details = []
        for item_variant in item_variants:
            item_variant_details.append({
                "item_variant_id": item_variant.id,
                "item_id": item_variant.item_id,
                "price": item_variant.price,
                "available_quantity": item_variant.available_quantity
            })
        return item_variant_details

    def get_items_details_for_item_id_variant_details(
            self, item_id_variant_details: List[Dict]) -> List:
        from django.db.models import Q

        q_objects = None
        for each in item_id_variant_details:
            if q_objects:
                q_objects |= Q(item_id=each["item_id"], variant=each["variant"])
            else:
                q_objects = Q(item_id=each["item_id"], variant=each["variant"])

        item_variants = models.ItemVariants.objects.filter(q_objects)
        item_variants_dicts = []
        for each in item_variants:
            item_variants_dicts.append(
                {
                    "item_variant_id": each.id,
                    "item_id": each.item_id,
                    "variant": each.variant,
                    "price": each.price,
                    "available_quantity": each.available_quantity
                }
            )
        return item_variants_dicts

    def create_order(self, user_id: int, total_price: int) -> int:
        # user_obj = self._get_user_obj_for_id(user_id)

        order = models.Order.objects.create(user_id=user_id, total_price=total_price)
        return order.id

    def create_order_items(self, order_id: int, order_items_details: List):
        order_items = [
            models.OrderItems(
                order_id=order_id,
                item_variant_id=each["item_variant_id"],
                quantity=each["quantity"]
            )for each in order_items_details
        ]
        models.OrderItems.objects.bulk_create(order_items)

    def decrease_item_variants_quantity(self, item_variant_id_quantity_details: List):
        item_variant_id_wise_quantity = {
            each["item_variant_id"]: each["quantity"]
            for each in item_variant_id_quantity_details
        }
        item_variant_ids = list(item_variant_id_wise_quantity.keys())
        item_variants = models.ItemVariants.objects.filter(id__in=item_variant_ids)
        for each in item_variants:
            quantity = item_variant_id_wise_quantity[each.id]
            each.available_quantity = each.available_quantity - quantity

        models.ItemVariants.objects.bulk_update(item_variants, ["available_quantity"])

    def get_user_orders_details(self, user_id: int) -> List:
        orders = models.Order.objects.filter(user_id=user_id)
        orders_details = [
            {
                "order_id": order.id,
                "user_id": user_id,
                "total_price": order.total_price
            } for order in orders
        ]
        return orders_details

    def get_order_items_details(self, order_ids: List[int]) -> List:
        orders_items = models.OrderItems.objects.filter(
            order_id__in=order_ids)

        orders_items_details = [
            {
                "order_id": each.order_id,
                "item_variant_id": each.item_variant_id,
                "quantity": each.quantity
            } for each in orders_items
        ]
        return orders_items_details

    def get_item_variants_details(self, item_variant_ids: List[int]) -> List:
        item_variants = models.ItemVariants.objects.filter(id__in=item_variant_ids)
        return [
            {
                "item_variant_id": each.id,
                "item_id": each.item_id,
                "variant": each.variant,
                "price": each.price,
                "available_quantity": each.available_quantity
            } for each in item_variants
        ]

    def get_items_details(self, item_ids: List[int]) -> List:
        items = models.Item.objects.filter(id__in=item_ids)
        items_details = [
            {
                "item_id": item.id,
                "name": item.name,
                "description": item.description,
                "category_id": item.category_id,
                "category_name": item.category.name
            }for item in items
        ]
        return items_details

    def get_items_variants(self, item_ids: List[int]) -> List:
        item_variants = models.ItemVariants.objects.filter(
            item_id__in=item_ids)
        items_variants_details = [
            {
                "item_id": item_variant.item_id,
                "item_variant_id": item_variant.id,
                "variant": item_variant.variant,
                "price": item_variant.price,
                "available_quantity": item_variant.available_quantity
            } for item_variant in item_variants
        ]
        return items_variants_details

    def get_item_ids_matching_search_query(
            self, sub_strs_of_search_query: List[str]) -> List:
        from django.db.models import Q

        print("sub_strs_of_search_query", sub_strs_of_search_query)

        q_objects = None
        for sub_str in sub_strs_of_search_query:
            q_object = Q(name__icontains=sub_str) | \
                       Q(category__name__icontains=sub_str)
            if q_objects:
                q_objects |= q_object
            else:
                q_objects = q_object
        if not q_objects:
            return []

        item_ids = models.Item.objects.filter(q_objects).values_list("id", flat=True)
        return list(item_ids)

    def get_cart_items_details(self, user_id: int) -> List:
        cart_objects = models.Cart.objects.filter(user_id=user_id)
        cart_details = [
            {
                "user_id": cart_obj.user_id,
                "item_variant_id": cart_obj.item_variant_id,
                "quantity": cart_obj.quantity
            } for cart_obj in cart_objects
        ]
        return cart_details

    def get_item_ids_in_price_range(self, from_price: int, to_price: int) -> List:
        item_ids_queryset = models.ItemVariants.objects.filter(
            price__gte=from_price, price__lte=to_price
        ).values_list("item_id", flat=True)

        return list(item_ids_queryset)

    def get_item_ids_in_ratings(self, ratings: List) -> List:
        item_ids_queryset = models.Rating.objects.filter(
            rating__in=ratings).values_list("item_id", flat=True)

        return list(item_ids_queryset)

    def remove_all_items_from_cart(self, user_id: int):
        models.Cart.objects.all().delete()

    def register_user_profile_details(self, user_profile_details: Dict):
        models.UserProfileDetails.objects.create(
            user=user_profile_details["user"],
            bio_link=user_profile_details["bio_link"],
            profile_pic=user_profile_details["profile_pic"],
        )
