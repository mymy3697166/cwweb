from flask import Blueprint, render_template, request, jsonify
import leancloud

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
  ls = query.add_descending('createdAt').skip(rows * page).limit(rows).find()
  print ls
  data = map(lambda item: {
    'id': item.id,
    'name': item.get('name'),
    'cover': item.get('cover').get_thumbnail_url(width = 128, height = 64),
    'status': item.get('status'),
    'tag': {
      'id': item.get('tag').id,
      'name': item.get('tag').get('name'),
      'cover': item.get('tag').get('cover').get_thumbnail_url(width = 128, height = 64),
    } if item.get('tag') != None else None,
    'createdAt': item.get('createdAt').strftime('%Y-%m-%d %H:%M:%S')
  }, ls)
  return jsonify({'status': 0, 'data': data, 'count': Tag.query.count()})

@tag_apis.route('/update', methods = ['POST'])
def update():
  if request.json.has_key('id'):
    id = str(request.json['id'])
    tag = Tag.query.get(id)
  else:
    tag = Tag()
  if request.json.has_key('status'): tag.set('status', int(request.json['status']))
  if request.json.has_key('name'): tag.set('name', str(request.json['name']))
  if request.json.has_key('description'): tag.set('description', str(request.json['description']))
  if request.json.has_key('name'): tag.set('name', str(request.json['name']))
  return fetch()
