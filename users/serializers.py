from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'password', 'name', 'email', 'phone_number', 'photo']

    def create(self, validated_data):
        user = User.objects.create_user(email=validated_data['email'], phone_number=validated_data['phone_number'], password=validated_data['password'])
        return user

class TokenObtainPairSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get('phone_number')
        password = attrs.get('password')

        user = User.objects.filter(phone_number=phone_number).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return data
        raise serializers.ValidationError("Phone number or password is incorrect.")

