# coding: utf-8
from flask import Blueprint, request, jsonify
import leancloud

user_apis = Blueprint('user_apis', __name__)

@user_apis.route('/fetch_default', methods = ['POST'])
def fetch_default():
  ls = leancloud.User.query.equal_to('type', 1).find()
  data = map(lambda item: {
    'id': item.id,
    'nickname': item.get('nickname')
  }, ls)
  return jsonify({'status': 0, 'data': data})