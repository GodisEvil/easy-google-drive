#!python
#-*- coding: utf-8 -*-
'''
    url
'''

from webServ import app, request
from gdapi.api import driver, AuthError
from cm.myJsonEncoder import MyJsonEncode
import json
import os
import logging

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return 'Hello world'

def output(data):
    ## add headers
    return (json.dumps(data, ensure_ascii=False, cls=MyJsonEncode), 200, {'Access-Control-Allow-Origin': '*'})

@app.route('/auth/get_uri')
def getAuthUri():
    return output({'code': 0, 'uri': driver.getAuthUri()})


@app.route('/auth/auth')
def auth():
    code = request.args.get('code', '')
    if not code.strip():
        return output({'code': 1, 'msg': 'must special code'})
    try:
        ret = driver.auth(code)
    except AuthError, e:
        return output({'code': 2, 'msg': str(e)})
    except Exception, e2:
        return output({'code': 3, 'msg': str(e2)})
    return output({'code': 0, 'ret': ret})

@app.route('/config/about')
def about():
    try:
        ret = driver.about()
    except AuthError, e:
        return output({'code': 2, 'msg': str(e)})
    except Exception, e2:
        return output({'code': 3, 'msg': str(e2)})
    return output({'code': 0, 'ret': ret})

@app.route('/file/upload')
def upload():
    lpath = request.args.get('lpath', '')
    rname = request.args.get('rname', '')
    parentId = request.args.get('parent', '')
    if not lpath.strip() or not parentId.strip():
        return output({'code': 1, 'msg': 'must special lpath and parent'})
    if not rname.strip():
        rname = os.path.basename(lpath)
    try:
        ret = driver.uploadFile(lpath, parentId, rname)
    except AuthError, e:
        return output({'code': 2, 'msg': str(e)})
    except Exception, e2:
        return output({'code': 3, 'msg': str(e2)})
    return output({'code': 0, 'ret': ret})


@app.route('/dir/create')
def makeDir():
    dname = request.args.get('dname')
    pname = request.args.get('parent')
    if not dname or not pname:
        return output({'code': 1, 'msg': 'must special dname and parent'})
    try:
        ret = driver.mkDir(dname, pname)
    except Exception, e:
        return output({'code': 2, 'msg': str(e)})
    return output({'code': 0, 'ret': ret})


@app.route('/dir/list')
def listDir():
    dname = request.args.get('dname')
    if not dname:
        return output({'code': 1, 'msg': 'must special dname and parent'})
    try:
        ret = driver.listDir(dname)
    except Exception, e:
        return output({'code': 2, 'msg': str(e)})
    return output({'code': 0, 'ret': ret})


@app.route('/file/info')
def infoFile():
    fid = request.args.get('fid', '')
    if not fid.strip():
        return output({'code': 1, 'msg': 'must special fid'})
    fileobj = driver.infoFile(fid)
    return output({'code': 0, 'data': fileobj})

