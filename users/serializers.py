from rest_framework import serializers
from users.models import User
from dotenv import load_dotenv
load_dotenv()
from home.utils.validators import Validations
validation=Validations()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","name","email","phone","password","is_active"]
        extra_kwargs={
            "password":{"write_only":True}
        }

    def create(self, validated_data):
        # print(validated_data)
        password=validated_data.pop("password",None)
        instance=self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    # def validate(self, data):
    #     print(data)
    #     password=data["password"]
    #     if len(password) < 8:
    #         raise serializers.ValidationError({"error":"password should be at least 8 characters"})
    #
    #     validation.checkConfirm_and_pass(data["password"],data["confirmPassword"])
    #
    #     return data
