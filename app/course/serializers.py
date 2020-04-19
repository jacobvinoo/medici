from rest_framework import serializers

from core.models import Student


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for student objects"""

    class Meta:
        model = Student
        fields = ('id', 'name')
        read_only_fields = ('id',)
