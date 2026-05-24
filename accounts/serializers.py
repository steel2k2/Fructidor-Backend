from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers

from .models import Person, Role

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name', 'description')


class PersonSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True, required=False)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Person
        fields = ('id', 'dni', 'nombres', 'apellidos', 'fecha_nacimiento', 'user', 'user_id', 'role')


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), required=False, allow_null=True)
    person = PersonSerializer(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'role', 'person')

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Las contraseñas no coinciden.'})

        user = User(username=data.get('username', ''), email=data.get('email', ''))
        validate_password(data['password'], user=user)
        return data

    def create(self, validated_data):
        with transaction.atomic():
            validated_data.pop('password2', None)
            role = validated_data.pop('role', None)
            person_data = validated_data.pop('person', None)
            password = validated_data.pop('password')
            
            user = User(**validated_data)
            user.set_password(password)
            user.save()

            if person_data:
                Person.objects.create(user=user, role=role, **person_data)

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
    role = serializers.SerializerMethodField()
    person = PersonSerializer(source='persona', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active', 'role', 'person')

    def get_role(self, obj):
        if hasattr(obj, 'persona') and obj.persona.role:
            return obj.persona.role.name
        return None
