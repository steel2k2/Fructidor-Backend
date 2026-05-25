from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from drf_spectacular.utils import extend_schema_view, extend_schema

from .views import (
    ChangePasswordView,
    CustomTokenObtainPairView,
    PersonDetailView,
    PersonListCreateView,
    RegisterView,
    CargoDetailView,
    CargoListCreateView,
    UserProfileView,
)

token_refresh_view = extend_schema_view(
    post=extend_schema(tags=['Autenticación'], summary="Refrescar token de acceso")
)(TokenRefreshView.as_view())

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', token_refresh_view, name='token_refresh'),
    path('me/', UserProfileView.as_view(), name='user_profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('cargos/', CargoListCreateView.as_view(), name='cargo_list'),
    path('cargos/<int:pk>/', CargoDetailView.as_view(), name='cargo_detail'),
    path('persons/', PersonListCreateView.as_view(), name='person_list'),
    path('persons/<int:pk>/', PersonDetailView.as_view(), name='person_detail'),
]
