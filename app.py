from flask import Flask, render_template
from analyzer import analyze_matches, fetch_latest_matches, get_recent_matches_plot

app = Flask(__name__)

@app.route('/')
def home():
    fetch_latest_matches()
    recommendation = analyze_matches()
    get_recent_matches_plot()
    return render_template('index.html', recommendation=recommendation, chart_url='static/form_chart.png')

if __name__ == '__main__':
    app.run(debug=True)
