from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from store.interactors.get_cart_items_interactor import GetCartItemsInteractor
from store.storages.storage_implementation import StorageImplementation


class GetCartItemsAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        storage = StorageImplementation()
        interactor = GetCartItemsInteractor(storage=storage)
        response = interactor.get_cart_items_wrapper(user_id=user_id)

        return response
