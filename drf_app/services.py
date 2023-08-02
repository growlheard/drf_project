import requests
import stripe
from config import settings
from drf_app.models import Payment, Course
from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY
url = 'https://api.stripe.com/v1'
headers = {'Authorization': f'Bearer {stripe.api_key}'}


def create_payment_intent(course_pay, user_id):
    course = Course.objects.get(id=course_pay)
    amount = course.price
    user = User.objects.get(id=user_id)
    data = [
        ('amount', amount * 100),
        ('currency', 'rub'),
        ('metadata[course_pay]', course_pay),
        ('metadata[user_id]', user_id)
    ]
    response = requests.post(f'{url}/payment_intents', headers=headers, data=data)
    if response.status_code != 200:
        raise Exception(f'Ошибка: {response.json()["error"]["message"]}')
    return response.json()


def create_payment_method(payment_token):
    data = {
        'type': 'card',
        'card[token]': payment_token,
    }

    response = requests.post(f'{url}/payment_methods', headers=headers, data=data)
    payment_method = response.json()

    if response.status_code != 200:
        raise Exception(f'Ошибка метода платежа: {response.status_code}')
    return payment_method


def create_payment(course_pay, user_id, payment_token, amount):
    try:
        payment_method = create_payment_method(payment_token)
        payment_intent = create_payment_intent(course_pay, user_id)
        payment = Payment(course_pay_id=course_pay, user_id=user_id,
                          payment_intent_id=payment_intent['id'], payment_method_id=payment_method['id'],
                          amount=amount, payment_method=payment_method['type'])

        payment.save()
        return payment
    except Exception as e:
        raise Exception(f'Ошибка создания платежа: {str(e)}')


def confirm_payment(payment_intent_id):
    response = requests.post(f'{url}/payment_intents/{payment_intent_id}/confirm', headers=headers)
    if response.status_code != 200:
        raise Exception(f'Ошибка подтверждения платежа: {response.json()["error"]["message"]}')
    return response.json()
