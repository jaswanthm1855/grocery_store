"""grocery_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from store.apis import RegisterAPI
from store.apis.get_cart_items.api_wrapper import GetCartItemsAPI
from store.apis.get_items_for_search_query.api_wrapper import GetItemsForSearchQueryAPI
from store.apis.get_user_orders.api_wrapper import GetUserOrdersAPI
from store.apis.logout.api_wrapper import LogoutAPI
from store.apis.get_item_details.api_wrapper import GetItemDetailsAPI
from store.apis.create_order.api_wrapper import CreateOrderAPI

urlpatterns = [
    path('admin/', admin.site.urls),

    path('register', RegisterAPI.as_view()),
    path('login', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path('login/refresh', jwt_views.TokenRefreshView.as_view(), name='login_refresh'),
    path('logout', LogoutAPI.as_view(), name='auth_logout'),

    path('items/', GetItemsForSearchQueryAPI.as_view()),
    path('items/<int:id>/', GetItemDetailsAPI.as_view()),

    path('order/', CreateOrderAPI.as_view()),
    path('orders_list/', GetUserOrdersAPI.as_view()),

    path('cart/', GetCartItemsAPI.as_view()),

    path('store/', include('store.urls')),



]
