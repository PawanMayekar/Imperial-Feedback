from django import forms


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


class ClubFeedbackForm(forms.Form):
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

    member_name = forms.CharField(
        label="Member name",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Jane Smith", "autocomplete": "name"}),
    )
    membership_id = forms.CharField(
        label="Membership ID",
        max_length=40,
        widget=forms.TextInput(attrs={"placeholder": "CLB-2048"}),
    )
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
        label="Additional comments",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Share any suggestions, concerns, or highlights from your visit.",
                "rows": 6,
            }
        ),
        required=False,
    )


class SpaFeedbackForm(forms.Form):
    """Field wording aligned with WhatsApp spa feedback reference (mobile form)."""

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

    first_name = forms.CharField(
        label="First",
        max_length=80,
        widget=forms.TextInput(attrs={"placeholder": "First", "autocomplete": "given-name"}),
    )
    last_name = forms.CharField(
        label="Last",
        max_length=80,
        widget=forms.TextInput(attrs={"placeholder": "Last", "autocomplete": "family-name"}),
    )
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
        label="Would you like us to contact you for any further suggestions or questions regarding your answers?",
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect,
    )


class HotelFeedbackForm(forms.Form):
    """Wording aligned with WhatsApp hotel feedback reference (Seaside-style layout)."""

    guest_name = forms.CharField(
        label="Guest Name",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "", "autocomplete": "name"}),
    )
    room_number = forms.CharField(
        label="Room #",
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": ""}),
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
        label="Please let us know if there's anything specific we could improve.",
        widget=forms.Textarea(
            attrs={
                "placeholder": "",
                "rows": 5,
            }
        ),
        required=False,
    )


class RestaurantFeedbackForm(forms.Form):
    """Imperial Club resident dining feedback (per Resident_Feedback_Form.pdf)."""

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

    visit_date = forms.DateField(
        label="Date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    resident_name = forms.CharField(
        label="Resident name (optional)",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Optional", "autocomplete": "name"}),
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
        label="Additional comments / suggestions",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Tell us what you loved or what we can improve.",
                "rows": 5,
            }
        ),
        required=False,
    )
