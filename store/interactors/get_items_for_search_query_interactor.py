import json
from typing import List, Dict

from django.http import HttpResponse

from store.interactors.storage_interface import StorageInterface


class GetItemsForSearchQueryInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_items_for_search_query_wrapper(
            self, search_query: str, price_range: str, ratings: List):
        items = self.get_items_for_search_query(
            search_query=search_query, price_range=price_range, ratings=ratings)
        response = json.dumps({"items": items})
        status = 200

        return HttpResponse(content=response, status=status)

    def get_items_for_search_query(
            self, search_query: str, price_range: str, ratings: List) -> List:
        # Assumptions
        # search_query gets category_name or item_name
        # price_range format from_price-to_price
        # ratings - ['1', '2', '3', '4', '5']
        # sorting - didn't understand requirement
        from itertools import combinations

        sub_strs_of_search_query = [
            search_query[x: y]
            for x, y in combinations(range(len(search_query)+1), r=2)
        ]

        item_ids = []
        if search_query:
            item_ids_matching_search_query = \
                self.storage.get_item_ids_matching_search_query(sub_strs_of_search_query)
            item_ids.extend(item_ids_matching_search_query)

        if price_range:
            item_ids_in_price_range = self.get_item_ids_in_price_range(price_range)
            item_ids.extend(item_ids_in_price_range)

        if ratings:
            item_ids_in_ratings = self.storage.get_item_ids_in_ratings(ratings=ratings)
            item_ids.extend(item_ids_in_ratings)

        # TODO improve the querying and add filtering of item_ids
        #  related to sorting
        items_details = self.get_items_details(item_ids)
        return items_details

    def get_item_ids_in_price_range(self, price_range: str) -> List:
        price_ranges = list(map(int, (price_range.split('-'))))
        from_price = price_ranges[0]
        to_price = price_ranges[1]
        item_ids_in_price_range = self.storage.get_item_ids_in_price_range(
            from_price=from_price, to_price=to_price
        )
        return item_ids_in_price_range

    def get_items_details(self, item_ids: List[int]) -> List[Dict]:
        from store.interactors.get_item_details_interactor import GetItemDetailsInteractor

        interactor = GetItemDetailsInteractor(storage=self.storage)
        items_details = interactor.get_items_details(item_ids=item_ids)
        return items_details
