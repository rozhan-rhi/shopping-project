from rest_framework import serializers
from users.models import User
from django.contrib.auth.hashers import make_password
from dotenv import load_dotenv
import os
load_dotenv()
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","name","email","phone","password","is_active"]
        extra_kwargs={
            "password":{"write_only":True}
        }

    def create(self, validated_data):
        password=validated_data.pop("password",None)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(make_password(password))
        instance.save()
        return instance

    def validate(self, data):
        phone_number = str(data["phone"])
        password=data["password"]

        phone_pattern = re.compile(os.getenv("PHONE_REGEX"))

        if not phone_pattern.match(phone_number):
            raise serializers.ValidationError({"error":"enter valid phone number"})

        if len(password) < 8:
            raise serializers.ValidationError({"error":"password should be at least 8 characters"})

        return data

