from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator



class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.IntegerField()

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('This username is been taken')
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('This email is already registered to an account')
        if len(str(data['password'])) != 6:
            raise serializers.ValidationError('Password should be six digits long')
        return data
    
    def create(self, validated_data):
        user = User.objects.create(username = validated_data['username'], email=validated_data['email'])
        user.set_password(str(validated_data['password']))
        user.save()
        return validated_data



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.IntegerField()

    def validate(self, data):
        user = User.objects.filter(email=data['email']).exists()
        if not user:
            raise serializers.ValidationError('This email is not registered')
        if user:
            user = User.objects.get(email=data['email'])
            if not user.check_password(data['password']):
                raise serializers.ValidationError('Incorrect password')
        return data