from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_safe

from .forms import VlogPostForm
from .models import VlogPost


@require_safe
def vlog_list(request):
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    posts = VlogPost.objects.select_related("author")
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(tags__icontains=query) | Q(author__username__icontains=query))
    if category:
        posts = posts.filter(category=category)
    page = Paginator(posts, 6).get_page(request.GET.get("page"))
    return render(request, "vlogs/vlog_list.html", {
        "page_obj": page, "query": query, "category": category,
        "categories": VlogPost.Category.choices,
    })


@require_safe
def vlog_detail(request, pk):
    post = get_object_or_404(VlogPost.objects.select_related("author"), pk=pk)
    return render(request, "vlogs/vlog_detail.html", {"post": post})


@staff_member_required
@require_http_methods(["GET", "POST"])
def vlog_create(request):
    form = VlogPostForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        messages.success(request, "Your vlog has been published.")
        return redirect(post)
    return render(request, "vlogs/vlog_form.html", {"form": form})


@staff_member_required
@require_http_methods(["GET", "POST"])
def vlog_update(request, pk):
    post = get_object_or_404(VlogPost, pk=pk)
    form = VlogPostForm(request.POST if request.method == "POST" else None, instance=post)
    if request.method == "POST" and form.is_valid():
        post = form.save()
        messages.success(request, "Your changes have been saved.")
        return redirect(post)
    return render(request, "vlogs/vlog_form.html", {"form": form, "post": post})


@staff_member_required
@require_http_methods(["GET", "POST"])
def vlog_delete(request, pk):
    post = get_object_or_404(VlogPost, pk=pk)
    if request.method == "POST":
        post.delete()
        messages.success(request, "The vlog has been deleted.")
        return redirect("vlogs:list")
    return render(request, "vlogs/vlog_confirm_delete.html", {"post": post})
