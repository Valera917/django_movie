from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Genre, Movie, MovieShorts, Actor, RatingStar, Rating, Reviews


from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категория"""
    list_display = ('id', 'name', 'url', )
    list_display_links = ('name',)
    prepopulated_fields = {'url': ('name',)}


class ReviewsInline(admin.TabularInline):
    """Отзывы на странице фильма"""
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')


class MovieShotsInline(admin.TabularInline):
    model = MovieShorts
    extra = 1
    readonly_fields = ("get_photo",)

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50" height="50">')

    get_photo.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ('title', 'category', 'url', 'draft')
    list_display_links = ('title',)
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__name')
    list_editable = ('draft',)
    readonly_fields = ("get_photo",)
    inlines = [MovieShotsInline, ReviewsInline]
    actions = ['publish', 'unpublish']
    prepopulated_fields = {'url': ('title',)}
    save_on_top = True
    save_as = True
    form = MovieAdminForm
    # fields = (('actors', 'directors', 'genres'),)
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_photo"))
        }),
        (None, {
            "fields": (("year", "world_premier", "country"),)
        }),
        ("Actors", {
            'classes': ('collapse',),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.poster.url}" width="110" height="110">')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)

        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)

        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change', )

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change',)

    get_photo.short_description = 'Постер'


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ('name', 'email', 'parent', 'movie')
    list_display_links = ('name',)
    readonly_fields = ('name', 'email')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")
    prepopulated_fields = {'url': ('name',)}


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актеры"""
    list_display = ("name", "age", "get_photo")
    readonly_fields = ("get_photo",)

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50" height="50">')

    get_photo.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "movie", "ip")


@admin.register(MovieShorts)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie", "get_photo")
    readonly_fields = ("get_photo",)

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50" height="50">')

    get_photo.short_description = 'Изображение'


admin.site.register(RatingStar)

admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'

