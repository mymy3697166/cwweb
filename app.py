# coding: utf-8

from datetime import datetime

from flask import Flask
from flask import render_template

app = Flask(__name__)

# 动态路由
# app.register_blueprint(todos_view, url_prefix='/todos')

@app.route('/')
def index():
  return render_template('index.html')
