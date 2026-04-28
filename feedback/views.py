from django.shortcuts import render

from .forms import ClubFeedbackForm, HotelFeedbackForm, SpaFeedbackForm


FORM_PAGES = {
    "club": {
        "title": "Club Feedback Form",
        "kicker": "Club experience",
        "heading": "Tell us about your latest club visit",
        "description": "Capture member satisfaction, services used, facility ratings, and follow-up preferences.",
        "hero_points": [
            "Member and visit details",
            "Service and facility ratings",
            "Comments and contact preference",
        ],
        "submit_label": "Submit club feedback",
        "form_class": ClubFeedbackForm,
        "sections": [
            {
                "title": "Visit details",
                "layout": "fields",
                "fields": ["member_name", "membership_id", "visit_date"],
                "columns": 2,
            },
            {
                "title": "Overall experience",
                "layout": "choices",
                "fields": ["overall_experience", "visit_reasons"],
            },
            {
                "title": "Service and facilities",
                "layout": "cards",
                "fields": ["staff_service", "facility_cleanliness", "amenities", "dining_experience"],
                "columns": 2,
            },
            {
                "title": "Final questions",
                "layout": "choices",
                "fields": ["activity_comfort", "concerns_addressed", "recommend_rating", "follow_up", "comments"],
            },
        ],
    },
    "spa": {
        "title": "Spa Feedback Form",
        "kicker": "Wellness experience",
        "heading": "Tell us about your spa treatment",
        "description": "A separate wellness form for treatment quality, therapist support, and comfort preferences.",
        "hero_points": [
            "Service date and guest details",
            "Spa satisfaction and treatment reasons",
            "Therapist rating and follow-up",
        ],
        "submit_label": "Submit spa feedback",
        "form_class": SpaFeedbackForm,
        "sections": [
            {
                "title": "Visit details",
                "layout": "fields",
                "fields": ["guest_name", "service_date"],
                "columns": 2,
            },
            {
                "title": "Experience feedback",
                "layout": "choices",
                "fields": ["overall_spa_experience", "therapy_reasons", "massage_pressure", "concerns_addressed"],
            },
            {
                "title": "Closing details",
                "layout": "choices",
                "fields": ["therapist_rating", "follow_up", "comments"],
            },
        ],
    },
    "hotel": {
        "title": "Hotel Feedback Form",
        "kicker": "Hospitality experience",
        "heading": "Tell us about your recent stay",
        "description": "A structured hospitality form for guest details, service ratings, room feedback, and comments.",
        "hero_points": [
            "Guest and stay information",
            "Service and room quality ratings",
            "Improvement comments",
        ],
        "submit_label": "Submit hotel feedback",
        "form_class": HotelFeedbackForm,
        "sections": [
            {
                "title": "Stay details",
                "layout": "fields",
                "fields": ["guest_name", "room_number", "check_in", "check_out"],
                "columns": 2,
            },
            {
                "title": "Service quality",
                "layout": "cards",
                "fields": ["front_desk", "housekeeping", "restaurant"],
                "columns": 3,
            },
            {
                "title": "Room and facilities",
                "layout": "cards",
                "fields": ["cleanliness", "amenities", "pool_fitness"],
                "columns": 3,
            },
            {
                "title": "Additional comments",
                "layout": "choices",
                "fields": ["comments"],
            },
        ],
    },
}


def dashboard(request):
    form_cards = [
        {
            "slug": slug,
            "title": config["title"],
            "description": config["description"],
            "kicker": config["kicker"],
        }
        for slug, config in FORM_PAGES.items()
    ]
    return render(request, "feedback/dashboard.html", {"form_cards": form_cards})


def form_page(request, form_type):
    config = FORM_PAGES[form_type]
    form_class = config["form_class"]
    submitted = False

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            submitted = True
            form = form_class()
    else:
        form = form_class()

    rendered_sections = []
    for section in config["sections"]:
        rendered_sections.append(
            {
                **section,
                "bound_fields": [form[field_name] for field_name in section["fields"]],
            }
        )

    context = {
        "form": form,
        "submitted": submitted,
        "form_type": form_type,
        "page": {
            **config,
            "sections": rendered_sections,
        },
    }
    return render(request, "feedback/form_page.html", context)
