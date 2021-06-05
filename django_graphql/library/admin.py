from django.contrib import admin

from library.models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
        "created",
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "slug",
        "author",
        "created",
    )
