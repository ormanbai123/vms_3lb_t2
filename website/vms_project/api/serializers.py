from rest_framework import serializers
from vms_app.models import CustomUser, Driver, Task


class CustomUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def create(self, validated_data):
        pass

    def validate(self, data):
        username = data['username']
        password = data['password']

        lUser = CustomUser.objects.filter(username=username, password=password,
                                          user_type=CustomUser.DRIVER).last()
        if not lUser:
            raise serializers.ValidationError("User does not exist")

        lDriver = Driver.objects.get(profile=lUser)

        data['id'] = lUser.id
        data['email'] = lUser.email
        data['first_name'] = lUser.first_name
        data['last_name'] = lUser.last_name
        data['user_type'] = CustomUser.DRIVER
        data['government_id'] = lDriver.government_id
        data['driving_license_code'] = lDriver.driving_license_code
        data['phone_number'] = lDriver.phone_number
        return data

    def update(self, instance, validated_data):
        pass


class DriverSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    profile = serializers.CharField(read_only=True)
    government_id = serializers.CharField()
    driving_license_code = serializers.CharField()
    phone_number = serializers.CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.government_id = validated_data.get('government_id', instance.government_id)
        instance.save()
        return instance