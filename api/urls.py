from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, get_client_types, visit_list, visit_detail

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('client-types/', get_client_types, name='client_types'),
    path('visits/', visit_list, name='visit_list'),
    path('visits/<int:pk>/', visit_detail, name='visit_detail'),
]