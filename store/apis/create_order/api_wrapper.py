from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from store.interactors.create_order_interactor import CreateOrderInteractor
from store.storages.storage_implementation import StorageImplementation


class CreateOrderAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args,  **kwargs):
        user_id = request.user.id
        request_data = request.data
        items_details = request_data["items_details"]

        storage = StorageImplementation()
        interactor = CreateOrderInteractor(storage=storage)
        response = interactor.create_order_wrapper(
            user_id=user_id, items_details=items_details)
        return response
