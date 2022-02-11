from django.contrib import admin

from apps.categories.models import Category


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    prepopulated_fields = {'slug': ('name',)}

    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)

    fieldsets = (
        ('Category Info', {'fields': ('name', 'slug', 'description')}),
        ('Other info', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at',)


admin.site.register(Category, CategoryAdmin)
