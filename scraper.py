from bs4 import BeautifulSoup
import requests
from flask import Flask, render_template, url_for, request, redirect
from dates import predmetDatum, formatirajDatum

def soup_request(url):
    page = requests.get(url, headers=headers)
    return BeautifulSoup(page.content, 'html.parser')

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
MTR_URL = 'http://ctm.fon.bg.ac.rs/menadzment-tehnologije-i-razvoja/'
SPA_URL = 'http://is.fon.bg.ac.rs/strukture-podataka-i-algoritmi/vesti/'
STAT_URL = 'http://statlab.fon.bg.ac.rs/predmeti/statistika-2/'
FMIR_URL = 'http://finansije.fon.bg.ac.rs/osnovne-studije/finansijski-menadzment-i-racunovodstvo/Vesti.html'
NUM_URL = 'http://math.fon.bg.ac.rs/vesti/numericka-analiza/'
DMS_URL = 'http://math.fon.bg.ac.rs/vesti/dms/'

def cetvrtiSemestar():
    lista = []
    lista.append(mtrPoslednji())
    lista.append(spaPoslednji())
    lista.append(fmirPoslednji())
    lista.append(numPoslednji())
    lista.append(dmsPoslednji())
    lista.append(statPoslednji())
    lista.sort(key=lambda x: x['vreme'], reverse=True)

    return lista


def mtrPosts():
    soup = soup_request(MTR_URL)
    soup = soup.findAll(class_ = 'status-publish')
    lista = []

    for element in soup:
        post = {}
        post['link'] = element.find('a')['href']
        post['naslov'] = element.find(class_='post-title entry-title').text
        post['vreme'] = formatirajDatum(element.find(class_='updated').text, '%b %d, %Y')
        opis = element.find(class_='entry-summary').text.replace('Read More', '')
        if len(opis) > 150:
            post['opis'] = opis[0:150]+'...'
        else:
            post['opis'] = opis
        post['tip'] = predmetDatum(post['vreme'])
        lista.append(post)

    return lista

def mtrPoslednji():
    soup = soup_request(MTR_URL)
    soup = soup.find(class_ = 'status-publish')

    post = {}
    post['url'] = '/mtr'
    post['predmet'] = 'Menadžment tehnologije i razvoja'
    post['link'] = soup.find('a')['href']
    post['naslov'] = soup.find(class_='post-title entry-title').text
    post['vreme'] = formatirajDatum(soup.find(class_='updated').text, '%b %d, %Y')
    opis = soup.find(class_='entry-summary').text.replace('Read More', '')
    if len(opis) > 150:
        post['opis'] = opis[0:150]+'...'
    else:
        post['opis'] = opis
    post['tip'] = predmetDatum(post['vreme'])

    return post

def spaPoslednji():
    soup = soup_request(SPA_URL)
    soup = soup.find(class_ = 'status-publish')

    post = {}
    post['url'] = '/spa'
    post['predmet'] = 'Strukture podataka i algoritmi'
    post['link'] = soup.find('a')['href']
    post['naslov'] = soup.find(class_='entry-title').text
    post['vreme'] = formatirajDatum(soup.find(class_='updated').text, '%d. %B %Y.')
    opis = soup.find(class_='entry-content').text
    if len(opis) > 150:
        post['opis'] = opis[0:150]+'...'
    else:
        post['opis'] = opis
    post['tip'] = predmetDatum(post['vreme'])

    return post

def spaPosts():
    soup = soup_request(SPA_URL)
    soup = soup.findAll(class_ = 'status-publish')
    lista = []

    for element in soup:
        post = {}
        post['link'] = element.find('a')['href']
        post['naslov'] = element.find(class_='entry-title').text
        post['vreme'] = formatirajDatum(element.find(class_='updated').text, '%d. %B %Y.')
        opis = element.find(class_='entry-content').text
        if len(opis) > 150:
            post['opis'] = opis[0:150]+'...'
        else:
            post['opis'] = opis
        post['tip'] = predmetDatum(post['vreme'])
        lista.append(post)

    return lista


def statPosts():
    soup = soup_request(STAT_URL)
    soup = soup.findAll(class_ = 'status-publish')
    lista = []

    for element in soup:
        post = {}
        post['link'] = element.find('a')['href']
        post['naslov'] = element.find('h4').text
        post['vreme'] = formatirajDatum(element.find(class_='date_label').text,'%d/%m/%Y')
        post['opis'] = ''
        post['tip'] = predmetDatum(post['vreme'])
        lista.append(post)

    return lista


