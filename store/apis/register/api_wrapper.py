from rest_framework import generics
from rest_framework.response import Response
from store.apis.register.serializer import RegisterSerializer, UserSerializer


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        self._register_user_profile_details(request, user)

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "User Created Successfully. Now perform Login to get your token",
        })

    @staticmethod
    def _register_user_profile_details(request, user):
        from store.interactors.register_user_profile_details_interactor \
            import RegisterUserprofileDetailsInteractor
        from store.storages.storage_implementation import StorageImplementation

        request_data = request.data
        bio_link = request_data["bio_link"]
        profile_pic = request_data["profile_pic"]
        user_profile_details = {
            "user": user,
            "bio_link": bio_link,
            "profile_pic": profile_pic
        }

        storage = StorageImplementation()
        interactor = RegisterUserprofileDetailsInteractor(storage=storage)
        interactor.register_user_profile_details(user_profile_details)
