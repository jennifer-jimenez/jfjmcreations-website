"""
app.py 
"""
#!/usr/bin/env python

from flask import Flask, request, make_response #, redirect, url_for
from flask import render_template

from spotify import get_top_content, ContentItem

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """Main page."""
    content = get_top_content("6vm278XNbcMlxfthkeJpw2")

    html = render_template("index.html", results=content)
    response = make_response(html)

    return response
