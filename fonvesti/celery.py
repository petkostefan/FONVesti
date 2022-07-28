import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fonvesti.settings')

app = Celery('fonvesti')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'get_news_os':{
        'task':'vesti.tasks.sacuvaj_nove_postove_os',
        'schedule':30.0
    },
    'get_news_semestar4':{
        'task':'vesti.tasks.sacuvaj_nove_postove_4sem',
        'schedule':60.0
    }
}

app.autodiscover_tasks()