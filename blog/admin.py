from django.contrib import admin

# Register your models here.
from blog.models import Category, Tag, Post, ContentImage
from markdownx.admin import MarkdownxModelAdmin

class ContentImageInline(admin.TabularInline):
    mocdel = ContentImage
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = [
        ContentImageInline,
    ]


admin.site.register(Post, PostAdmin, MarkdownxModelAdmin)
admin.site.register(Category)
admin.site.register(Tag)
