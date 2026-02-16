from django.urls import path
from .views import *

urlpatterns = [
    path('client-types/', get_client_types, name='client_types'),
    path('visits/', visit_list, name='visit_list'),
    path('visits/<int:pk>/', visit_detail, name='visit_detail'),
    path('clients/', client_list, name='client_list'),
    path('clients/<str:code>/', client_detail, name='client_detail'),
]