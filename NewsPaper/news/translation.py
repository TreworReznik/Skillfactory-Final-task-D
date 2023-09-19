from .models import Category, Author, Post, Comment, Subscriber, PostCategory
from modeltranslation.translator import register, TranslationOptions


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name_category_post',)  # указываем, какие именно поля надо переводить в виде кортежа


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('author', 'rating_author',)


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('author', 'category_type', 'date_of_creation', 'post_category', 'article_title', 'text', 'rating')


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('comment_user', 'text_comment', 'datetime_comment', 'comment_post', 'rating')


@register(Subscriber)
class SubscriberTranslationOptions(TranslationOptions):
    fields = ('user', 'category')

@register(PostCategory)
class PostCategoryTranslationOptions(TranslationOptions):
    fields = ('post', 'category')