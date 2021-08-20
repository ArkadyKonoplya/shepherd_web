from django.urls import path

from .views import farm_dashboard, farm_details, ProfileView

urlpatterns = [path("dashboard", farm_dashboard, name="farm_dashboard"),
               path("my_farm", farm_details, name="farm_details"),
               path("profile/<str:pk>/", ProfileView.as_view(), name="farm_profile"),
               path("profile/", ProfileView.as_view(), name="farm_profile_default")]
