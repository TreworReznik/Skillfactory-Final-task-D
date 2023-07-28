from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from news.management.commands.runapscheduler import my_job

from .models import Post

@shared_task
def new_post_send(post_id):

    post = Post.objects.get(pk=post_id)

    emails = User.objects.filter(subscriber__category=post.post_category).values_list('email', flat=True)
    subject = f' категории {post.post_category}'

    text_content = (
        f'Автор: {post.author}\n\n'
        f'NewsPost: {post.article_title}\n'

        f'Ссылка на новость : http://127.0.0.1:8000{post.get_absolute_url()}'
    )
    html_content = (
        f'NewsPost: {post.article_title}<br>'
        f'Автор: {post.author}'
        f'<a href="http://127.0.0.1:8000{post.get_absolute_url()}">'
        f'Ссылка на новость </a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()



@shared_task
def periodic_mailing():
    my_job()