import datetime
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.utils import timezone
from news.models import Post, Subscriber, Category
from django.core.mail import EmailMultiAlternatives


logger = logging.getLogger(__name__)


def my_job():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    posts_send = Post.objects.filter(date_of_creation__gte=last_week).order_by('date_of_creation')

    category = set(posts_send.values_list('post_category__name_category_post', flat=True))
    subscriber_email = []

    for c in category:
        subscribers = Subscriber.objects.filter(category__name_category_post=c)
        subscriber_email += [i.user.email for i in subscribers]
    subscriber_email = set(subscriber_email)

    html_content = render_to_string(
        'mailin.html',
        {'link': f'settings.SITE_URL/news/',
            'post': posts_send,
        })
    msg = EmailMultiAlternatives(
        subject='Новые публикации ',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscriber_email,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week="fri", hour="18", minute="00"),
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="fri", hour="18", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")