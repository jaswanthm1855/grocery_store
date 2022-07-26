import abc
from typing import Dict, List


class StorageInterface:

    @abc.abstractmethod
    def get_item_details(self, item_id: int) -> Dict:
        pass

    @abc.abstractmethod
    def get_item_ratings(self, item_id: int) -> List[Dict]:
        pass

    @abc.abstractmethod
    def get_item_reviews(self, item_id: int) -> List[Dict]:
        pass

    @abc.abstractmethod
    def get_item_variants(self, item_id: int) -> List:
        pass

    @abc.abstractmethod
    def get_items_details_for_item_id_variant_details(
            self, item_id_variant_details: List[Dict]) -> List:
        pass

    @abc.abstractmethod
    def create_order(self, user_id: int, total_price: int) -> int:
        pass

    @abc.abstractmethod
    def create_order_items(self, order_id: int, order_items_details: List):
        pass

    @abc.abstractmethod
    def decrease_item_variants_quantity(self, order_items_details: List):
        pass

    @abc.abstractmethod
    def get_user_orders_details(self, user_id: int) -> List:
        pass

    @abc.abstractmethod
    def get_order_items_details(self, order_ids: List[int]) -> List:
        pass

    @abc.abstractmethod
    def get_item_variants_details(self, item_variant_ids: List[int]) -> List:
        pass

    @abc.abstractmethod
    def get_items_details(self, item_ids: List[int]) -> List:
        pass

    @abc.abstractmethod
    def get_items_variants(self, item_ids: List[int]) -> List:
        pass

    @abc.abstractmethod
    def get_item_ids_matching_search_query(
            self, sub_strs_of_search_query: List[str]) -> List:
        pass

    @abc.abstractmethod
    def get_cart_items_details(self, user_id: int) -> List:
        pass

    @abc.abstractmethod
    def get_item_ids_in_price_range(self, from_price: int, to_price: int) -> List:
        pass

    @abc.abstractmethod
    def get_item_ids_in_ratings(self, ratings: List) -> List:
        pass

    @abc.abstractmethod
    def remove_all_items_from_cart(self, user_id: int):
        pass

    @abc.abstractmethod
    def register_user_profile_details(self, user_profile_details: Dict):
        pass
