# coding: utf-8
from flask import Blueprint, render_template, request, jsonify
import leancloud, apis

class Tag(leancloud.Object):
  pass
tag_apis = Blueprint('tag_apis', __name__)

@tag_apis.route('/')
def tag():
  return render_template('tag.jade')

@tag_apis.route('/fetch', methods = ['POST'])
def fetch():
  rows = int(request.json['rows'])
  page = int(request.json['page'])
  status = int(request.json['sstatus'])

  query = Tag.query
  query.equal_to('status', status)
  query.include('tag.name')
  ls = query.add_descending('createdAt').skip(rows * page).limit(rows).find()
  data = map(lambda item: {
    'id': item.id,
    'name': item.get('name'),
    'cover': {'id': item.get('cover').id, 'url': item.get('cover').get_thumbnail_url(width = 128, height = 64), 'origin_url': item.get('cover').url},
    'status': item.get('status'),
    'description': item.get('description'),
    'tag': {'id': item.get('tag').id, 'name': item.get('tag').get('name')} if item.get('tag') != None else None,
    'createdAt': item.get('createdAt').strftime('%Y-%m-%d %H:%M:%S')
  }, ls)
  return jsonify({'status': 0, 'data': data, 'count': Tag.query.count()})

@tag_apis.route('/fetch_tags', methods = ['POST'])
def fetch_tags():
  ls = Tag.query.equal_to('status', 0).find()
  data = map(lambda item: {
    'id': item.id,
    'name': item.get('name')
  }, ls)
  return jsonify({'status': 0, 'data': data})

@tag_apis.route('/update', methods = ['POST'])
def update():
  ps = request.json
  if ps.has_key('id'):
    tag = Tag.query.get(ps['id'])
  else:
    tag = Tag()
  tag.set('status', ps['status'] if ps.has_key('status') else 0)
  if ps.has_key('name'): tag.set('name', ps['name'])
  if ps.has_key('description'): tag.set('description', ps['description'])
  if ps.has_key('cover'): tag.set('cover', leancloud.File.create_without_data(ps['cover']['id']))
  tag.set('tag', Tag.create_without_data(ps['tag']['id']) if not apis.isNone(ps, 'tag') else None)
  tag.save()
  return fetch()
