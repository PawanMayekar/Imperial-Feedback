"""
Self-contained admin panel for reviewing submitted feedback.

Routes (mounted under /admin/ in sdcorp/urls.py):
- GET  /admin/                       -> dashboard (or redirect to login)
- GET  /admin/login/                 -> login page
- POST /admin/login/                 -> authenticate
- GET  /admin/logout/                -> logout
- GET  /admin/<slug>/                -> list rows for a feedback table
- GET  /admin/<slug>/download/       -> CSV download for a feedback table

Auth uses the local UserMaster model (separate from django.contrib.auth)
and Django's session middleware to keep things simple.
"""

from __future__ import annotations

import csv
from functools import wraps

from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_http_methods

from .models import FEEDBACK_MODELS, UserMaster


SESSION_KEY = "user_master_id"

FEEDBACK_LABELS = {
    "club": "Club Feedback",
    "spa": "Spa Feedback",
    "hotel": "Hotel Feedback",
    "restaurant": "Resident Dining Feedback",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _current_user(request):
    user_id = request.session.get(SESSION_KEY)
    if not user_id:
        return None
    try:
        return UserMaster.objects.get(pk=user_id, is_active=True)
    except UserMaster.DoesNotExist:
        request.session.flush()
        return None


def admin_required(view_func):
    """Redirect unauthenticated requests to the admin login page."""

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user = _current_user(request)
        if user is None:
            return redirect(f"{reverse('admin-login')}?next={request.path}")
        request.user_master = user
        return view_func(request, *args, **kwargs)

    return _wrapped


def _resolve_model(slug):
    model = FEEDBACK_MODELS.get(slug)
    if model is None:
        raise Http404("Unknown feedback table.")
    return model


def _row_for(obj, fields):
    """Build a display-friendly row, expanding choice labels and JSON lists."""
    row = []
    for field in fields:
        value = getattr(obj, field.name)
        if field.choices:
            value = getattr(obj, f"get_{field.name}_display")()
        elif isinstance(value, list):
            value = ", ".join(str(item) for item in value) if value else ""
        elif value is None:
            value = ""
        row.append(value)
    return row


# ---------------------------------------------------------------------------
# Auth views
# ---------------------------------------------------------------------------


@never_cache
@require_http_methods(["GET", "POST"])
def admin_login(request):
    if _current_user(request) is not None:
        return redirect("admin-dashboard")

    error = None
    next_url = request.GET.get("next") or request.POST.get("next") or ""

    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""

        if not username or not password:
            error = "Please provide both username and password."
        else:
            user = UserMaster.objects.filter(username=username, is_active=True).first()
            if user is None or not user.check_password(password):
                error = "Invalid username or password."
            else:
                request.session[SESSION_KEY] = user.pk
                request.session.set_expiry(60 * 60 * 8)  # 8 hours
                user.touch_login()
                if next_url and next_url.startswith("/admin"):
                    return redirect(next_url)
                return redirect("admin-dashboard")

    return render(
        request,
        "feedback/admin/login.html",
        {"error": error, "next": next_url, "username": request.POST.get("username", "")},
    )


@never_cache
def admin_logout(request):
    request.session.flush()
    return redirect("admin-login")


# ---------------------------------------------------------------------------
# Reviewer views
# ---------------------------------------------------------------------------


@never_cache
@admin_required
def admin_dashboard(request):
    cards = []
    for slug, model in FEEDBACK_MODELS.items():
        cards.append(
            {
                "slug": slug,
                "title": FEEDBACK_LABELS.get(slug, slug.title()),
                "count": model.objects.count(),
                "latest": model.objects.values_list("submitted_at", flat=True).first(),
            }
        )

    return render(
        request,
        "feedback/admin/dashboard.html",
        {
            "cards": cards,
            "user_master": request.user_master,
        },
    )


@never_cache
@admin_required
def admin_feedback_list(request, slug):
    model = _resolve_model(slug)
    fields = list(model._meta.fields)
    qs = model.objects.all()
    total = qs.count()
    rows = [{"obj": obj, "values": _row_for(obj, fields)} for obj in qs[:500]]

    return render(
        request,
        "feedback/admin/list.html",
        {
            "slug": slug,
            "title": FEEDBACK_LABELS.get(slug, slug.title()),
            "headers": [f.verbose_name.title() for f in fields],
            "rows": rows,
            "total": total,
            "showing": len(rows),
            "user_master": request.user_master,
        },
    )


@never_cache
@admin_required
def admin_feedback_download(request, slug):
    model = _resolve_model(slug)
    fields = list(model._meta.fields)

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = (
        f'attachment; filename="{slug}_feedback.csv"'
    )
    # UTF-8 BOM so Excel opens accented characters (e.g., Décor) correctly.
    response.write("\ufeff")

    writer = csv.writer(response)
    writer.writerow([field.verbose_name.title() for field in fields])

    for obj in model.objects.all().iterator():
        writer.writerow(_row_for(obj, fields))

    return response
