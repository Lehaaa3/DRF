import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_API_KEY


def get_stripe_price(amount):
    stripe_price = stripe.Price.create(
        currency="usd",
        unit_amount=amount * 100,
        product_data={"name": "Payment"},
    )
    return stripe_price


def get_stripe_session(price):
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.get("url")
