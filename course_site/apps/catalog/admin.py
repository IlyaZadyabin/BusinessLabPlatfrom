from django.contrib import admin
from .models import Author, Genre, Book

# admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'borrower', 'due_back')
    list_filter = ('status', 'due_back')

    # fieldsets = (
    #     (None, {
    #         'fields': ('book', 'imprint', 'id')
    #     }),
    #     ('Availability', {
    #         'fields': ('status', 'due_back', 'borrower')
    #     }),
    # )
