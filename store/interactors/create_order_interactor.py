import json
from typing import List, Dict

from django.http import HttpResponse

from store.interactors.storage_interface import StorageInterface


class CreateOrderInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def create_order_wrapper(
            self, user_id: int, items_details: List[Dict]):
        order_id = self.create_order(
            user_id=user_id, items_details=items_details)
        response = json.dumps({"order_id": order_id})
        status = 201

        return HttpResponse(content=response, status=status)

    def create_order(self, user_id: int, items_details: List[Dict]):
        """

        :param user_id:
        :param items_details: [
            {
                "item_id": int,
                "variant": str,
                "quantity": int
            }
        ]
        :return:
        """
        item_variants_details = self.storage.get_items_details_for_item_id_variant_details(items_details)
        item_id_variant_wise_item_variant_details = {
            (each["item_id"], each["variant"]): each
            for each in item_variants_details
        }
        order_total_price = 0
        order_items_details = []
        for each in items_details:
            item_variant_details = item_id_variant_wise_item_variant_details[
                (each["item_id"], each["variant"])]

            # Assumption, only available quantity is given to user even though he asks for more
            if each["quantity"] > item_variant_details["available_quantity"]:
                each["quantity"] = item_variant_details["available_quantity"]

            # Only items that are added with more than quantity 0 will be considered
            if each["quantity"] > 0:
                order_total_price += each["quantity"] * item_variant_details["price"]
                order_items_details.append({
                    "item_variant_id": item_variant_details["item_variant_id"],
                    "quantity": each["quantity"]
                })

        order_id = self.storage.create_order(
            user_id=user_id, total_price=order_total_price)
        self.storage.create_order_items(
            order_id=order_id, order_items_details=order_items_details)
        self.storage.decrease_item_variants_quantity(order_items_details)

        # Assuming that user will buy after adding to cart only
        self.storage.remove_all_items_from_cart(user_id)

        return order_id
