import json
from typing import List, Dict

from django.http import HttpResponse

from store.custom_exceptions import ItemDoesNotExistException
from store.interactors.storage_interface import StorageInterface


class GetItemDetailsInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_item_details_wrapper(self, item_id: int):
        try:
            item_details = self.get_item_details(item_id)
            response_dict = {"item_details": item_details}
            status = 200
        except ItemDoesNotExistException:
            response_dict = {"message": "Item does not exists"}
            status = 404

        response = json.dumps(response_dict)
        return HttpResponse(content=response, status=status)

    def get_item_details(self, item_id: int):

        item = self.storage.get_item_details(item_id)
        item_variants = self.storage.get_item_variants(item_id)
        ratings = self.storage.get_item_ratings(item_id)
        average_rating = self._get_item_average_rating(ratings)
        reviews = self.storage.get_item_reviews(item_id)

        # preparing response
        item_related_details = {}
        item_related_details.update(item)
        item_related_details["variants"] = item_variants
        item_related_details["ratings"] = ratings
        item_related_details["reviews"] = reviews
        item_related_details["average_rating"] = average_rating

        return item_related_details

    def get_items_details(self, item_ids: List[int]) -> List[Dict]:
        from collections import defaultdict

        items_details = self.storage.get_items_details(item_ids)

        items_variants = self.storage.get_items_variants(item_ids)
        item_id_wise_variants_details = defaultdict(list)
        for item_variant in items_variants:
            item_id_wise_variants_details[
                item_variant["item_id"]
            ].append({
                "variant": item_variant["variant"],
                "price": item_variant["price"],
                "available_quantity": item_variant["available_quantity"]
            })

        for item in items_details:
            item["variants"] = item_id_wise_variants_details[item["item_id"]]

        return items_details

    @staticmethod
    def _get_item_average_rating(ratings: List) -> float:
        no_of_ratings = len(ratings)
        total_ratings_value = 0
        for rating in ratings:
            total_ratings_value += int(rating["rating"])

        total_ratings_value = total_ratings_value/no_of_ratings

        return total_ratings_value
