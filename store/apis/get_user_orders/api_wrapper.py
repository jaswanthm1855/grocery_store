from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from store.interactors.get_user_orders_interactor import UserOrdersInteractor
from store.storages.storage_implementation import StorageImplementation


class GetUserOrdersAPI(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user_id = request.user.id

        storage = StorageImplementation()
        interactor = UserOrdersInteractor(storage=storage)
        response = interactor.get_user_orders_wrapper(user_id=user_id)

        return response
