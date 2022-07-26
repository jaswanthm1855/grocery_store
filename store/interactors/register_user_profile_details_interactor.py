from typing import Dict

from store.interactors.storage_interface import StorageInterface


class RegisterUserprofileDetailsInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def register_user_profile_details_wrapper(self, user_profile_details: Dict):
        self.register_user_profile_details(user_profile_details)

    def register_user_profile_details(self, user_profile_details: Dict):
        self.storage.register_user_profile_details(user_profile_details)
