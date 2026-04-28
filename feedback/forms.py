from django import forms


RATING_CHOICES = [
    ("excellent", "Excellent"),
    ("good", "Good"),
    ("average", "Average"),
    ("poor", "Poor"),
]

SATISFACTION_CHOICES = [
    ("very_satisfied", "Very satisfied"),
    ("satisfied", "Satisfied"),
    ("neutral", "Neutral"),
    ("unsatisfied", "Unsatisfied"),
    ("very_unsatisfied", "Very unsatisfied"),
]

YES_NO_CHOICES = [
    ("yes", "Yes"),
    ("no", "No"),
]


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
    THERAPY_REASON_CHOICES = [
        ("stress_relief", "Stress relief"),
        ("pain_management", "Pain management"),
        ("injury", "Recovery or injury support"),
        ("relaxation", "Relax and me-time"),
    ]

    PRESSURE_CHOICES = [
        ("too_light", "Too light"),
        ("too_hard", "Too hard"),
        ("perfect", "Perfect"),
    ]

    guest_name = forms.CharField(
        label="Guest name",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Jane Smith"}),
    )
    service_date = forms.DateField(
        label="Date of service",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    overall_spa_experience = forms.ChoiceField(
        label="How satisfied were you with your overall spa experience?",
        choices=SATISFACTION_CHOICES,
        widget=forms.RadioSelect,
    )
    therapy_reasons = forms.MultipleChoiceField(
        label="Which reasons most closely reflect why you booked the service?",
        choices=THERAPY_REASON_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    massage_pressure = forms.ChoiceField(
        label="How was the pressure during the treatment?",
        choices=PRESSURE_CHOICES,
        widget=forms.RadioSelect,
    )
    concerns_addressed = forms.ChoiceField(
        label="Did your therapist address your areas of concern?",
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect,
    )
    therapist_rating = forms.TypedChoiceField(
        label="How would you rate your therapist overall?",
        choices=[(5, "5"), (4, "4"), (3, "3"), (2, "2"), (1, "1")],
        coerce=int,
        widget=forms.RadioSelect,
    )
    follow_up = forms.ChoiceField(
        label="May we contact you about your feedback?",
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect,
    )
    comments = forms.CharField(
        label="Additional comments",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Tell us what you enjoyed or where we can improve.",
                "rows": 5,
            }
        ),
        required=False,
    )


class HotelFeedbackForm(forms.Form):
    guest_name = forms.CharField(
        label="Guest name",
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Jane Smith"}),
    )
    room_number = forms.CharField(
        label="Room number",
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": "205"}),
    )
    check_in = forms.DateField(
        label="Check-in date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    check_out = forms.DateField(
        label="Check-out date",
        widget=forms.DateInput(attrs={"type": "date"}),
    )
    front_desk = forms.ChoiceField(
        label="Front desk assistance",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
    )
    housekeeping = forms.ChoiceField(
        label="Housekeeping service",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
    )
    restaurant = forms.ChoiceField(
        label="Restaurant or dining experience",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )
    cleanliness = forms.ChoiceField(
        label="Room cleanliness",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
    )
    amenities = forms.ChoiceField(
        label="Amenities",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
    )
    pool_fitness = forms.ChoiceField(
        label="Pool or fitness center",
        choices=RATING_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )
    comments = forms.CharField(
        label="Additional comments",
        widget=forms.Textarea(
            attrs={
                "placeholder": "Please tell us anything specific we could improve.",
                "rows": 5,
            }
        ),
        required=False,
    )
