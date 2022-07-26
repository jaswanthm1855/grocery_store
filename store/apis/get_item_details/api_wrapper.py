from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from store.interactors.get_item_details_interactor import GetItemDetailsInteractor
from store.storages.storage_implementation import StorageImplementation


class GetItemDetailsAPI(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        item_id = kwargs['id']

        storage = StorageImplementation()
        interactor = GetItemDetailsInteractor(storage=storage)
        response = interactor.get_item_details_wrapper(item_id=item_id)

        return response
