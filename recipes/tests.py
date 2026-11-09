from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Recipe


class CookbookTests(TestCase):
    def setUp(self):
        self.staff = get_user_model().objects.create_user("chef", is_staff=True)
        self.data = {
            "title": "Scrambled eggs",
            "ingredients": "2 eggs\nButter\nSalt",
            "instructions": "Whisk the eggs and cook in butter.",
            "cooking_time": 5,
        }
        self.recipe = Recipe.objects.create(**self.data)

    def test_public_browsing_search_and_detail(self):
        response = self.client.get(reverse("recipe_list"))
        self.assertContains(response, "Scrambled eggs")
        self.assertNotContains(response, "Import from URL")
        self.assertContains(self.client.get(reverse("recipe_list"), {"q": "EGGS"}), "Scrambled eggs")
        self.assertNotContains(self.client.get(reverse("recipe_list"), {"q": "pasta"}), "Scrambled eggs")
        self.assertContains(self.client.get(reverse("recipe_detail", args=[self.recipe.pk])), self.recipe.instructions)

    def test_staff_can_create_and_edit(self):
        self.client.force_login(self.staff)
        form = self.client.get(reverse("recipe_create"))
        self.assertEqual(list(form.context["form"].fields), ["title", "ingredients", "instructions", "cooking_time"])
        response = self.client.post(reverse("recipe_create"), {**self.data, "title": "Omelette"})
        created = Recipe.objects.get(title="Omelette")
        self.assertRedirects(response, reverse("recipe_detail", args=[created.pk]))
        response = self.client.post(reverse("recipe_update", args=[created.pk]), {**self.data, "title": "Omelette", "cooking_time": 10})
        self.assertRedirects(response, reverse("recipe_detail", args=[created.pk]))
        created.refresh_from_db()
        self.assertEqual(created.cooking_time, 10)
        self.assertEqual(Recipe.objects.count(), 2)

    def test_invalid_recipe_is_not_saved(self):
        self.client.force_login(self.staff)
        response = self.client.post(reverse("recipe_create"), {**self.data, "cooking_time": -1})
        self.assertEqual(response.status_code, 200)
        self.assertIn("cooking_time", response.context["form"].errors)
        self.assertEqual(Recipe.objects.count(), 1)

    def test_writes_require_staff(self):
        for signed_in in (False, True):
            if signed_in:
                self.client.force_login(get_user_model().objects.create_user("reader"))
            self.assertEqual(self.client.post(reverse("recipe_create"), self.data).status_code, 302)
            self.assertEqual(self.client.post(reverse("recipe_update", args=[self.recipe.pk]), {**self.data, "title": "Changed"}).status_code, 302)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, "Scrambled eggs")
        self.assertEqual(Recipe.objects.count(), 1)

    def test_import_route_removed(self):
        self.assertEqual(self.client.get("/recipes/import/").status_code, 404)
