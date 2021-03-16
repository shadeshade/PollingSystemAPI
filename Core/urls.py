from django.urls import path
from . import views

app_name = "Core"
urlpatterns = [
    path('', views.UserViewSet.as_view({'get': 'list'})),
]