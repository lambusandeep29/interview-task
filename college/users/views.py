from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from .permissions import IsAdmin, IsStudent, IsTeacher

# Create your views here.
from .models import User
from .serializers import UserLoginSerializer, UserRefreshTokenSerializer, UserSerializer, \
    ResetPasswordSerializer, AddUserSerializer, ListStudentSerializer


class LoginAPIView(TokenViewBase):
    serializer_class = UserLoginSerializer


class RefreshTokenApiView(TokenViewBase):
    serializer_class = UserRefreshTokenSerializer


class GetUserFromEmail(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = []

    def get_queryset(self):
        return User.objects.filter(email=self.kwargs['email'])

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        if not serializer.data:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResetPassword(generics.CreateAPIView):
    serializer_class = ResetPasswordSerializer
    queryset = User.objects.all()
    permission_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({}, status=status.HTTP_201_CREATED)


class UserListCreateApiView(generics.ListCreateAPIView):
    serializer_class = AddUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAdmin | IsTeacher]


class ListStudentsApiView(generics.ListAPIView):
    serializer_class = ListStudentSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return User.objects.filter(user_type=User.USER_TYPE_STUDENT)



