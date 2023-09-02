from django.contrib import admin
from .models import Author, Post, Comment, Category, PostCategory, Subscriber

class PostAdmin(admin.ModelAdmin):
    list_display = ('article_title', 'author', 'category_type', 'date_of_creation', 'rating', )
    list_filter = ('author', 'date_of_creation', 'category_type', 'rating',)
    search_fields = ('author__author__username', 'rating', 'date_of_creation', 'category_type', 'post_category__name_category_post', 'article_title', )


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('author', 'rating_author',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name_category_post', )


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category', )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('comment_user', 'text_comment', 'datetime_comment', 'rating', )


admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
# Register your models here.
