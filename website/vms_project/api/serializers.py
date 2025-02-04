from rest_framework import serializers
from vms_app.models import CustomUser, Driver, Task, DriverTask


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

        temp = DriverTask.objects.filter(driver_id=lDriver).values_list('task_id',flat=True)
        temp1 = Task.objects.filter(status='posted',id__in=temp)

        lTasks = []
        for i in temp1:
            sourceName, sourceLatLng = i.pointA.split('|')
            destName, destLatLng = i.pointB.split('|')

            sourceLatLng = sourceLatLng.replace("(","").replace(")","")
            destLatLng = destLatLng.replace("(", "").replace(")", "")

            sourceLat, sourceLng = [ float(j) for j in sourceLatLng.split(",")]
            destLat, destLng = [float(k) for k in destLatLng.split(",")]

            lTasks.append({
                'id' : i.id,
                'sourceName' : sourceName,
                'destName' : destName,
                'date' : i.dateTaken,
                'sourceLatLng': {'lat':sourceLat, 'lng':sourceLng},
                'destLatLng': {'lat':destLat, 'lng':destLng}
            })

        data['id'] = lUser.id
        data['email'] = lUser.email
        data['first_name'] = lUser.first_name
        data['last_name'] = lUser.last_name
        data['user_type'] = CustomUser.DRIVER
        data['government_id'] = lDriver.government_id
        data['driving_license_code'] = lDriver.driving_license_code
        data['phone_number'] = lDriver.phone_number

        data['tasks'] = lTasks
        return data

    def update(self, instance, validated_data):
        pass


class TaskSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    task_status = serializers.CharField()

    def create(self, validated_data):
        pass

    def validate(self, data):
        task_id = data['task_id']

        task = Task.objects.get(id=task_id)
        if task:
            data['Task'] = task
            return data
        else:
            raise serializers.ValidationError("This task does not exist")


    def update(self, instance, validated_data):
        pass