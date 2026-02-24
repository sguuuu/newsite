from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdmin(BasePermission):
    """Только администраторы."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsTeacher(BasePermission):
    """Только педагоги."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'teacher'


class IsParticipant(BasePermission):
    """Только участники."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'participant'


class IsJury(BasePermission):
    """Только жюри."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'jury'


class IsAdminOrReadOnly(BasePermission):
    """Чтение — для всех; запись — только для администраторов."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.role == 'admin'


class IsAdminOrTeacher(BasePermission):
    """Только администраторы и педагоги."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ('admin', 'teacher')
        )


class IsOwnerOrAdmin(BasePermission):
    """Владелец объекта или администратор."""
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        # Объект может иметь поле `user`, `participant`, или быть самим пользователем
        owner = getattr(obj, 'user', None) or getattr(obj, 'participant', None) or obj
        return owner == request.user
