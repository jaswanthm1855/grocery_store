import json
from typing import List, Dict

from django.http import HttpResponse

from store.interactors.storage_interface import StorageInterface


class GetCartItemsInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_cart_items_wrapper(self, user_id: int):
        cart_items = self.get_cart_items(user_id)
        response = json.dumps({"cart_items": cart_items})
        status = 200

        return HttpResponse(content=response, status=status)

    def get_cart_items(self, user_id: int) -> List[Dict]:
        from collections import defaultdict

        cart_items_details = self.storage.get_cart_items_details(user_id=user_id)
        item_variant_id_wise_quantity_chose_in_cart = {
            cart_item["item_variant_id"]: cart_item["quantity"]
            for cart_item in cart_items_details
        }

        item_variant_ids = list(item_variant_id_wise_quantity_chose_in_cart.keys())
        item_variants_details = \
            self.storage.get_item_variants_details(item_variant_ids)

        item_ids = [
            item_variant["item_id"] for item_variant in item_variants_details
        ]
        items_details = self.storage.get_items_details(item_ids)

        item_id_wise_variants_details = defaultdict(list)
        for item_variant in item_variants_details:
            item_id_wise_variants_details[
                item_variant["item_id"]
            ].append({
                "variant": item_variant["variant"],
                "price": item_variant["price"],
                "quantity_chosen": item_variant_id_wise_quantity_chose_in_cart[
                    item_variant["item_variant_id"]],
                "available_quantity": item_variant["available_quantity"]
            })

        for item in items_details:
            item["variants"] = item_id_wise_variants_details[item["item_id"]]

        return items_details
