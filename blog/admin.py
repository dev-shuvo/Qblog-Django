from django.contrib import admin
from django.shortcuts import render
from .models import Category, Post, Bookmark
from django.utils.html import format_html
from .models import Post
from django.db import models


class CatAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    prepopulated_fields = {"slug": ("name",)}

    def get_urls(self):
        from django.urls import path

        urls = super().get_urls()
        custom_urls = [
            path(
                "total-blogs-by-category/",
                self.admin_site.admin_view(self.total_blogs_by_category),
                name="total-blogs-by-category",
            ),
        ]
        return custom_urls + urls

    def total_blogs_by_category(self, request):
        total_blogs = Category.objects.annotate(article_count=models.Count("post"))

        labels = [blog.name for blog in total_blogs]
        data = [category.article_count for category in total_blogs]

        context = {
            "labels": labels,
            "data": data,
        }
        return render(request, "admin/total_blogs_by_category.html", context)


class PostAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "author",
        "total_views",
        "created_at",
        "modified_at",
    )
    prepopulated_fields = {"slug": ("title",)}
    list_display_links = ("title",)
    search_fields = ("title", "author__email__icontains", "author__username__icontains")
    list_filter = ("category", "author")
    readonly_fields = ("total_views",)


class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "created_at")
    list_filter = ("user",)
    search_fields = (
        "post__author__email__icontains",
        "post__author__username__icontains",
    )


admin.site.register(Category, CatAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Bookmark, BookmarkAdmin)
