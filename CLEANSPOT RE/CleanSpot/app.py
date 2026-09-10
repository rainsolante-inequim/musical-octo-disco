from flask import Flask, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'CleanSpot'

msql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html') 


@app.route('/checker', methods=['GET', 'POST'])
def checker():
    return render_template('checker.html') #result= will be added once the query is written

    #   Data passed to template: 'result' — a list of matching waste
    #   items from the database, or None if the form hasn't been
    #   submitted yet.
    #   HTML writer needs: a search <form method="POST"> with an
    #   input named "item", and a loop to display 'result' if it exists.

@app.route('/guide')
def guide():
    return render_template('guide.html') # wastes= will be added once the query is written
    # URL: /guide
    # Template needed: guide.html
    # Data passed to template: 'wastes' — full list of all waste
    # items in the database, for browsing without searching.
    # HTML writer needs: a table/list that loops through 'wastes'.

@app.route('/report', methods=['GET', 'POST'])
def report_waste():
    return render_template('report.html')
# URL: /report
# Template needed: report.html
# Data passed to template: none on GET; on POST, redirects back
#   here with a flash message ("Report submitted successfully").
# HTML writer needs: a <form method="POST" enctype="multipart/form-data">
#   with inputs named "waste_type", "location", "description", "image".

@app.route('/admin/reports')
def admin_reports():
    return render_template('admin_reports.html') #reports= will be added once the query is written
# URL: /admin/reports
# Template needed: admin_reports.html
# Data passed to template: 'reports' — list of all submitted
# waste reports from the database.
# HTML writer needs: a table that loops through 'reports'.

@app.route('/admin/stats')
def admin_stats():
    return render_template('admin_stats.html')
# URL: /admin/stats
# Template needed: admin_stats.html
# Data passed to template: 'total_reports', 'waste_stats',
# 'location_stats' — counts grouped by type/location.
# HTML writer needs: cards/tables to display these three values.



if __name__=='__main__':
    app.run(debug=True)