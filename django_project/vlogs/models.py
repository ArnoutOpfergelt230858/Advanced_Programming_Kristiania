from django.conf import settings
from django.core.validators import URLValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone


class VlogPost(models.Model):
    class Category(models.TextChoices):
        DAILY = "daily", "Daily life"
        TRAVEL = "travel", "Travel"
        FOOD = "food", "Food"
        TECH = "tech", "Technology"
        LEARNING = "learning", "Learning"
        OTHER = "other", "Other"

    title = models.CharField(max_length=200)
    video_url = models.URLField(max_length=500, validators=[URLValidator(schemes=["https", "http"])])
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="vlog_posts")
    published_date = models.DateTimeField(default=timezone.now, db_index=True)
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.DAILY)
    tags = models.CharField(max_length=200, blank=True, help_text="Separate tags with commas, e.g. oslo, weekend")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_date", "-pk"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("vlogs:detail", kwargs={"pk": self.pk})

    @property
    def tag_list(self):
        return [tag.strip() for tag in self.tags.split(",") if tag.strip()]
