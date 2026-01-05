from django.contrib import admin
from .models import Film, Genre, Review

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'genre', 'rating', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('genre', 'year')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('film', 'author', 'text', 'rating', 'created_at')
    filter_horizontal = ('favorited_by',)  # ✅ Работает только если поле есть в модели