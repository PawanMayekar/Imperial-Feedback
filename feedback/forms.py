from django import forms
from django.core.validators import RegexValidator


RATING_CHOICES = [
    ("excellent", "Excellent"),
    ("good", "Good"),
    ("average", "Average"),
    ("poor", "Poor"),
]

SATISFACTION_CHOICES = [
    ("very_satisfied", "Very Satisfied"),
    ("satisfied", "Satisfied"),
    ("neutral", "Neutral"),
    ("unsatisfied", "Unsatisfied"),
    ("very_unsatisfied", "Very Unsatisfied"),
]

YES_NO_CHOICES = [
    ("yes", "Yes"),
    ("no", "No"),
]

SCORE_1_TO_5 = [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]

VISIT_REASON_CHOICES = [
    ("fitness", "Fitness and wellness"),
    ("dining", "Dining and lounge"),
    ("events", "Events and social gatherings"),
    ("family", "Family time"),
    ("business", "Business meetings"),
]

COMFORT_CHOICES = [
    ("too_light", "Too light"),
    ("too_strong", "Too strong"),
    ("perfect", "Just right"),
]

THERAPY_REASON_CHOICES = [
    ("stress_relief", "Stress Relief"),
    ("pain_management", "Pain Management"),
    ("injury", "Injury"),
    ("relaxation", "Relax & Me-Time"),
]

PRESSURE_CHOICES = [
    ("too_light", "Too light"),
    ("too_hard", "Too hard"),
    ("perfect", "Perfect"),
]

OUTLET_CHOICES = [
    ("deli_cafe", "Deli Café"),
    ("aqua", "Aqua"),
    ("on_nine", "On Nine"),
    ("whisky_mist", "Whisky Mist"),
]

RECOMMEND_CHOICES = [
    ("yes", "Yes"),
    ("no", "No"),
    ("maybe", "Maybe"),
]

ROOM_NUMBER_CHOICES = [
    ("902", "902"),
    ("903", "903"),
    ("904", "904"),
    ("905", "905"),
    ("906", "906"),
    ("907", "907"),
    ("908", "908"),
    ("909", "909"),
]

# Permits +, -, spaces, parentheses, and 7–20 digits/separators.
PHONE_REGEX_VALIDATOR = RegexValidator(
    regex=r"^[0-9+\-\s()]{7,20}$",
    message="Enter a valid phone number (digits, +, -, spaces, parentheses).",
)


class ContactFeedbackBase(forms.Form):
    """
    Mandatory resident-contact fields shared by every feedback form.

    All four feedback forms (Club / Spa / Hotel / Restaurant) inherit from
    this base so the contact triplet is enforced consistently.
    """

    name = forms.CharField(
        label="Name",
        max_length=120,
        widget=forms.TextInput(
            attrs={"placeholder": "Your full name", "autocomplete": "name"}
        ),
    )
    flat_no = forms.CharField(
        label="Flat No.",
        max_length=20,
        widget=forms.TextInput(
            attrs={"placeholder": "e.g. 902", "autocomplete": "off"}
        ),
    )
    phone_number = forms.CharField(
        label="Phone Number",
        max_length=20,
        validators=[PHONE_REGEX_VALIDATOR],
        widget=forms.TextInput(
            attrs={
                "placeholder": "+91 98765 43210",
                "type": "tel",
                "autocomplete": "tel",
                "inputmode": "tel",
            }
        ),
    )


class ClubFeedbackForm(ContactFeedbackBase):
    visit_date = forms.DateField(
        label="Date of visit",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    overall_experience = forms.ChoiceField(
        label="How satisfied were you with your overall club experience?",
        choices=SATISFACTION_CHOICES,
        widget=forms.RadioSelect,
    )
    visit_reasons = forms.MultipleChoiceField(
        label="Which reasons best reflect your visit?",
        choices=VISIT_REASON_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    staff_service = forms.ChoiceField(
        label="Front desk and staff support",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
    )
    facility_cleanliness = forms.ChoiceField(
        label="Club cleanliness",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
    )
    amenities = forms.ChoiceField(
        label="Amenities and facilities",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
    )
    dining_experience = forms.ChoiceField(
        label="Dining or lounge experience",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )
    activity_comfort = forms.ChoiceField(
        label="How was the comfort level of the activity or service you used?",
        choices=COMFORT_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )
    concerns_addressed = forms.ChoiceField(
        label="Did our team address your needs or concerns?",
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect,
    )
    recommend_rating = forms.TypedChoiceField(
        label="How likely are you to recommend the club?",
        choices=[(5, "5"), (4, "4"), (3, "3"), (2, "2"), (1, "1")],
        coerce=int,
        widget=forms.RadioSelect,
    )
    follow_up = forms.ChoiceField(
        label="May we contact you regarding your feedback?",
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect,
    )
    comments = forms.CharField(
        label="Extra remarks (optional)",
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Share any suggestions, concerns, or highlights from your visit.",
                "rows": 6,
            }
        ),
    )


