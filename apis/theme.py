# coding: utf-8
from flask import Blueprint, render_template, request, jsonify
import leancloud, apis
from apis.wallpaper import Wallpaper
from apis.tag import Tag

class Theme(leancloud.Object):
  pass
class ThemeWallpapers(leancloud.Object):
  pass
theme_apis = Blueprint('theme_apis', __name__)

@theme_apis.route('/')
def theme():
  return render_template('theme.jade')

@theme_apis.route('/fetch', methods = ['POST'])
def fetch():
  rows = int(request.json['rows'])
  page = int(request.json['page'])
  status = int(request.json['sstatus'])

  ls = Theme.query.include('user').equal_to('status', status).add_descending('createdAt').skip(rows * page).limit(rows).find()
  data = map(lambda item: {
    'id': item.id,
    'user': {'id': item.get('user').id, 'nickname': item.get('user').get('nickname')},
    'name': item.get('name'),
    'cover': {'id': item.get('cover').id, 'url': item.get('cover').get_thumbnail_url(width = 160, height = 90, scale_to_fit = False), 'origin_url': item.get('cover').url},
    'description': item.get('description'),
    'status': item.get('status'),
    'createdAt': item.get('createdAt').strftime('%Y-%m-%d %H:%M:%S')
  }, ls)
  return jsonify({'status': 0, 'data': data, 'count': Theme.query.equal_to('status', status).count()})

@theme_apis.route('/update', methods = ['POST'])
def update():
  ps = request.json
  if ps.has_key('id'):
    te = Theme.query.get(ps['id'])
  else:
    te = Theme()
    te.set('comment_count', 0)
    te.set('browse_count', 0)
  if not apis.isNone(ps, 'user'): te.set('user', leancloud.User.create_without_data(ps['user']['id']))
  te.set('status', ps['status'] if ps.has_key('status') else 0)
  if ps.has_key('name'): te.set('name', ps['name'])
  if ps.has_key('description'): te.set('description', ps['description'])
  if ps.has_key('cover'): te.set('cover', leancloud.File.create_without_data(ps['cover']['id']))
  te.save()
  return fetch()

@theme_apis.route('/fetch_wps', methods = ['POST'])
def fetch_wps():
  rows = int(request.json['rows'])
  page = int(request.json['page'])

  theme = Theme.query.get(request.json['id'])
  ls = ThemeWallpapers.query.include('wallpaper').equal_to('theme', theme).add_descending('createdAt').skip(rows * page).limit(rows).find()
  data = map(lambda item: {
    'id': item.id,
    'name': item.get('wallpaper').get('name'),
    'image': item.get('wallpaper').get('cover').get_thumbnail_url(width = 90, height = 160, scale_to_fit = False),
    'createdAt': item.get('createdAt').strftime('%Y-%m-%d %H:%M:%S')
  }, ls)
  return jsonify({'status': 0, 'data': data, 'count': ThemeWallpapers.query.equal_to('theme', theme).count()})

@theme_apis.route('/search_wps', methods = ['POST'])
def search_wps():
  rows = int(request.json['rows'])
  page = int(request.json['page'])
  key = request.json['key'] if request.json.has_key('key') else ''

  if key == '':
    ls = ThemeWallpapers.query.equal_to('status', 0).add_descending('createdAt').limit(20).find()
  else:
    ls = leancloud.Query.do_cloud_query("select id, name, image from Wallpaper where name like '%?%' or id in (select wallpaper from WallpaperTags where tag in(select id from Tag where name like '%?%'))", key, key).results
  data = map(lambda item: {
    'id': item.id,
    'name': item.get('wallpaper').get('name'),
    'image': item.get('wallpaper').get('cover').get_thumbnail_url(width = 90, height = 160, scale_to_fit = False)
  }, ls)
  return jsonify({'status': 0, 'data': data, 'count': ThemeWallpapers.query.equal_to('theme', theme).count()})

@theme_apis.route('/remove_wp', methods = ['POST'])
def remove_wp():
  twp = ThemeWallpapers.query.get(request.json['twp_id'])
  twp.destroy()
  return fetch_wps()

@theme_apis.route('/add_wp', methods = ['POST'])
def add_wp():
  theme = Theme.query.get(request.json['theme'])
  wallpaper = Wallpaper.query.get(request.json['wallpaper'])
  count = ThemeWallpapers.query.equal_to('theme', theme).equal_to('wallpaper', wallpaper).find().count()
  if count == 0:
    twp = ThemeWallpapers()
    twp.theme = theme
    twp.wallpaper = wallpaper
    twp.save()
  else:
    return jsonify({'status': 1})
  return fetch_wps()