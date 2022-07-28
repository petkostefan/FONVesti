from bs4 import BeautifulSoup
from .dates import formatiraj_datum, oznaci_nov_post
import requests
from datetime import datetime

from .models import Izvor, Vest


HEADERS = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

OSNOVNE_STUDIJE = 'http://www.fon.bg.ac.rs/obavestenja/vesti-osnovne-studije/'

MTR_URL = 'http://ctm.fon.bg.ac.rs/menadzment-tehnologije-i-razvoja/'
SPA_URL = 'http://is.fon.bg.ac.rs/strukture-podataka-i-algoritmi/vesti/'
STAT_URL = 'http://statlab.fon.bg.ac.rs/predmeti/statistika-2/'
FMIR_URL = 'http://finansije.fon.bg.ac.rs/osnovne-studije/finansijski-menadzment-i-racunovodstvo/Vesti.html'
NUM_URL = 'http://math.fon.bg.ac.rs/vesti/numericka-analiza/'
DMS_URL = 'http://math.fon.bg.ac.rs/vesti/dms/'

def soup_request(url):
    page = requests.get(url, headers=HEADERS)
    return BeautifulSoup(page.content, 'html.parser')

def uzmi_jedan(url, kontejner, post, naslov, opis, datum, format_datuma, klasa_link=''):
    soup = soup_request(url)
    soup = soup.find(class_ = kontejner)
    soup_post = soup.find(class_ = post)

    post = {}
    post['naslov'] = soup_post.find(class_= naslov).decode_contents()
    if klasa_link:
        soup_link = soup_post.find(class_ = klasa_link)
        post['link'] = soup_link.find('a')['href']
    else:
        post['link'] = soup_post.find('a')['href']
    post['vreme'] = formatiraj_datum(soup_post.find(class_=datum).text, format_datuma)
    opis_posta = soup_post.find(class_= opis).text
    if not opis_posta:
        opis_posta = soup_post.find(opis).text
    if len(opis_posta) > 150:
        post['opis'] = opis_posta[0:150]+'...'
    else:
        post['opis'] = opis_posta
    post['tip'] = oznaci_nov_post(post['vreme'])

    return post

def uzmi_sve(url, kontejner, post, naslov, opis, datum, format_datuma, link=''):
    soup = soup_request(FMIR_URL)
    soup = soup.findAll(class_ = 'dataNav')
    lista = []

    for post in soup:
        if post.find(class_= naslov) and post.find(class_= naslov).text:
            lista.append(uzmi_jedan(url, kontejner, post, naslov, opis, datum, format_datuma, link))
        else:
            pass

    return lista

def vesti_osnovne_studije():
    soup = soup_request(OSNOVNE_STUDIJE)
    posts = soup.findAll('article')
    post_list = []

    for post in posts:
        data = {}
        data['izvor'] = Izvor.objects.get(naziv='Osnovne studije')
        data['naslov'] = post.find(class_='entry-title').a.text
        data['opis'] = post.find(class_ = 'entry-content').p.text
        data['vreme'] = datetime.fromisoformat(post.find('time').get('datetime'))
        data['link'] = post.a.get('href')
        data['img_link'] = post.find(class_='thumb').a.img['src'] if post.find(class_='thumb').a.img is not None else None

        post_list.append(data)

    return post_list


def mtr_postovi():
    soup = soup_request(MTR_URL)
    soup = soup.findAll(class_ = 'status-publish')
    lista = []

    for element in soup:
        post = {}
        post['izvor'] = Izvor.objects.get(naziv='Menadžment tehnologije i razvoja')
        post['link'] = element.find('a')['href']
        post['naslov'] = element.find(class_='post-title entry-title').text
        post['vreme'] = formatiraj_datum(element.find(class_='updated').text, '%b %d, %Y')
        post['opis'] = element.find(class_='entry-summary').text.replace('Read More', '')
        post['img_link'] = None

        lista.append(post)

    return lista


def spa_postovi():
    soup = soup_request(SPA_URL)
    soup = soup.findAll(class_ = 'status-publish')
    lista = []

    for element in soup:
        post = {}
        post['izvor'] = Izvor.objects.get(naziv='Strukture podataka i algoriitmi')
        post['link'] = element.find('a')['href']
        post['naslov'] = element.find(class_='entry-title').text
        post['vreme'] = datetime.fromisoformat(element.find(class_='entry-date').get('datetime'))
        post['opis'] = element.find(class_='entry-content').text
        post['img_link'] = None

        lista.append(post)

    return lista


def stat_postovi():
    soup = soup_request(STAT_URL)
    soup = soup.findAll(class_ = 'status-publish')
    lista = []

    for element in soup:
        post = {}
        post['izvor'] = Izvor.objects.get(naziv='Statistika')
        post['link'] = element.find('a')['href']
        post['naslov'] = element.find('h4').text
        post['vreme'] = formatiraj_datum(element.find(class_='date_label').text,'%d/%m/%Y')
        post['opis'] = ''
        post['img_link'] = None
        lista.append(post)

    return lista


def fmir_postovi():
    soup = soup_request(FMIR_URL)
    soup = soup.findAll(class_ = 'dataNav')
    lista = []

    for element in soup:
        post = {}
        post['izvor'] = Izvor.objects.get(naziv='Finansijski menadžment i računovodstvo')
        post['link'] = element.find('a')['href']
        post['naslov'] = element.find(class_='title').text
        post['vreme'] = formatiraj_datum(element.find(class_='eventDate').text,'%d. %m. %Y.')
        post['opis'] = element.find(class_='lead').text
        post['img_link'] = None

        lista.append(post)

    return lista


def num_postovi():
    soup = soup_request(NUM_URL)
    soup = soup.findAll(class_ = 'k-article-summary')
    lista = []
    for element in soup:
        post = {}
        post['izvor'] = Izvor.objects.get(naziv='Numerička analiza')
        post['link'] = 'http://math.fon.bg.ac.rs'+element.find('a')['href']
        post['naslov'] = element.find('h5').text
        vreme = element.find(class_='news-meta-date').text
        vreme = vreme[:11] + vreme[14:19]
        post['vreme'] = formatiraj_datum(vreme,'%d.%m.%Y.%H:%M')
        post['opis'] = element.find(class_='news-body').text.replace('ВИШЕ', '')
        post['img_link'] = None
        lista.append(post)

    return lista


def dms_postovi():
    soup = soup_request(DMS_URL)
    soup = soup.findAll(class_ = 'k-article-summary')
    lista = []

    for element in soup:
        post = {}
        post['izvor'] = Izvor.objects.get(naziv='Diskretne matematičke strukture')
        post['link'] = 'http://math.fon.bg.ac.rs'+element.find('a')['href']
        post['naslov'] = element.find('h5').text
        vreme = element.find(class_='news-meta-date').text
        vreme = vreme[:11] + vreme[14:19]
        post['vreme'] = formatiraj_datum(vreme,'%d.%m.%Y.%H:%M')
        post['opis'] = element.find(class_='news-body').text.replace('ВИШЕ', '')
        post['img_link'] = None
        lista.append(post)

    return lista

    
# def sacuvaj_nove_postove_os():
#     poslednjih_pet = [el['vreme'] for el in list(VestOsnovneStudije.objects.all().values('vreme')[-5:])]
    
#     novi = vesti_osnovne_studije()
#     novi.reverse()

#     for post in novi:
#         if post['vreme'] not in poslednjih_pet:
#             novi_post = VestOsnovneStudije.objects.create(**post)
#             print(novi_post)

#     return novi