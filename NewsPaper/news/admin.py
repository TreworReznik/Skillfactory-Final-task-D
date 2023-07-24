from django.contrib import admin
from .models import Author, Post, Comment, Category, PostCategory, Subscriber

admin.site.register(Post)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(PostCategory)
admin.site.register(Subscriber)
# Register your models here.
