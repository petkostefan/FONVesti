from datetime import datetime, timedelta
from django.utils import timezone
import pytz
from django.conf import settings

def oznaci_nov_post(datum):
    sada = datetime.now()
    
    if datetime.strptime(datum, '%d.%m.%Y. %H:%M') + timedelta(days=1)>=sada:
        return 'Novo'
    else:
        return ''

def oznaci_nove_postove(postovi):
    for post in postovi:
        if post.vreme + timedelta(days=1)>=timezone.make_aware(datetime.now()):
            post.tip = 'Novo'
    
    return postovi

def formatiraj_datum(datum, format_datuma=''):
    if format_datuma:
        datum = datetime.strptime(datum, format_datuma)
        datum = timezone.make_aware(datum, pytz.timezone(settings.TIME_ZONE))
        return datetime.isoformat(datum)
    return datetime.fromisoformat(datum).strftime('%d.%m.%Y. %H:%M')

def ulepsaj_datum(datum):

    return datum.strftime('%d.%m.%Y. %H:%M')

def oznaci_tip(datum):
    sada = datetime.now()
    
    if datetime.strptime(datum, '%d.%m.%Y. %H:%M') + timedelta(days=3)>=sada:
        return 'warning'
    else:
        return 'info'