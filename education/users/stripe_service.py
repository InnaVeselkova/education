import stripe
from django.conf import settings
from .models import Payment
from education_app.models import Course

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course_id: int) -> dict:
    course = Course.objects.get(id=course_id)
    product = stripe.Product.create(
        name=course.title,
        description=course.description
    )
    return product


def create_stripe_price(course_id: int, payment_id: int) -> dict:
    course = Course.objects.get(id=course_id)
    payment = Payment.objects.get(id=payment_id)

    price = stripe.Price.create(
        product=payment.stripe_product_id,
        unit_amount=int(course.price * 100),
        currency='rub',
    )
    return price


def create_checkout_session(payment: Payment, success_url: str, cancel_url: str) -> dict:
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        customer_email=payment.user.email,
        line_items=[{
            "price": payment.stripe_price_id,
            "quantity": 1
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session


def init_stripe_payment(payment: Payment, success_url: str, cancel_url: str) -> dict:
    # Создаем товар
    if not payment.stripe_product_id:
        product = create_stripe_product(payment.course_id)
        payment.stripe_product_id = product.id
        payment.save()

    # Создаем цену
    if not payment.stripe_price_id:
        price = create_stripe_price(payment.course_id, payment.id)
        payment.stripe_price_id = price.id
        payment.save()

    # Создаем сессию
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        customer_email=payment.user.email,
        line_items=[{
            "price": payment.stripe_price_id,
            "quantity": 1
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
    )

    payment.stripe_session_id = session.id
    payment.checkout_url = session.url
    payment.save()

    return {
        "id": session.id,
        "url": session.url
    }
