"""
URL configuration for sdcorp project.

The `/admin/` namespace below is intentionally NOT django.contrib.admin —
we expose a custom admin panel backed by `feedback.UserMaster` instead.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic import RedirectView

from feedback.admin_views import (
    admin_dashboard,
    admin_feedback_download,
    admin_feedback_list,
    admin_login,
    admin_logout,
)
from feedback.views import dashboard, form_page


urlpatterns = [
    path(
        "favicon.ico",
        RedirectView.as_view(
            url=f"{settings.MEDIA_URL}theimperialclubtransparent.png",
            permanent=False,
        ),
    ),
    # Public site
    path("", dashboard, name="home"),
    path("forms/<str:form_type>/", form_page, name="form-page"),

    # Custom admin / reviewer panel
    path("admin/", admin_dashboard, name="admin-dashboard"),
    path("admin/login/", admin_login, name="admin-login"),
    path("admin/logout/", admin_logout, name="admin-logout"),
    path("admin/<str:slug>/", admin_feedback_list, name="admin-feedback-list"),
    path(
        "admin/<str:slug>/download/",
        admin_feedback_download,
        name="admin-feedback-download",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
