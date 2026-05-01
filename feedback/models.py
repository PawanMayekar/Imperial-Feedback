from django.contrib.auth.hashers import check_password, make_password
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from .forms import (
    COMFORT_CHOICES,
    OUTLET_CHOICES,
    PHONE_REGEX_VALIDATOR,
    PRESSURE_CHOICES,
    RATING_CHOICES,
    RECOMMEND_CHOICES,
    ROOM_NUMBER_CHOICES,
    SATISFACTION_CHOICES,
    SCORE_1_TO_5,
    YES_NO_CHOICES,
)


SCORE_VALIDATORS = [MinValueValidator(1), MaxValueValidator(5)]


class ContactFeedbackFields(models.Model):
    """
    Required at the form layer (see forms.ContactFeedbackBase). The
    `default=""` here just lets `makemigrations` backfill any pre-existing
    rows without prompting — real submissions always carry real values.
    """

    name = models.CharField(max_length=120, default="")
    flat_no = models.CharField(max_length=20, default="")
    phone_number = models.CharField(
        max_length=20, default="", validators=[PHONE_REGEX_VALIDATOR]
    )
    comments = models.TextField(blank=True, default="")

    class Meta:
        abstract = True


class UserMaster(models.Model):
    username = models.CharField(max_length=80, unique=True, db_index=True)
    full_name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(blank=True)
    password_hash = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "user_master"
        ordering = ["username"]
        verbose_name = "User (master)"
        verbose_name_plural = "Users (master)"

    def set_password(self, raw_password: str) -> None:
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password(raw_password, self.password_hash)

    def touch_login(self) -> None:
        self.last_login_at = timezone.now()
        self.save(update_fields=["last_login_at"])

    def __str__(self) -> str:
        return self.username


class TimestampedFeedback(models.Model):
    """Abstract base: every submission row is timestamped."""

    submitted_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ["-submitted_at"]


class ClubFeedback(ContactFeedbackFields, TimestampedFeedback):
    """Imperial Club — club visit feedback (table: feedback_clubfeedback)."""

    visit_date = models.DateField()

    overall_experience = models.CharField(max_length=20, choices=SATISFACTION_CHOICES)
    visit_reasons = models.JSONField(default=list, blank=True)

    staff_service = models.CharField(max_length=20, choices=RATING_CHOICES)
    facility_cleanliness = models.CharField(max_length=20, choices=RATING_CHOICES)
    amenities = models.CharField(max_length=20, choices=RATING_CHOICES)
    dining_experience = models.CharField(
        max_length=20, choices=RATING_CHOICES, blank=True, null=True
    )

    activity_comfort = models.CharField(
        max_length=20, choices=COMFORT_CHOICES, blank=True, null=True
    )
    concerns_addressed = models.CharField(max_length=10, choices=YES_NO_CHOICES)
    recommend_rating = models.PositiveSmallIntegerField(
        choices=SCORE_1_TO_5, validators=SCORE_VALIDATORS
    )

    class Meta(TimestampedFeedback.Meta):
        verbose_name = "Club feedback"
        verbose_name_plural = "Club feedback"

    def __str__(self) -> str:
        return f"Club — {self.name} ({self.visit_date})"


class SpaFeedback(ContactFeedbackFields, TimestampedFeedback):
    """Imperial Club — spa treatment feedback (table: feedback_spafeedback)."""

    service_date = models.DateField()

    overall_spa_experience = models.CharField(
        max_length=20, choices=SATISFACTION_CHOICES
    )
    therapy_reasons = models.JSONField(default=list, blank=True)
    massage_pressure = models.CharField(max_length=20, choices=PRESSURE_CHOICES)
    concerns_addressed = models.CharField(max_length=10, choices=YES_NO_CHOICES)
    therapist_rating = models.PositiveSmallIntegerField(
        choices=SCORE_1_TO_5, validators=SCORE_VALIDATORS
    )
    follow_up = models.CharField(max_length=10, choices=YES_NO_CHOICES)

    class Meta(TimestampedFeedback.Meta):
        verbose_name = "Spa feedback"
        verbose_name_plural = "Spa feedback"

    def __str__(self) -> str:
        return f"Spa — {self.name} ({self.service_date})"


class HotelFeedback(ContactFeedbackFields, TimestampedFeedback):
    """Imperial Club — hotel stay feedback (table: feedback_hotelfeedback)."""

    room_number = models.CharField(max_length=10, choices=ROOM_NUMBER_CHOICES)
    check_in = models.DateField()
    check_out = models.DateField()

    front_desk = models.CharField(max_length=20, choices=RATING_CHOICES)
    housekeeping = models.CharField(max_length=20, choices=RATING_CHOICES)
    restaurant = models.CharField(max_length=20, choices=RATING_CHOICES)
    cleanliness = models.CharField(max_length=20, choices=RATING_CHOICES)
    amenities = models.CharField(max_length=20, choices=RATING_CHOICES)
    pool_fitness = models.CharField(
        max_length=20, choices=RATING_CHOICES, blank=True, null=True
    )

    class Meta(TimestampedFeedback.Meta):
        verbose_name = "Hotel feedback"
        verbose_name_plural = "Hotel feedback"

    def __str__(self) -> str:
        return f"Hotel — {self.name} (Room {self.room_number})"


class RestaurantFeedback(ContactFeedbackFields, TimestampedFeedback):
    """Imperial Club — resident dining feedback (table: feedback_restaurantfeedback)."""

    visit_date = models.DateField()
    outlet_visited = models.CharField(max_length=20, choices=OUTLET_CHOICES)

    food_quality = models.PositiveSmallIntegerField(
        choices=SCORE_1_TO_5, validators=SCORE_VALIDATORS
    )
    food_presentation = models.PositiveSmallIntegerField(
        choices=SCORE_1_TO_5, validators=SCORE_VALIDATORS
    )
    service_quality = models.PositiveSmallIntegerField(
        choices=SCORE_1_TO_5, validators=SCORE_VALIDATORS
    )
    staff_courtesy = models.PositiveSmallIntegerField(
        choices=SCORE_1_TO_5, validators=SCORE_VALIDATORS
    )
    ambience = models.PositiveSmallIntegerField(
        choices=SCORE_1_TO_5, validators=SCORE_VALIDATORS
    )
    decor = models.PositiveSmallIntegerField(
        choices=SCORE_1_TO_5, validators=SCORE_VALIDATORS
    )
    music = models.PositiveSmallIntegerField(
        choices=SCORE_1_TO_5, validators=SCORE_VALIDATORS
    )
    cleanliness = models.PositiveSmallIntegerField(
        choices=SCORE_1_TO_5, validators=SCORE_VALIDATORS
    )
    value_for_money = models.PositiveSmallIntegerField(
        choices=SCORE_1_TO_5, validators=SCORE_VALIDATORS
    )

    overall_satisfaction = models.PositiveSmallIntegerField(
        choices=SCORE_1_TO_5, validators=SCORE_VALIDATORS
    )
    recommend = models.CharField(max_length=10, choices=RECOMMEND_CHOICES)

    class Meta(TimestampedFeedback.Meta):
        verbose_name = "Restaurant feedback"
        verbose_name_plural = "Restaurant feedback"

    def __str__(self) -> str:
        return f"Dining — {self.name} · {self.outlet_visited} ({self.visit_date})"


# Convenience map used by the views layer for save-on-submit.
FEEDBACK_MODELS = {
    "club": ClubFeedback,
    "spa": SpaFeedback,
    "hotel": HotelFeedback,
    "restaurant": RestaurantFeedback,
}
