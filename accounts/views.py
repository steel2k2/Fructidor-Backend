from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Person, Role
from .serializers import (
    ChangePasswordSerializer,
    PersonSerializer,
    RegisterSerializer,
    RoleSerializer,
    UserSerializer,
)

@extend_schema(tags=['Registro y Perfil'])
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(tags=['Autenticación'])
class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]


@extend_schema(tags=['Registro y Perfil'])
class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


@extend_schema(tags=['Registro y Perfil'])
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not self.object.check_password(serializer.validated_data['old_password']):
            return Response({'old_password': 'Contraseña incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)

        self.object.set_password(serializer.validated_data['new_password'])
        self.object.save()
        return Response({'detail': 'Contraseña actualizada correctamente.'}, status=status.HTTP_200_OK)


@extend_schema(tags=['Gestión de Roles'])
class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(tags=['Gestión de Roles'])
class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(tags=['Gestión de Personas'])
class PersonListCreateView(generics.ListCreateAPIView):
    queryset = Person.objects.select_related('user', 'role').all()
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(tags=['Gestión de Personas'])
class PersonDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Person.objects.select_related('user', 'role').all()
    serializer_class = PersonSerializer
    permission_classes = [permissions.IsAdminUser]
