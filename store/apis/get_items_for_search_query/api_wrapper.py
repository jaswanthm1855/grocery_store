from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from store.interactors.get_items_for_search_query_interactor import GetItemsForSearchQueryInteractor
from store.storages.storage_implementation import StorageImplementation


class GetItemsForSearchQueryAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        request_data = request.data
        search_query = request_data["search_query"]
        price_range = request_data["price_range"]
        ratings = request_data["ratings"]

        storage = StorageImplementation()
        interactor = GetItemsForSearchQueryInteractor(storage=storage)
        response = interactor.get_items_for_search_query_wrapper(
            search_query=search_query, price_range=price_range, ratings=ratings)

        return response
