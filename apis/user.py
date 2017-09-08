# coding: utf-8
from flask import Blueprint, request, jsonify
from leancloud import Query, User

user_apis = Blueprint('user_apis', __name__)

@user_apis.route('/fetch_default', methods = ['POST'])
def fetch_default():
  ls = Query.or_(User.query.equal_to('type', 1), User.query.equal_to('type', 99)).find()
  data = map(lambda item: {
    'id': item.id,
    'nickname': item.get('nickname')
  }, ls)
  return jsonify({'status': 0, 'data': data})