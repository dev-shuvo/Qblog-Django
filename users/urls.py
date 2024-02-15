from django.urls import path
from .views import *

urlpatterns = [
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", logout, name="logout"),
    path("my-account/", my_account, name="my_account"),
    path("author-dashboard/", author_dashboard, name="author_dashboard"),
    path("author-dashboard/create-post/", create_post, name="create_post"),
    path("user-dashboard/", user_dashboard, name="user_dashboard"),
    path("bookmark-post/<int:post_id>/", bookmark_post, name="bookmark_post"),
]
