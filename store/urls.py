from django.urls import path, include
from store.apis import RegisterAPI
urlpatterns = [
      path('api/register', RegisterAPI.as_view()),
]
