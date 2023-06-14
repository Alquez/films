from django.contrib import admin
from .models import Movie, Director, Genre, Rating, RatingStar, Actor, Comment
from django.utils.safestring import mark_safe
from django.db import models
from django.forms import Textarea


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = [
        'get_image', 'name', 'description', 'year',
        'directors', 'display_genres', 'display_actors',
        'is_exclusive'
    ]
    list_editable = ['name', 'description', 'year', 'directors']
    readonly_fields = ['get_image']
    search_fields = ['name', 'directors__name', 'genre__name', 'year']
    prepopulated_fields = {'slug': ('name', )}

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 20})},
        models.CharField: {'widget': Textarea(attrs={'rows': 2, 'cols': 15})},
    }

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" height="200"/>')

    def display_genres(self, obj):
        return ', '.join([str(each_genre) for each_genre in obj.genre.all()])

    def display_actors(self, obj):
        return ', '.join([str(each_actor) for each_actor in obj.actor.all()])

    get_image.short_description = "Изображение"


admin.site.register(Director)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}


admin.site.register(RatingStar)
admin.site.register(Rating)
admin.site.register(Actor)
admin.site.register(Comment)
