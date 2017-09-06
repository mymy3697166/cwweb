# coding: utf-8
from flask import Blueprint, render_template, request, jsonify
import leancloud, apis

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
