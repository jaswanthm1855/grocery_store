import json
from typing import List, Dict

from django.http import HttpResponse

from store.interactors.storage_interface import StorageInterface


class UserOrdersInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_user_orders_wrapper(self, user_id: int):
        user_orders = self.get_user_orders(user_id=user_id)

        response = json.dumps({"user_orders": user_orders})
        status = 200

        return HttpResponse(content=response, status=status)

    def get_user_orders(self, user_id: int):
        from collections import defaultdict

        orders_details = self.storage.get_user_orders_details(user_id)
        order_id_wise_total_price = {
            order["order_id"]: order["total_price"] for order in orders_details
        }
        order_ids = list(order_id_wise_total_price.keys())
        order_items = self.storage.get_order_items_details(order_ids)

        order_id_wise_order_items = defaultdict(list)
        for each in order_items:
            order_id_wise_order_items[each["order_id"]].append(each)

        item_variant_ids = [
            each["item_variant_id"] for each in order_items
        ]
        item_variants_details = self.storage.get_item_variants_details(
            item_variant_ids)
        item_variant_id_wise_details = {
            each["item_variant_id"]: each for each in item_variants_details
        }

        item_ids = [
            each["item_id"] for each in item_variants_details
        ]
        items_details = self.storage.get_items_details(item_ids)
        item_id_wise_item_details = {
            item["item_id"]: item for item in items_details
        }

        return [
            {
                "order_id": order_id,
                "total_price": order_id_wise_total_price[order_id],
                "items": self._prepare_items_details(
                    order_items=order_items,
                    item_variant_id_wise_details=item_variant_id_wise_details,
                    item_id_wise_item_details=item_id_wise_item_details
                )
            } for order_id, order_items in order_id_wise_order_items.items()
        ]

    @staticmethod
    def _prepare_items_details(
            order_items: List, item_variant_id_wise_details: Dict,
            item_id_wise_item_details: Dict) -> List:
        items_details = []
        for order_item in order_items:
            item_variant_id = order_item["item_variant_id"]
            item_variant_details = item_variant_id_wise_details[item_variant_id]

            item_id = item_variant_id_wise_details[
                order_item["item_variant_id"]]["item_id"]
            item_details = item_id_wise_item_details[item_id]

            items_details.append(
                {
                    "item_id": item_id,
                    "name": item_details["name"],
                    "price": item_variant_details["price"],
                    "quantity": order_item["quantity"],
                    "variant": item_variant_details["variant"]
                }
            )
        return items_details
