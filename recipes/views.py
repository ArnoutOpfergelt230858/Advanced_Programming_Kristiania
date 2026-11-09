from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import Recipe


def recipe_list(request):
    query = request.GET.get("q", "").strip()

    recipes = Recipe.objects.all().order_by("title")

    if query:
        recipes = recipes.filter(title__icontains=query)

    return render(
        request,
        "recipes/recipe_list.html",
        {
            "recipes": recipes,
            "query": query,
        },
    )


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    return render(
        request,
        "recipes/recipe_detail.html",
        {"recipe": recipe},
    )


@staff_member_required
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)

        if form.is_valid():
            recipe = form.save()
            return redirect("recipe_detail", pk=recipe.pk)
    else:
        form = RecipeForm()

    return render(
        request,
        "recipes/recipe_form.html",
        {"form": form},
    )

@staff_member_required
def recipe_update(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == "POST":
        form = RecipeForm(request.POST, instance=recipe)

        if form.is_valid():
            recipe = form.save()
            return redirect("recipe_detail", pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)

    return render(
        request,
        "recipes/recipe_form.html",
        {
            "form": form,
            "recipe": recipe,
        },
    )
