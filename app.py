"""
app.py 
"""
#!/usr/bin/env python

from flask import Flask, request, make_response #, redirect, url_for
from flask import render_template

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """Main page."""
    html = render_template("index.html")
    response = make_response(html)

    return response
