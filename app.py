from flask import Flask, render_template, url_for, request, redirect
from scraper import mtrPoslednji, mtrPosts, spaPoslednji, spaPosts, cetvrtiSemestar, statPosts, fmirPosts, numPosts, dmsPosts
from datetime import datetime, timedelta
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = APScheduler()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cetvrti')
def predmeti():
    return render_template('semestri.html', predmeti=cetvrtiSemestar())

@app.route('/mtr')
def vest():
    return render_template('vesti.html', posts=mtrPosts(), naslov='Menadzment tehnologije i razvoja')

@app.route('/spa')
def spa():
    return render_template('vesti.html', posts=spaPosts(), naslov='Strukture podataka i algoritmi')

@app.route('/stat')
def stat():
    return render_template('vesti.html', posts=statPosts(), naslov='Statistika')

@app.route('/fmir')
def fmir():
    return render_template('vesti.html', posts=fmirPosts(), naslov='Finansijski menadžment i računovodstvo')

@app.route('/num')
def num():
    return render_template('vesti.html', posts=numPosts(), naslov='Numerička analiza')

@app.route('/dms')
def dms():
    return render_template('vesti.html', posts=dmsPosts(), naslov='Diskretne matematičke strukture')

if __name__ == "__main__":
    app.run(debug=True)