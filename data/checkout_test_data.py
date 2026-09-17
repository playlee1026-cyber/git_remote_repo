# data/checkout_test_data.py

PAYMENT_VALID_DATA = {
    "name_on_card": "QA Tester",
    "card_number": "1234567890123456",
    "cvc": "311",
    "expiration_month": "12",
    "expiration_year": "2030"
}

CHECKOUT_FLOW_TEST_DATA = {
    "target_product_name": "Blue Top",
    "order_comment": "This is an automated test order for TC16.",
    "payment_details": PAYMENT_VALID_DATA
}