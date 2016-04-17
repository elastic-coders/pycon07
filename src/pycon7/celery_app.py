from celery import Celery
from django.conf import settings

app = Celery('pycon7')

app.config_from_object(settings)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


