from django.contrib import admin
from django.utils.html import format_html  # Add this import
from .models import BlogPost, Comment, Like

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'publication_date', 'author', 'display_image')
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Image'

admin.site.register(BlogPost, BlogPostAdmin)
    

admin.site.register(Comment)
admin.site.register(Like)