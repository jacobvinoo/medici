from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Student

from course import serializers


class StudentViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage students in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer

    def get_queryset(self):
        """Return objects for the current authenticated users only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')
