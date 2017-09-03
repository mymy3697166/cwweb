# coding: utf-8
from flask import Blueprint, render_template, request, jsonify
import leancloud, apis

class Wallpaper(leancloud.Object):
  pass
wallpaper_apis = Blueprint('wallpaper_apis', __name__)

@wallpaper_apis.route('/')
def wallpaper():
  return render_template('wallpaper.jade')

@wallpaper_apis.route('/fetch', methods = ['POST'])
def fetch():
  rows = int(request.json['rows'])
  page = int(request.json['page'])
  status = int(request.json['sstatus'])

  query = Wallpaper.query
  query.equal_to('status', status)
  ls = query.add_descending('createdAt').skip(rows * page).limit(rows).find()
  data = map(lambda item: {
    'id': item.id,
    'name': item.get('name'),
    'image': {'id': item.get('image').id, 'url': item.get('image').get_thumbnail_url(height = 128), 'origin_url': item.get('image').url},
    'status': item.get('status'),
    'price': item.get('price'),
    'createdAt': item.get('createdAt').strftime('%Y-%m-%d %H:%M:%S')
  }, ls)
  return jsonify({'status': 0, 'data': data, 'count': Wallpaper.query.count()})

@wallpaper_apis.route('/update', methods = ['POST'])
def update():
  ps = request.json
  if ps.has_key('id'):
    wp = Wallpaper.query.get(ps['id'])
  else:
    wp = Wallpaper()
  wp.set('status', ps['status'] if ps.has_key('status') else 0)
  if ps.has_key('name'): wp.set('name', ps['name'])
  if ps.has_key('price'): wp.set('price', ps['price'])
  if ps.has_key('image'): wp.set('image', leancloud.File.create_without_data(ps['image']['id']))
  wp.save()
  return fetch()
