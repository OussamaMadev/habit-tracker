from flask import Flask, render_template, request, redirect, url_for
import csv
import pandas as pd

app = Flask(__name__)
CSV_FILE = 'data.csv'

@app.route('/')
def home():
    return redirect(url_for('table'))

@app.route('/table')
def table():
    with open(CSV_FILE, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    headers = data[0]
    rows = data[1:]
    return render_template('table.html', headers=headers, rows=rows)

@app.route('/save', methods=['POST'])
def save():
    headers = request.form.getlist('headers')
    cells = request.form.getlist('cell')
    rows = int(request.form['rows'])
    cols = int(request.form['cols'])

    table = [headers]
    for i in range(rows):
        row = cells[i * cols:(i + 1) * cols]
        table.append(row)

    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(table)

    return redirect(url_for('table'))

@app.route('/stats')
def stats():
    df = pd.read_csv(CSV_FILE)
    desc = df.describe(include='all').fillna("").to_html(classes="stats-table")
    return render_template('stats.html', table=desc)

if __name__ == '__main__':
    app.run(debug=True)