class SpaFeedbackForm(ContactFeedbackBase):
    """Field wording aligned with WhatsApp spa feedback reference (mobile form)."""

    service_date = forms.DateField(
        label="Date of service",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    overall_spa_experience = forms.ChoiceField(
        label="How satisfied were you with your overall experience at our spa?",
        choices=SATISFACTION_CHOICES,
        widget=forms.RadioSelect,
    )
    therapy_reasons = forms.MultipleChoiceField(
        label="Which reason(s) most closely reflect why you seek massage therapy?",
        choices=THERAPY_REASON_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    massage_pressure = forms.ChoiceField(
        label="How was the pressure during the massage?",
        choices=PRESSURE_CHOICES,
        widget=forms.RadioSelect,
    )
    concerns_addressed = forms.ChoiceField(
        label="Did your massage therapist address your areas of concern?",
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect,
    )
    therapist_rating = forms.TypedChoiceField(
        label="How would you rate your massage therapist?",
        choices=[(5, "5"), (4, "4"), (3, "3"), (2, "2"), (1, "1")],
        coerce=int,
        widget=forms.RadioSelect,
    )
    follow_up = forms.ChoiceField(
        label="Did the therapist suggested different offerings for therapies?",
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect,
    )
    comments = forms.CharField(
        label="Extra remarks (optional)",
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Anything else you'd like us to know?",
                "rows": 5,
            }
        ),
    )


class HotelFeedbackForm(ContactFeedbackBase):
    """Wording aligned with WhatsApp hotel feedback reference (Seaside-style layout)."""

    room_number = forms.ChoiceField(
        label="Room #",
        choices=[("", "Select your room")] + ROOM_NUMBER_CHOICES,
        widget=forms.Select(attrs={"class": "js-custom-select"}),
    )
    check_in = forms.DateField(
        label="Check-in",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    check_out = forms.DateField(
        label="Check-out",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    front_desk = forms.ChoiceField(
        label="Front Desk Assistance",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
    )
    housekeeping = forms.ChoiceField(
        label="Housekeeping Service",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
    )
    restaurant = forms.ChoiceField(
        label="Restaurant/Dining Experience",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
    )
    cleanliness = forms.ChoiceField(
        label="Cleanliness",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
    )
    amenities = forms.ChoiceField(
        label="Amenities",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
    )
    pool_fitness = forms.ChoiceField(
        label="Pool/Fitness Center (if used)",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )
    comments = forms.CharField(
        label="Extra remarks (optional)",
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Please let us know if there's anything specific we could improve.",
                "rows": 5,
            }
        ),
    )


class RestaurantFeedbackForm(ContactFeedbackBase):
    """Imperial Club resident dining feedback (per Resident_Feedback_Form.pdf)."""

    visit_date = forms.DateField(
        label="Date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    outlet_visited = forms.ChoiceField(
        label="Outlet visited",
        choices=OUTLET_CHOICES,
        widget=forms.RadioSelect,
    )

    food_quality = forms.TypedChoiceField(
        label="Food Quality", choices=SCORE_1_TO_5, coerce=int, widget=forms.RadioSelect,
    )
    food_presentation = forms.TypedChoiceField(
        label="Food Presentation", choices=SCORE_1_TO_5, coerce=int, widget=forms.RadioSelect,
    )
    service_quality = forms.TypedChoiceField(
        label="Service Quality", choices=SCORE_1_TO_5, coerce=int, widget=forms.RadioSelect,
    )
    staff_courtesy = forms.TypedChoiceField(
        label="Staff Courtesy", choices=SCORE_1_TO_5, coerce=int, widget=forms.RadioSelect,
    )
    ambience = forms.TypedChoiceField(
        label="Ambience", choices=SCORE_1_TO_5, coerce=int, widget=forms.RadioSelect,
    )
    decor = forms.TypedChoiceField(
        label="Décor", choices=SCORE_1_TO_5, coerce=int, widget=forms.RadioSelect,
    )
    music = forms.TypedChoiceField(
        label="Music", choices=SCORE_1_TO_5, coerce=int, widget=forms.RadioSelect,
    )
    cleanliness = forms.TypedChoiceField(
        label="Cleanliness", choices=SCORE_1_TO_5, coerce=int, widget=forms.RadioSelect,
    )
    value_for_money = forms.TypedChoiceField(
        label="Value for Money", choices=SCORE_1_TO_5, coerce=int, widget=forms.RadioSelect,
    )

    overall_satisfaction = forms.TypedChoiceField(
        label="Overall Satisfaction (1–5)",
        choices=SCORE_1_TO_5,
        coerce=int,
        widget=forms.RadioSelect,
    )
    recommend = forms.ChoiceField(
        label="Would you recommend this outlet?",
        choices=RECOMMEND_CHOICES,
        widget=forms.RadioSelect,
    )
    comments = forms.CharField(
        label="Extra remarks (optional)",
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Tell us what you loved or what we can improve.",
                "rows": 5,
            }
        ),
    )
