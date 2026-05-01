# Django's built-in admin is not used by this project — we expose a custom
# reviewer console at /admin/ backed by `feedback.UserMaster`. See
# `feedback/admin_views.py` for the real admin implementation.
#
# This file is intentionally empty so Django's admin autodiscover (run when
# `django.contrib.admin` is installed) finds nothing to register.
