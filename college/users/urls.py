from django.urls import path
from .views import LoginAPIView, RefreshTokenApiView, GetUserFromEmail, ResetPassword, UserListCreateApiView, \
    ListStudentsApiView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('refresh/', RefreshTokenApiView.as_view(), name='token_refresh'),
    path('forgot_password/<str:email>/', GetUserFromEmail.as_view()),
    path('reset_password/', ResetPassword.as_view()),
    path('all-users/', UserListCreateApiView.as_view()),
    path('students/', ListStudentsApiView.as_view()),
]
