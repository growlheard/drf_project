import stripe
from config import settings
from drf_app.models import Payment, Course
from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_intent(course_pay, user_id, payment_method):
    course = Course.objects.get(id=course_pay)
    amount = course.price
    user = User.objects.get(id=user_id)
    metadata = {
        'course_pay': str(course_pay),
        'user_id': str(user_id)
    }
    payment_intent = stripe.PaymentIntent.create(
        amount=int(amount * 100),
        currency='rub',
        metadata=metadata,
        payment_method=payment_method['id']
    )
    return payment_intent


def create_payment_method(payment_token):
    payment_method = stripe.PaymentMethod.create(
        type='card',
        card={
            'token': payment_token,
        }
    )
    return payment_method


def create_payment(course_pay, user_id, payment_token, amount):
    try:
        payment_method = create_payment_method(payment_token)
        payment_intent = create_payment_intent(course_pay, user_id, payment_method)
        payment = Payment.objects.create(
            course_pay_id=course_pay,
            user_id=user_id,
            payment_intent_id=payment_intent['id'],
            payment_method_id=payment_method['id'],
            amount=amount,
            payment_method=payment_method['type'],
            status=Payment.PENDING
        )
        return payment
    except Exception as e:
        raise Exception(f'Ошибка создания платежа: {str(e)}')



def retrieve_payment(payment_intent_id):
    try:
        payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        status = payment_intent['status']
        return status
    except stripe.error.StripeError as e:
        raise Exception(f'Ошибка при получении информации о платеже: {str(e)}')


def confirm_payment(payment_intent_id):
    try:
        payment_intent = stripe.PaymentIntent.confirm(payment_intent_id)
        status = payment_intent['status']
        return status
    except stripe.error.StripeError as e:
        raise Exception(f'Ошибка подтверждения платежа: {str(e)}')
