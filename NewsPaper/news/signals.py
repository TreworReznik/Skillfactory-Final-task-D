from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from .tasks import new_post_send
from .models import Post


@receiver(post_save, sender=Post)
def post_created(instance, created, **kwargs):
    if not created:
        return

    emails = User.objects.filter(subscriber__category=instance.post_category).values_list('email', flat=True)
    subject = f' категории {instance.post_category}'

    text_content = (
        f'Автор: {instance.author}\n\n'
        f'NewsPost: {instance.article_title}\n'
        
        f'Ссылка на новость : http://127.0.0.1:8000{instance.get_absolute_url()}'
    )
    html_content = (
        f'NewsPost: {instance.article_title}<br>'
        f'Автор: {instance.author}'
        f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
        f'Ссылка на новость </a>'
    )
    for email in emails:
        msg = EmailMultiAlternatives(subject, text_content, None, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@receiver(post_save, sender=Post)
def post_send(instance, created, **kwargs):
    if not created:
        return
    new_post_send.delay(instance.id)
