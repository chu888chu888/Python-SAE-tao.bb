#!/usr/bin/env python
#coding: utf-8
# vim: ai ts=4 sts=4 et sw=4 ft=python

import sys
from bottle import route, run, static_file, request ,abort, redirect, response, error

from base62 import base62_encode, base62_decode
from hashlib import md5
from url_uniq import url_uniq
from SAEKVDBPlugin import SAEKVDBPlugin
from qrcode import make as makeqrcode
from StringIO import StringIO
#from short_rewriter import real_url

#MAX = 62 ** 5
MAX = 916132832

def hashto62(url):
	m = md5()
	m.update(url)
	return int(m.hexdigest(), 16) % MAX

kv_plugin = SAEKVDBPlugin()

@error(404)
@route('/')
def index(error = None):
    return static_file('taobb.html', root='.')

@route('/favicon.ico')
def notfound():
    redirect('http://www.taobao.com/favicon.ico', 302)

@route('/<key>', apply=[kv_plugin])
def url(key, kv):
    #if request.get_header('Host' , 'tao.bb') != 'tao.bb':
    	#abort(404, "NOT FOUND")

    key = key.strip('/')
    if len(request.query) == 0 and len(key) == 5:
        url = kv.get(key)
	if url:
	    redirect(url)

    abort(404, "NOT FOUND")


@route('/<key>/real', apply=[kv_plugin])
def qrcode(key, kv):
    if len(request.query) == 0 and len(key) == 5:
        url = kv.get(key)
	if url:
	    return url + "\n"

    abort(404, "NOT FOUND")

@route('/<key>/qrcode', apply=[kv_plugin])
@route('/<key>/qrcode.png', apply=[kv_plugin])
def qrcode(key, kv):
    if len(request.query) == 0 and len(key) == 5:
        url = kv.get(key)
	if url:
	    response.content_type = 'image/png'
	    img = makeqrcode(url)
	    output = StringIO()
	    img.save(output,'PNG')
	    contents = output.getvalue()
	    output.close()
	    return contents
	
    abort(404, "NOT FOUND")

@route('/d/save', method='POST', apply=[kv_plugin])
def save(kv):
    key = None
    err = None

    url = request.forms['url']
    if url:
        url = url_uniq(url)
        if url:
            code = hashto62(url)

            key = base62_encode(code)

            if not kv.set(key, url):
                err = '内部错误'

        else:
            err = '请输入有效的 URL'

    else:
        err = '请输入URL'

    return {'key':key, 'err':err }

@route('/d/long', method='POST')
def longurl():
    wanted = request.forms['url']
    longurl = None
    if wanted and len(wanted) < 25:
        if not wanted.startswith('http://'):
	    wanted = 'http://' + wanted
	
	#longurl = real_url(wanted)

    return { 'wanted':wanted,  'long': longurl}

if __name__ == '__main__':
    debug = False
    if len(sys.argv) > 0:
        debug = True
    run(host='localhost', port=8008, debug=debug)
