from rest_framework import serializers

from drf_app.models import Payment
from users.models import User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(source='user_payment', many=True, read_only=True)

    class Meta:
        model = User
        fields = '__all__'
