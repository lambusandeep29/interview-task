from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from .models import User


class UserLoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        super().validate(attrs)

        data = dict()
        data['email'] = self.user.email
        data['user_type'] = self.user.user_type
        data['user_type_display'] = self.user.get_user_type_display()
        data['refresh_token'] = self.user.get_refresh_token()
        data['access_token'] = self.user.get_access_token()

        return data


class UserRefreshTokenSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['refresh_token'] = data['refresh']
        data['access_token'] = data['access']
        del data['access']
        del data['refresh']
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    class Meta:
        fields = ['email', 'new_password', 'confirm_password']

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise ValidationError({
                'passwords': 'Passwords do not match',
            })
        return attrs

    def create(self, validated_data):
        user_instance = User.objects.get(email=validated_data['email'])
        user_instance.set_password(validated_data['new_password'])
        user_instance.save()
        return user_instance


class AddUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class ListStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password',)
