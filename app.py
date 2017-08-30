# coding: utf-8

from datetime import datetime

from flask import Flask
from flask import render_template
from apis.tag import tag_apis

app = Flask(__name__)
app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

# 标签 apis
app.register_blueprint(tag_apis, url_prefix='/tag')

@app.route('/')
def index():
  return render_template('index.jade')
