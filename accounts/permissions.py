from rest_framework import permissions

class IsManagementLevel(permissions.BasePermission):
    """
    Permite el acceso solo a usuarios con nivel de gestión:
    - Nivel Administrador (Valor 100)
    - Nivel Supervisor/Verificador (Valor 50)
    """
    def has_permission(self, request, view):
        # El usuario debe estar autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Los superusuarios de Django siempre tienen acceso total
        if request.user.is_superuser:
            return True

        # Verificamos la jerarquía a través de la relación Persona -> Cargo -> Nivel
        persona = getattr(request.user, 'persona', None)
        if persona and persona.cargo and persona.cargo.nivel:
            return persona.cargo.nivel.valor >= 50
            
        return False