def statPoslednji():
    soup = soup_request(STAT_URL)
    soup = soup.find(class_ = 'status-publish')

    post = {}
    post['url'] = '/stat'
    post['predmet'] = 'Statistika'
    post['link'] = soup.find('a')['href']
    post['naslov'] = soup.find('h4').text
    post['vreme'] = formatirajDatum(soup.find(class_='date_label').text,'%d/%m/%Y')
    post['opis'] = ''
    post['tip'] = predmetDatum(post['vreme'])

    return post


def fmirPosts():
    soup = soup_request(FMIR_URL)
    soup = soup.findAll(class_ = 'dataNav')
    lista = []

    for element in soup:
        post = {}
        post['link'] = element.find('a')['href']
        post['naslov'] = element.find(class_='title').text
        post['vreme'] = formatirajDatum(element.find(class_='eventDate').text,'%d. %m. %Y.')
        opis = element.find(class_='lead').text
        if len(opis) > 150:
            post['opis'] = opis[0:150]+'...'
        else:
            post['opis'] = opis
        post['tip'] = predmetDatum(post['vreme'])
        lista.append(post)

    return lista


def fmirPoslednji():
    soup = soup_request(FMIR_URL)
    soup = soup.find(class_ = 'dataNav')

    post = {}
    post['url'] = '/fmir'
    post['predmet'] = 'Finansijski menadžment i računovodstvo'
    post['link'] = soup.find('a')['href']
    post['naslov'] = soup.find(class_='title').text
    post['vreme'] = formatirajDatum(soup.find(class_='eventDate').text,'%d. %m. %Y.')
    opis = soup.find(class_='lead').text
    if len(opis) > 150:
        post['opis'] = opis[0:150]+'...'
    else:
        post['opis'] = opis
    post['tip'] = predmetDatum(post['vreme'])

    return post


def numPosts():
    soup = soup_request(NUM_URL)
    soup = soup.findAll(class_ = 'k-article-summary')
    lista = []

    for element in soup:
        post = {}
        post['link'] = 'http://math.fon.bg.ac.rs'+element.find('a')['href']
        post['naslov'] = element.find('h5').text
        post['vreme'] = formatirajDatum(element.find(class_='news-meta-date').text[:11],'%d.%m.%Y.')
        opis = element.find(class_='news-body').text.replace('ВИШЕ', '')
        if len(opis) > 150:
            post['opis'] = opis[0:150]+'...'
        else:
            post['opis'] = opis
        post['tip'] = predmetDatum(post['vreme'])
        lista.append(post)

    return lista


def numPoslednji():
    soup = soup_request(NUM_URL)
    soup = soup.find(class_ = 'k-article-summary')

    post = {}
    post['url'] = '/num'
    post['predmet'] = 'Numerička analiza'
    post['link'] = 'http://math.fon.bg.ac.rs'+soup.find('a')['href']
    post['naslov'] = soup.find('h5').text
    post['vreme'] = formatirajDatum(soup.find(class_='news-meta-date').text[:11],'%d.%m.%Y.')
    opis = soup.find(class_='news-body').text.replace('ВИШЕ', '')
    if len(opis) > 150:
        post['opis'] = opis[0:150]+'...'
    else:
        post['opis'] = opis
    post['tip'] = predmetDatum(post['vreme'])

    return post


def dmsPosts():
    soup = soup_request(DMS_URL)
    soup = soup.findAll(class_ = 'k-article-summary')
    lista = []

    for element in soup:
        post = {}
        post['link'] = 'http://math.fon.bg.ac.rs'+element.find('a')['href']
        post['naslov'] = element.find('h5').text
        post['vreme'] = formatirajDatum(element.find(class_='news-meta-date').text[:11],'%d.%m.%Y.')
        opis = element.find(class_='news-body').text.replace('ВИШЕ', '')
        if len(opis) > 150:
            post['opis'] = opis[0:150]+'...'
        else:
            post['opis'] = opis
        post['tip'] = predmetDatum(post['vreme'])
        lista.append(post)

    return lista


def dmsPoslednji():
    soup = soup_request(DMS_URL)
    soup = soup.find(class_ = 'k-article-summary')

    post = {}
    post['url'] = '/dms'
    post['predmet'] = 'Diskretne matematičke strukture'
    post['link'] = 'http://math.fon.bg.ac.rs'+soup.find('a')['href']
    post['naslov'] = soup.find('h5').text
    post['vreme'] = formatirajDatum(soup.find(class_='news-meta-date').text[:11],'%d.%m.%Y.')
    opis = soup.find(class_='news-body').text.replace('ВИШЕ', '')
    if len(opis) > 150:
        post['opis'] = opis[0:150]+'...'
    else:
        post['opis'] = opis
    post['tip'] = predmetDatum(post['vreme'])

    return post