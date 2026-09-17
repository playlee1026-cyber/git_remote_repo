# data/product_test_data.py

SEARCH_AND_CART_TEST_DATA = {
    "search_keyword": "Top",
    "first_product_name": "Blue Top",
    "second_product_name": "Summer White Top",
    "expected_cart_details": [
        {
            "product_name": "Blue Top", 
            "price": "Rs. 500", 
            "quantity": "1", 
            "total_price": "Rs. 500"
        },
        {
            "product_name": "Summer White Top", 
            "price": "Rs. 400", 
            "quantity": "1", 
            "total_price": "Rs. 400"
        }
    ]
}