from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.author}'

    def update_rating(self):
        sum_rating_post = Post.objects.filter(author_id=self.pk).aggregate(rating=Coalesce(Sum('rating'), 0))['rating'] * 3
        rating_comment = Comment.objects.filter(comment_user_id=self.author).aggregate(rating_comment=Coalesce(Sum('rating'), 0))['rating_comment']
        rating_comment_post = Comment.objects.filter(comment_post__author__author=self.author).aggregate(post_rating=Coalesce(Sum('rating'), 0))['post_rating']

        self.rating_author = sum_rating_post + rating_comment + rating_comment_post
        self.save()



class Category(models.Model):
    name_category_post = models.CharField(max_length=128, unique=True)


    def __str__(self):
        return f'{self.name_category_post}'


class Post(models.Model):
    NEWS = 'NW'
    EVENTS = 'EV'
    ANALYTICS = 'AN'
    ARTICLE = 'AR'
    CATEGORY_TYPE = (
        (NEWS, 'Новость'),
        (EVENTS, 'События'),
        (ANALYTICS, 'Аналитика'),
        (ARTICLE, 'Статья'),
    )
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category_type = models.CharField(max_length=2, choices=CATEGORY_TYPE, default=ARTICLE)
    date_of_creation = models.DateTimeField(auto_now_add=True)
    post_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    article_title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.article_title}: {self.text} : {self.post_category}'

    def get_absolute_url(self):
        return reverse('new_detail', args=[str(self.id)])

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:64] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_comment = models.TextField()
    datetime_comment = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)


    def __str__(self):
        return f'{self.comment_post}: {self.comment_post}'

    def like(self):
        self.rating += 1

        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriber',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriber',
    )