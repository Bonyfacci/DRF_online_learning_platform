from rest_framework import serializers

from app_school.serializers.payments import PaymentsSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentsSerializer(source='user', many=True)

    class Meta:
        model = User
        # fields = '__all__'
        fields = ('id', 'email', 'city', 'is_superuser', 'payments')
