from flask import Blueprint, render_template, request, jsonify
import leancloud

class Tag(leancloud.Object):
  pass
tag_apis = Blueprint('tag_apis', __name__)

@tag_apis.route('/')
def tag():
  return render_template('tag.jade')

@tag_apis.route('/fetch', methods = ['POST', 'GET'])
def fetch():
  if request.method == 'POST':
    rows = int(request.json['rows'])
    page = int(request.json['page'])
  else:
    rows = int(request.args.get('rows'))
    page = int(request.args.get('page'))

  ls = Tag.query.add_descending('createdAt').skip(rows * page).limit(rows).find()
  data = map(lambda item: {
    'id': item.id,
    'name': item.get('name'),
    'cover': item.get('cover').url,
    'tag': {
      'id': item.get('tag').id,
      'name': item.get('tag').get('name'),
      'cover': item.get('tag').get('cover').url,
    } if item.get('tag') != None else None
  }, ls)
  return jsonify({'status': 0, 'data': data, 'count': Tag.query.count()})