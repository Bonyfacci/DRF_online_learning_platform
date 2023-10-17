import stripe

from config.settings import STRIPE_SECRET_KEY


def create_a_payment_intent(object):
    stripe.api_key = STRIPE_SECRET_KEY

    # Тестовая цена - 20 usd
    price = 2000

    starter_subscription = stripe.Product.create(
        name=object.title,
    )

    starter_subscription_price = stripe.Price.create(
        unit_amount=price,
        currency="usd",
        recurring={"interval": "month"},
        product=starter_subscription['id'],
    )

    pay_link = stripe.PaymentLink.create(
        line_items=[
            {
                "price": starter_subscription_price.id,
                "quantity": 1,
            },
        ],
    )

    return pay_link['url']
