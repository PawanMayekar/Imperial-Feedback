from django.shortcuts import render

from .forms import (
    ClubFeedbackForm,
    HotelFeedbackForm,
    RestaurantFeedbackForm,
    SpaFeedbackForm,
)


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
        "form_intro_kicker": "Member Feedback",
        "form_intro_title": "Share your Experience",
        "footer_note": "",
        "submit_with_chevron": True,
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
        "kicker": "Spa experience",
        "heading": "Spa Feedback Form",
        "description": "Tell us about your visit—your satisfaction, treatment, and therapist help us improve every detail.",
        "hero_points": [
            "Name and date of service",
            "Overall satisfaction and reasons for your visit",
            "Massage pressure, therapist care, and follow-up preferences",
        ],
        "form_intro_kicker": "",
        "form_intro_title": "Spa Feedback Form",
        "footer_note": "",
        "submit_with_chevron": False,
        "submit_label": "SEND",
        "form_class": SpaFeedbackForm,
        "sections": [
            {
                "title": "",
                "show_name_legend": True,
                "layout": "fields",
                "fields": ["first_name", "last_name", "service_date"],
                "columns": 2,
            },
            {
                "title": "Your experience",
                "layout": "choices",
                "fields": [
                    "overall_spa_experience",
                    "therapy_reasons",
                    "massage_pressure",
                    "concerns_addressed",
                ],
            },
            {
                "title": "Before you go",
                "layout": "choices",
                "fields": ["therapist_rating", "follow_up"],
            },
        ],
    },
    "hotel": {
        "title": "Hotel Feedback Form",
        "kicker": "Hospitality",
        "heading": "Hotel Feedback Form",
        "description": "We value your feedback! Please take a moment to let us know about your recent stay.",
        "hero_points": [
            "Guest name, room, and stay dates",
            "Service quality: front desk, housekeeping, and dining",
            "Room, amenities, pool & fitness—and your comments",
        ],
        "form_intro_kicker": "",
        "form_intro_title": "Hotel Feedback Form",
        "footer_note": "Thank you for your time! We look forward to welcoming you back.",
        "submit_with_chevron": True,
        "submit_label": "Submit hotel feedback",
        "form_class": HotelFeedbackForm,
        "sections": [
            {
                "title": "Guest information",
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
    "restaurant": {
        "title": "Resident Dining Feedback",
        "kicker": "Dining experience",
        "heading": "Resident Dining Feedback Form",
        "description": "Tell us about your meal—your honest feedback helps our team perfect every visit.",
        "hero_points": [
            "Date, outlet, and resident name (optional)",
            "Rate quality, service, ambience, and value (1–5)",
            "Overall satisfaction, recommendation, and comments",
        ],
        "form_intro_kicker": "Imperial Club",
        "form_intro_title": "Resident Dining Feedback Form",
        "footer_note": "Thank you! We appreciate your feedback.",
        "submit_with_chevron": True,
        "submit_label": "Submit dining feedback",
        "form_class": RestaurantFeedbackForm,
        "sections": [
            {
                "title": "Visit details",
                "layout": "fields",
                "fields": ["visit_date", "resident_name"],
                "columns": 2,
            },
            {
                "title": "Outlet visited",
                "layout": "choices",
                "fields": ["outlet_visited"],
            },
            {
                "title": "Please rate your experience (1 = Poor, 5 = Excellent)",
                "layout": "choices",
                "score": True,
                "columns": 2,
                "fields": [
                    "food_quality",
                    "food_presentation",
                    "service_quality",
                    "staff_courtesy",
                    "ambience",
                    "decor",
                    "music",
                    "cleanliness",
                    "value_for_money",
                ],
            },
            {
                "title": "Overall",
                "layout": "choices",
                "fields": ["overall_satisfaction", "recommend", "comments"],
            },
        ],
    },
}


def dashboard(request):
    """Dashboard cards mirror `imperial-club-feedback/src/App.tsx` DashboardCard copy and icons."""
    card_meta = {
        "club": {
            "title": "Club Visit",
            "kicker": "Fitness & Social",
            "description": "Service, facility ratings, and overall club experience.",
            "icon": "activity",
        },
        "spa": {
            "title": "Spa Treatment",
            "kicker": "Wellness & Care",
            "description": "Therapist quality, treatment comfort, and wellness feedback.",
            "icon": "waves",
        },
        "hotel": {
            "title": "Hotel Stay",
            "kicker": "Hospitality",
            "description": "Room cleanliness, hospitality staff, and amenities review.",
            "icon": "hotel",
        },
        "restaurant": {
            "title": "Resident Dining",
            "kicker": "Dining & Outlets",
            "description": "Outlet, food, service, ambience, and overall satisfaction.",
            "icon": "utensils",
        },
    }
    form_cards = []
    for slug, config in FORM_PAGES.items():
        meta = card_meta[slug]
        form_cards.append(
            {
                "slug": slug,
                "title": meta["title"],
                "description": meta["description"],
                "kicker": meta["kicker"],
                "icon": meta["icon"],
            }
        )
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
