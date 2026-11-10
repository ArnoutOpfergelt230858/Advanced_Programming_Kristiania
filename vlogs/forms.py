from django import forms

from .helpers import normalize_tags
from .models import VlogPost


class VlogPostForm(forms.ModelForm):
    class Meta:
        model = VlogPost
        fields = ["title", "video_url", "description", "category", "tags"]
        labels = {"video_url": "Video link"}
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "A weekend exploring Oslo"}),
            "video_url": forms.URLInput(attrs={"placeholder": "https://www.youtube.com/watch?v=..."}),
            "description": forms.Textarea(attrs={"rows": 7, "placeholder": "Tell viewers what your vlog is about (at least 20 characters)."}),
            "tags": forms.TextInput(attrs={"placeholder": "oslo, travel, weekend"}),
        }

    def clean_description(self):
        description = self.cleaned_data["description"].strip()
        if len(description) < 20:
            raise forms.ValidationError("Describe your vlog in at least 20 characters.")
        return description

    def clean_tags(self):
        return normalize_tags(self.cleaned_data["tags"])
