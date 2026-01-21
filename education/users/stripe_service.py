import requests
from django.conf import settings
from .models import Payment
from education_app.models import Course

API_BASE = "https://api.stripe.com/v1"
HEADERS = {
    "Authorization": f"Bearer {settings.STRIPE_SECRET_KEY}",
}


def create_stripe_product(course_id: int) -> dict:
    course = Course.objects.get(id=course_id)
    data = {
        "name": course.title,
        "description": course.description
    }
    resp = requests.post(f"{API_BASE}/products", headers=HEADERS, data=data)
    return resp.json()


def create_stripe_price(course_id: int, payment_id: int) -> dict:
    # Получаем курс и платеж
    course = Course.objects.get(id=course_id)
    payment = Payment.objects.get(id=payment_id)

    # Формируем данные для создания цены в Stripe
    data = {
        "product": payment.stripe_product_id,
        "unit_amount": int(course.price * 100),
        "currency": "rub",
    }

    resp = requests.post(f"{API_BASE}/prices", headers=HEADERS, json=data)
    return resp.json()


def create_checkout_session(payment: Payment, success_url: str, cancel_url: str) -> dict:
    data = {
        "payment_method_types": ["card"],
        "customer_email": payment.user.email,  # Используем email пользователя
        "line_items": [{
            "price": payment.stripe_price_id,
            "quantity": 1
        }],
        "mode": "payment",
        "success_url": success_url,
        "cancel_url": cancel_url
    }
    resp = requests.post(f"{API_BASE}/checkout/sessions", headers=HEADERS, json=data)
    session_data = resp.json()
    return session_data


def init_stripe_payment(payment: Payment, success_url: str, cancel_url: str) -> dict:
    # Проверяем, есть ли у платежа stripe_product_id
    if not payment.stripe_product_id:
        # Создаем товар в Stripe
        product_resp = create_stripe_product(payment.course_id)
        payment.stripe_product_id = product_resp.get("id")
        payment.save()

    # Проверяем, есть ли у платежа stripe_price_id
    if not payment.stripe_price_id:
        # Создаем цену в Stripe (используем ID продукта)
        price_resp = create_stripe_price(payment.course_id, payment.id)
        payment.stripe_price_id = price_resp.get("id")
        payment.save()

    session = create_checkout_session(payment, success_url, cancel_url)

    payment.stripe_session_id = session.get("id")
    payment.checkout_url = session.get("url")
    payment.save()

    return session