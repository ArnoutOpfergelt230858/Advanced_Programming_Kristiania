from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "title",
            "ingredients",
            "instructions",
            "cooking_time",
        ]

        labels = {
            "cooking_time": "Cooking time (minutes)",
        }

        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": "e.g. Creamy mushroom pasta"}
            ),
            "ingredients": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "Enter each ingredient on a separate line",
                }
            ),
            "instructions": forms.Textarea(
                attrs={
                    "rows": 8,
                    "placeholder": "Explain how to prepare your recipe",
                }
            ),
        }
