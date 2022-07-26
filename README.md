This is a GroceryStore Web Application

Supports below APIs
- Register User
- User Login
- User Logout
- Fetch Items
- Item Details
- Order
- User Orders
- Get Cart Items

steps to run the project
- Install requirements and setup the project
- Start development server
- Open jupyter notebook 'loading_data' and run it load some data
- Then access the other APIs by given API urls


Note: Links to the given API urls are kept in jupyter notebook, Please request for access if you want to go through the urls I used


- Register User
    - Request: {
        "username": str,
        "password": str,
        "email": str,
        "first_name": str,
        "last_name": str
      }
      
    - Response: {
        "user": {
            "id": int,
            ...
        }
      }
      
- Login
    - Request: {
        "username": str,
        "password": str
      }
    - Response: {
        "refresh": str,
        "access": str
      }
      
- Logout
    - Request: {
        "refresh_token": str
      }
    - Response: {}
    
- GetItemDetails
    - Request: {}
    - PathParams: {"item_id": int}
    - Response: {
        "item_details": {
            "item_id": int, 
            "name": str, 
            "description": str,
            "category_id": int, 
            "category_name": str, 
            "variants": [
                {
                    "item_variant_id": int, 
                    "item_id": int,
                    "price": int, 
                    "available_quantity": int
                }
            ],
            "ratings": [
                "user_id": str,
                "rating": int
            ],
            "reviews": [
                {
                    "user_id": str,
                    "description": str
                }
            ]
        } 
      }
      
- FetchItems
    - Request: {
        "search_query": str,
        "price_range": "from_price-to_price",
        "ratings": "[str]" 
    }
    - Response: {
        "items": [
            {
                "item_id": int,
                "name": str,
                "description": str,
                "category_id": int,
                "category_name": str,
                "variants": [
                    {
                        "variant": str, 
                        "price": int, 
                        "available_quantity": int
                    }
                ]
            }
        ]
      }
      
- Order
    - Request: {
        "items_details": [
            {
                "item_id": int,
                "variant": str,
                "quantity": int
            }
        ]
    }
    - Response: {
        "order_id": int
      }
      
- GetUserOrders
    - Request: {}
    - Response: {
        "user_orders": [
            {
                "order_id": int,
                "total_price": int,
                    "items": [
                        {
                            "item_id": int,
                            "name": str,
                            "price": int,
                            "quantity": int,
                            "variant": str
                        }
                    ]
                }
            ]
        }
      
- GetCartItems
    - Request: {}
    - Response: {
        "cart_items": [
            {
                "item_id": int,
                "name": str,
                "description": str,
                "category_id": int,
                "category_name": str,
                "variants": [
                    {
                        "variant": str,
                        "price": int,
                        "quantity_chosen": int,
                        "available_quantity": int
                    }
                ]
            }
        ]
    }
      
