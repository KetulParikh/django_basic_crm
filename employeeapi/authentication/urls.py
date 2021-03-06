from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    EmployeeList,
    EmployeeView,
    UpdateEmployeeView,
    DeleteEmployeeView,
    TestView,
)


urlpatterns = [
    path("AddEmployee", RegisterView.as_view()),
    path("login", LoginView.as_view()),
    path("Employees", EmployeeList.as_view()),
    path("Employee/<id>", EmployeeView.as_view()),
    path("UpdateEmployee", UpdateEmployeeView.as_view()),
    path("DeleteEmployee", DeleteEmployeeView.as_view()),
    path("TestLearn/<str:partner_api_key>", TestView.as_view()),
]
