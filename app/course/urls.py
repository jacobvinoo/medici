from django.urls import path, include
from rest_framework.routers import DefaultRouter

from course import views


router = DefaultRouter()
router.register('students', views.StudentViewSet)

app_name = 'course'

urlpatterns = [
    path('', include(router.urls))
]
