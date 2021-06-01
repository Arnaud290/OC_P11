import json
from flask import Flask,render_template,request,redirect,flash,url_for
from datetime import datetime

def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary',methods=['POST'])
def showSummary():
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
    except IndexError:
        flash("Wrong email")
        return redirect(url_for('index'))
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    date_now = datetime.today()
    date_event = datetime.strptime(foundCompetition['date'], "%Y-%m-%d %H:%M:%S")
    if foundClub and foundCompetition and date_now < date_event:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Event is too old!")
        return render_template('welcome.html', club=foundClub, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    club['points'] = int(club['points'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])
    if  placesRequired > int(club['points']):
        flash('Too points are allowed!')
    elif placesRequired > 12:
        flash('No more than 12 places per booking!')
    else:
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        club['points'] = int(club['points']) - placesRequired
        flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/clubsPoints')
def clubsPoints():
    return render_template('pointsDisplay.html', clubs=clubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))