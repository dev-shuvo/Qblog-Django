from django.shortcuts import get_object_or_404, redirect, render
from blog.models import Bookmark, Post
from users.forms import UserForm
from users.models import User
from django.contrib import messages, auth
from users.utils import detectUser
from django.contrib.auth.decorators import login_required
from blog.forms import PostForm
from django.core.paginator import Paginator
from django.core.cache import cache
from django.views.decorators.cache import cache_page

CACHE_TIMEOUT = 60 * 5


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in.")
            return redirect("my_account")
        else:
            messages.error(request, "Invalid login credentials!")
            return redirect("login")
    return render(request, "users/login.html")


def signup(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect("my_account")
    elif request.method == "POST":
        form = UserForm(request.POST)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            user_type = form.cleaned_data["user_type"]

            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            user.user_type = user_type
            user.phone_number = phone_number
            user.save()

            messages.success(
                request,
                "Your account has been registered successfully.",
            )

            return redirect("login")
        else:
            for errors in form.errors.values():
                for error in errors:
                    messages.error(request, error)

                    print(error)
    else:
        form = UserForm()

    context = {
        "form": form,
    }
    return render(request, "users/signup.html", context)


@login_required(login_url="login")
def my_account(request):
    user = request.user
    redirectUrl = detectUser(user)

    return redirect(redirectUrl)


@login_required(login_url="login")
@cache_page(CACHE_TIMEOUT)
def author_dashboard(request):
    cache_key = f"author_dashboard_{request.user.id}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    posts = Post.objects.filter(author=request.user).order_by("-created_at")
    paginator = Paginator(posts, 1)
    page = request.GET.get("page")
    paged_posts = paginator.get_page(page)

    context = {"posts": paged_posts}

    rendered_template = render(request, "users/author/author-dashboard.html", context)
    cache.set(cache_key, rendered_template, CACHE_TIMEOUT)

    return rendered_template


@login_required(login_url="login")
def create_post(request):
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.total_views = 0
            post.save()
            messages.success(request, "Post created successfully.")
            return redirect("create_post")
        else:
            for errors in post_form.errors.values():
                for error in errors:
                    messages.error(request, error)
    else:
        post_form = PostForm()

    context = {"form": post_form}

    return render(request, "users/author/create-post.html", context)


@login_required(login_url="login")
def user_dashboard(request):

    bookmarks = Bookmark.objects.filter(user=request.user).order_by("-created_at")
    paginator = Paginator(bookmarks, 1)
    page = request.GET.get("page")
    paged_posts = paginator.get_page(page)

    context = {"bookmarks": paged_posts}

    return render(request, "users/regular-user/user-dashboard.html", context)


@login_required(login_url="login")
def bookmark_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if Bookmark.objects.filter(user=request.user, post=post).exists():
        Bookmark.objects.filter(user=request.user, post=post).delete()
    else:
        Bookmark.objects.create(user=request.user, post=post)

    return redirect("post", category_slug=post.category.slug, post_slug=post.slug)


@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    messages.info(request, "You are logged out successfully.")
    return redirect("login")
