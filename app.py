# coding: utf-8
import time, leancloud
from StringIO import StringIO
from flask import Flask
from flask import render_template, request
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

@app.route('/upload', methods = ['POST'])
def upload():
  fn = '%s.jpg'%str(int(time.time() * 1000))
  io = StringIO()
  io.write(request.files['file'].read())
  file = leancloud.File(fn, io)
  file.save()
  io.close()
  return '{"status": 0, "url": "%s", "id": "%s"}'%(file.url, file.id)