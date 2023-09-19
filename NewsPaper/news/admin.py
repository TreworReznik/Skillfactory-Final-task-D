from django.contrib import admin
from .models import Author, Post, Comment, Category, PostCategory, Subscriber
from modeltranslation.admin import TranslationAdmin


class PostAdmin(TranslationAdmin):
    model = Post


class AuthorAdmin(TranslationAdmin):
    model = Author


class CategoryAdmin(TranslationAdmin):
    model = Category


class SubscriberAdmin(TranslationAdmin):
    model = Subscriber


class PostCategoryAdmin(TranslationAdmin):
    model = PostCategory


class CommentAdmin(TranslationAdmin):
    model = Comment



admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Subscriber)
# Register your models here.
