from rest_framework import serializers
from .models import AccountModel
from django.contrib.auth import settings

class AccountSerializers(serializers.ModelSerializer):
    account_number = serializers.CharField()
    class Meta:
        model = AccountModel
        fields = ['account_number']







