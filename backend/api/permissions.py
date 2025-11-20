from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission
from .models import CustomUser

class IsAdminQuizzesPermission(BasePermission):
    """
    Permite acesso se o usuário for admin (para quizzes).
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False
        
        customuser = get_object_or_404(CustomUser, user=user)
        
        return customuser.tipo_usuario == 'admin'

