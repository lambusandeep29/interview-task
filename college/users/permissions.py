from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from .models import User


class IsAdmin(IsAuthenticated):
    message = 'User Is Not Of A Type Admin'

    def has_permission(self, request: Request, view: View) -> bool:
        if super().has_permission(request, view):
            return request.user.user_type == User.USER_TYPE_ADMIN

        return False


class IsTeacher(IsAuthenticated):
    message = 'User Is Not Of A Type Teacher'

    def has_permission(self, request: Request, view: View) -> bool:
        if super().has_permission(request, view):
            return request.user.user_type >= User.USER_TYPE_TEACHER

        return False


class IsStudent(IsAuthenticated):
    message = 'User Is Not Of A Type Student'

    def has_permission(self, request: Request, view: View) -> bool:
        if super().has_permission(request, view):
            return request.user.user_type >= User.USER_TYPE_STUDENT

        return False
