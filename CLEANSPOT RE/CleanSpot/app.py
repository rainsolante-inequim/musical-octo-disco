from flask import Flask, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL
app = Flask(__name__)

@app.route('/')
def index():
    return 'hello'

if __name__=='__main__':
    app.run(debug=True)