from django.contrib import admin
from .models import Author, Genre, Course, Page

# admin.site.register(Course)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Page)



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # list_display = ('title', 'status', 'borrower', 'due_back')
    list_display = ('title', 'status')
    list_filter = ('status', )

    # fieldsets = (
    #     (None, {
    #         'fields': ('book', 'imprint', 'id')
    #     }),
    #     ('Availability', {
    #         'fields': ('status', 'due_back', 'borrower')
    #     }),
    # )
