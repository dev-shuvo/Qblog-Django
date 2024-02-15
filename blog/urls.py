from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("author/<int:author_id>/", index, name="by_author"),
    path("category/<slug:category_slug>/", index, name="by_category"),
    path("blog/<slug:category_slug>/<slug:post_slug>/", post, name="post"),
    path("search/", search, name="search"),
]
