# coding: utf-8
from flask import Blueprint, render_template, request, jsonify
import leancloud, apis
from apis.tag import Tag

class Wallpaper(leancloud.Object):
  pass
class WallpaperTags(leancloud.Object):
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

  ls = Wallpaper.query.include('user').equal_to('status', status).add_descending('createdAt').skip(rows * page).limit(rows).find()
  data = map(lambda item: {
    'id': item.id,
    'user': {'id': item.get('user').id, 'nickname': item.get('user').get('nickname')},
    'tags': map(lambda wpt: {'id': wpt.get('tag').id, 'name': wpt.get('tag').get('name')}, WallpaperTags.query.include('tag').equal_to('wallpaper', item).find()),
    'name': item.get('name'),
    'image': {'id': item.get('image').id, 'url': item.get('image').get_thumbnail_url(width = 90, height = 160, scale_to_fit = False), 'origin_url': item.get('image').url},
    'status': item.get('status'),
    'price': item.get('price'),
    'createdAt': item.get('createdAt').strftime('%Y-%m-%d %H:%M:%S')
  }, ls)
  return jsonify({'status': 0, 'data': data, 'count': Wallpaper.query.equal_to('status', status).count()})

@wallpaper_apis.route('/update', methods = ['POST'])
def update():
  ps = request.json
  if ps.has_key('id'):
    wp = Wallpaper.query.get(ps['id'])
  else:
    wp = Wallpaper()
    wp.set('comment_count', 0)
    wp.set('favorite_count', 0)
    wp.set('download_count', 0)
  if not apis.isNone(ps, 'user'): wp.set('user', leancloud.User.create_without_data(ps['user']['id']))
  wp.set('status', ps['status'] if ps.has_key('status') else 0)
  if ps.has_key('name'): wp.set('name', ps['name'])
  if ps.has_key('price'): wp.set('price', ps['price'])
  if ps.has_key('image'):
    img = leancloud.File.create_without_data(ps['image']['id'])
    img.fetch()
    wp.set('image', img)
    wp.set('width', img.metadata['width'])
    wp.set('height', img.metadata['height'])
    wp.set('size', img.metadata['size'])
  if not apis.isNone(ps, 'tags'):
    ls = WallpaperTags.query.equal_to('wallpaper', wp).find()
    leancloud.Object.destroy_all(ls)
    tags = ''
    for tag in ps['tags']:
      t = Tag.create_without_data(tag['id'])
      t.fetch()
      tags += t.get('name') if tags == '' else ',' + t.get('name')
      wpt = WallpaperTags()
      wpt.set('wallpaper', wp)
      wpt.set('tag', t)
      wpt.save()
    wp.set('tags', tags)
  wp.save()
  return fetch()
