# coding: utf-8
import time, leancloud
from StringIO import StringIO
from PIL import Image
from flask import Flask
from flask import render_template, request
from apis.tag import tag_apis
from apis.wallpaper import wallpaper_apis
from apis.user import user_apis
from apis.theme import theme_apis

app = Flask(__name__)
app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

# 注册路由
app.register_blueprint(tag_apis, url_prefix = '/tag')
app.register_blueprint(wallpaper_apis, url_prefix = '/wallpaper')
app.register_blueprint(user_apis, url_prefix = '/user')
app.register_blueprint(theme_apis, url_prefix = '/theme')

@app.route('/')
def index():
  return render_template('index.jade')

@app.route('/upload', methods = ['POST'])
def upload():
  fn = '%s.jpg'%str(int(time.time() * 1000))
  io = StringIO()
  io.write(request.files['file'].read())
  size = Image.open(io).size
  file = leancloud.File(fn, io)
  file.metadata['width'] = size[0]
  file.metadata['height'] = size[1]
  file.save()
  io.close()
  return '{"status": 0, "url": "%s", "id": "%s"}'%(file.url, file.id)

@app.route('/login')
def login():
  return render_template('login.jade')
