from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from employee.models import EmployeeDirectory
from employee.permissions import EmployeeDirectoryUpdatePermission
from employee.serializers import EmployeeListViewSerializer, EmployeeDetailViewSerializer, EmployeeCreateViewSerializer, \
    EmployeeSerializer


class EmployeeListView(ListAPIView):
    queryset = EmployeeDirectory.objects.all()
    serializer_class = EmployeeListViewSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ('job_title',)
    search_fields = ('first_name', 'last_name', 'job_title', 'employment_date', 'salary', 'boss')


class EmployeeDetailView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = EmployeeDirectory.objects.all()
    serializer_class = EmployeeDetailViewSerializer


class EmployeeCreateView(CreateAPIView):
    queryset = EmployeeDirectory.objects.all()
    serializer_class = EmployeeCreateViewSerializer


class EmployeeUpdateDeleteView(UpdateAPIView):
    permission_classes = [EmployeeDirectoryUpdatePermission, permissions.IsAuthenticated]
    queryset = EmployeeDirectory.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDeleteView(DestroyAPIView):
    queryset = EmployeeDirectory.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [EmployeeDirectoryUpdatePermission, permissions.IsAuthenticated]
