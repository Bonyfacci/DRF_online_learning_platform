import stripe
from app_school.tasks import send_mail_about_update

from app_school.models import Course, Subscription
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


def check_subscription(course: Course) -> None:
    subscriptions = Subscription.objects.filter(course=course)
    if subscriptions:
        for subscription in subscriptions:
            send_mail_about_update.delay(subscription.user.email, subscription.course.title)
