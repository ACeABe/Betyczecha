from flask import Flask, render_template, request, redirect, session, send_file
from analyzer import analyze_matches, fetch_latest_matches, get_recent_matches_plot, save_user_pick, export_user_picks
import os

app = Flask(__name__)
app.secret_key = 'tajny_klucz'

@app.route('/', methods=['GET', 'POST'])
def home():
    if 'username' not in session:
        return redirect('/login')

    fetch_latest_matches()
    recommendation = analyze_matches()
    get_recent_matches_plot()

    if request.method == 'POST':
        team = request.form['team']
        date = request.form['date']
        odds = float(request.form['odds'])
        pick = request.form['pick']
        save_user_pick(session['username'], team, date, odds, pick)

    return render_template('index.html', recommendation=recommendation, username=session['username'], chart_url='static/form_chart.png')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect('/')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

@app.route('/export')
def export():
    if 'username' not in session:
        return redirect('/login')
    filepath = export_user_picks(session['username'])
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
