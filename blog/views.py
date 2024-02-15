from django.shortcuts import render, get_object_or_404
from spellchecker import SpellChecker
from users.models import User
from .models import Bookmark, Post, Category
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.core.cache import cache
from django.views.decorators.cache import cache_page
from silk.profiling.profiler import silk_profile

CACHE_TIMEOUT = 60 * 5


@cache_page(CACHE_TIMEOUT)
def index(request, author_id=None, category_slug=None):
    cache_key = f"index_{author_id}_{category_slug}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    posts = Post.objects.all().order_by("-created_at")
    paginator = Paginator(posts, 3)
    page = request.GET.get("page")
    paged_posts = paginator.get_page(page)
    category = None
    author = None

    if author_id is not None:
        author = get_object_or_404(User, id=author_id)
        posts = posts.filter(author__id=author_id)

    elif category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)

    context = {
        "posts": paged_posts,
        "category": category,
        "author": author,
    }

    rendered_template = render(request, "index.html", context)
    cache.set(cache_key, rendered_template, CACHE_TIMEOUT)

    return rendered_template


def post(request, category_slug, post_slug):

    category = get_object_or_404(Category, slug=category_slug)
    post = get_object_or_404(Post, category=category, slug=post_slug)

    try:
        bookmarked = Bookmark.objects.filter(user=request.user, post=post)
    except:
        bookmarked = None

    post.total_views += 1
    post.save()

    context = {
        "post": post,
        "bookmarked": bookmarked,
    }
    return render(request, "blog/post.html", context)


def search(request):
    query = request.GET.get("q", "")
    corrected_query = query

    spell = SpellChecker()
    misspelled_words = spell.unknown(query.split())

    for word in misspelled_words:
        corrected_word = spell.correction(word)
        if corrected_word is not None:
            corrected_query = corrected_query.replace(word, corrected_word)

    cache_key = f"search_{corrected_query}"
    cached_response = cache.get(cache_key)

    if cached_response:
        return cached_response

    results = Post.objects.filter(
        Q(title__icontains=corrected_query) | Q(post__icontains=corrected_query)
    )
    context = {
        "query": query,
        "corrected_query": corrected_query,
        "posts": results,
    }
    response = render(request, "blog/search.html", context)

    cache.set(cache_key, response, CACHE_TIMEOUT)
    return response


@silk_profile(name="My API View Profile")
def my_api_view(request):
    pass
