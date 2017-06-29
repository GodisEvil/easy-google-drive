#!python
#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


if __name__ == '__main__':
    from webServ import app
    if len(sys.argv) > 1 and sys.argv[1] == '-t':
        app.run('0.0.0.0', 9999, debug=True)
    else:
        from gevent.pywsgi import WSGIServer
        app.debug = True
        httpServer = WSGIServer(('0.0.0.0', 9999), app)
        httpServer.serve_forever()
