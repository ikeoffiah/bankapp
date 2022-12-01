from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    class Meta:
        model = User
        fields = ('email','first_name','last_name', 'password','password2')


    def validate(self, attrs):
        password = attrs.get('password',None)
        password2 = attrs.get('password2',None)
        email = attrs.get('email',None)

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")

        if password != password2:
            raise serializers.ValidationError("Password and Confirm Password needs to match")
        return attrs


    def create(self, validated_data):

        user = User.objects.create_user(
            email=validated_data['email'],
            first_name= validated_data['first_name'],
            last_name = validated_data['last_name'],
            password=validated_data['password']
        )

        user.save()
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, max_length=100)
    token = serializers.CharField(read_only=True, max_length=100)

    class Meta:
        model= User
        fields = ['email','password','token']


    def validate(self, attrs):
        email = attrs.get('email',None)
        password = attrs.get('password',None)


        req = self.context['request']

        if not authenticate(email=email,password=password):
            raise serializers.ValidationError('Email or Password is Invalid')

        user = User.objects.get(email=email)

        login(req,user)

        return attrs

