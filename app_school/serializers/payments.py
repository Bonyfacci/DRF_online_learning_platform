from rest_framework import serializers

from app_school.models import Payments
from app_school.services import create_a_payment_intent


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'


class PaymentRetrieveSerializer(serializers.ModelSerializer):
    payment_link = serializers.SerializerMethodField()

    class Meta:
        model = Payments
        fields = '__all__'

    @staticmethod
    def get_payment_link(instance):
        return create_a_payment_intent(instance)


class PaymentSuccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = ['amount', 'is_paid']
