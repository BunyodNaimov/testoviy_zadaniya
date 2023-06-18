from rest_framework import serializers

from employee.models import EmployeeDirectory


class EmployeeListViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDirectory
        fields = ('first_name', 'last_name', 'job_title', 'employment_date', 'salary', 'boss', 'image')


class EmployeeDetailViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDirectory
        fields = (
            'id', 'first_name', 'last_name', 'surname', 'job_title', 'employment_date', 'salary', 'boss', 'image'
        )


class EmployeeCreateViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeDirectory
        fields = ('first_name', 'last_name', 'surname', 'job_title', 'employment_date', 'salary', 'boss', 'image')

    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        surname = data.get('surname')

        if not first_name:
            raise serializers.ValidationError("First name is required.")
        if not last_name:
            raise serializers.ValidationError("Last name is required.")
        if not surname:
            raise serializers.ValidationError("Surname is required.")

        # Check if employee with given first_name, last_name, and surname already exists
        if EmployeeDirectory.objects.filter(first_name=first_name, last_name=last_name, surname=surname).exists():
            raise serializers.ValidationError("Employee with given first name, last name, and surname already exists.")

        return data


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeDirectory
        fields = (
            'id', 'first_name', 'last_name', 'surname', 'job_title', 'employment_date', 'salary', 'boss', 'image'
            )
