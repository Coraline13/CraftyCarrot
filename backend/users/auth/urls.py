from django.urls import path

from .views import (
    ChangePasswordAPIView, DeleteAccountAPIView, LoginAPIView, LogoutAPIView, RegisterAPIView,
    RequestPasswordResetAPIView, ResetPasswordAPIView
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    # path('confirm-email/', ConfirmEmailAPIView.as_view()),
    path('request-password-reset/', RequestPasswordResetAPIView.as_view()),
    path('reset-password/', ResetPasswordAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('change-password/', ChangePasswordAPIView.as_view()),
    path('logout/', LogoutAPIView.as_view()),
    path('delete-account/', DeleteAccountAPIView.as_view()),
]
