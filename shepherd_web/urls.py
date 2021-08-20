"""shepherd_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

import debug_toolbar

from web import views as site_views

urlpatterns = i18n_patterns(
    path("", site_views.index, name="main_page"),
    path("admin/", admin.site.urls),
    path("activity/", include("activity.urls")),
    path("accounts/", include("user.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("equipment/", include("equipment.urls")),
    path("farm/", include("farm.urls")),
    path("feedback/", site_views.feedback, name="feedback"),
    path("inventory/", include("inventory.urls")),
    path("locations/", include("field.urls")),
    path("plan/", include("plan.urls")),
    path("settings/", site_views.settings, name="settings"),
    path("subscription/", include("subscription.urls")),
    path("tasks/", include("task.urls")),
    path("work_orders/", include("work_order.urls")),
)

urlpatterns += staticfiles_urlpatterns()

urlpatterns += [
    path('martor/', include('martor.urls')),
]

urlpatterns += [
    path("__debug__/", include(debug_toolbar.urls)),
]
