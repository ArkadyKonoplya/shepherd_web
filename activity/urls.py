from django.urls import path

from .views import farm_custom_activity_list, custom_activity_detail, custom_activity_create

urlpatterns = [path("farm_activities/", farm_custom_activity_list, name="farm_activities"),
               path("<str:pk>/", custom_activity_detail, name="custom_activity_detail"),
               path("new", custom_activity_create, name="custom_activity_create"),]
