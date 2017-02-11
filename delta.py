# -*- coding: utf-8 -*-
import os
import urllib.request
import urllib.parse
from pyquery import PyQuery as pq

HOST = os.getenv('DELTA_HOST')
LANG = 'ja'

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.73',
}


def _http_get(url):
    req = urllib.request.Request(url, headers=REQUEST_HEADERS)
    return urllib.request.urlopen(req)


def _http_get_text(url):
    return _http_get(url).read().decode('utf-8')


def get_image_url(post_id):
    url = '{}/{}/post/show/{}'.format(HOST, LANG, post_id)
    html = pq(_http_get_text(url))
    image_url = html('#image').attr('src')
    return 'https:' + image_url


def get_image_response(post_id):
    image_url = get_image_url(post_id)
    return _http_get(image_url)


def search(keyword, page=1):
    url = '{}/{}/post/index.content?{}'.format(HOST, LANG, urllib.parse.urlencode({'tags': keyword, 'page': page}))
    html = pq(_http_get_text(url))
    result = []
    for post in [pq(elem) for elem in html('.thumb')]:
        result.append({
            'id': post.attr('id').lstrip('p'),
            'tags': post.find('.preview').eq(0).attr('title').split(' '),
            'thumbnail_url': 'https:' + post.find('.preview').eq(0).attr('src'),
        })
    return result

