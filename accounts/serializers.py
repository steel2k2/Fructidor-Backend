from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers

from .models import Person, Cargo, Nivel, Departamento

User = get_user_model()


class NivelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nivel
        fields = ('id', 'nombre', 'valor')

class DepartamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departamento
        fields = '__all__'

class CargoSerializer(serializers.ModelSerializer):
    nivel_detalle = NivelSerializer(source='nivel', read_only=True)
    nivel = serializers.PrimaryKeyRelatedField(queryset=Nivel.objects.all())
    superior_nombre = serializers.ReadOnlyField(source='superior.nombre')
    departamento_nombre = serializers.ReadOnlyField(source='departamento.nombre')

    class Meta:
        model = Cargo
        fields = ('id', 'nombre', 'descripcion', 'nivel', 'nivel_detalle', 'departamento', 'departamento_nombre', 'superior', 'superior_nombre')

class PersonSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True, required=False)
    cargo = serializers.PrimaryKeyRelatedField(queryset=Cargo.objects.all(), required=False, allow_null=True)
    departamento = serializers.PrimaryKeyRelatedField(queryset=Departamento.objects.all(), required=False, allow_null=True)
    superior_nombre = serializers.ReadOnlyField(source='superior.nombre_completo')

    class Meta:
        model = Person
        fields = (
            'id', 'dni', 'nombres', 'apellido_paterno', 'apellido_materno', 
            'fecha_nacimiento', 'user', 'user_id', 'cargo', 'departamento', 
            'superior', 'superior_nombre'
        )

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    cargo = serializers.PrimaryKeyRelatedField(queryset=Cargo.objects.all(), required=False, allow_null=True)
    person = PersonSerializer(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'cargo', 'person')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Las contraseñas no coinciden.'})

        user = User(username=data.get('username', ''), email=data.get('email', ''))
        validate_password(data['password'], user=user)
        return data

    def create(self, validated_data):
        with transaction.atomic():
            validated_data.pop('password2', None)
            cargo = validated_data.pop('cargo', None)
            person_data = validated_data.pop('person', None)
            password = validated_data.pop('password')
            
            # Evitar duplicidad si el cargo viene dentro de person_data
            if person_data and 'cargo' in person_data:
                person_data.pop('cargo')

            user = User(**validated_data)
            user.set_password(password)
            user.save()

            if person_data:
                Person.objects.create(user=user, cargo=cargo, **person_data)

            return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError({'new_password': 'Las contraseñas no coinciden.'})
        validate_password(attrs['new_password'], user=self.context['request'].user)
        return attrs


class UserSerializer(serializers.ModelSerializer):
    cargo = serializers.SerializerMethodField()
    person = PersonSerializer(source='persona', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_active', 'cargo', 'person')

    def get_cargo(self, obj):
        if hasattr(obj, 'persona') and obj.persona.cargo:
            cargo = obj.persona.cargo
            return {
                'id': cargo.id,
                'nombre': cargo.nombre,
                'nivel': cargo.nivel.valor if cargo.nivel else 0,
                'nivel_nombre': cargo.nivel.nombre if cargo.nivel else "Sin nivel"
            }
        return None
