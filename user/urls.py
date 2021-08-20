from django.urls import path

from .views import (
    ActivateAccount,
    ConfirmEmailView,
    ProfileView,
    SignupView,
    worker_list,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("profile/<str:pk>/", ProfileView.as_view(), name="profile"),
    path("email-confirm/<uidb64>/", ConfirmEmailView.as_view(), name="email-confirm"),
    path("activate/<uidb64>/<token>/", ActivateAccount.as_view(), name="activate"),
    path("workers/", worker_list, name="worker_list"),
]
