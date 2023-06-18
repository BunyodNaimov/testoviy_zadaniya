from django.urls import path

from employee.views import EmployeeListView, EmployeeDetailView, EmployeeCreateView, EmployeeUpdateDeleteView, \
    EmployeeDeleteView

app_name = 'employee'

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee-list'),
    path('<int:pk>', EmployeeDetailView.as_view(), name='employee-detail'),
    path('create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('<int:pk>/update/', EmployeeUpdateDeleteView.as_view(), name='employee-update'),
    path('<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),

]