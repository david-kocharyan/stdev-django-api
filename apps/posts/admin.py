from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    model = Post

    list_display = ('title', 'created_at')
    search_fields = ('title', 'created_at')
    ordering = ('-created_at',)
    filter_horizontal = ()

    fieldsets = (
        ('Post Info', {'fields': ('title', 'description', 'image', 'category', 'author')}),
        ('Other info', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at',)


admin.site.register(Post, PostAdmin)
