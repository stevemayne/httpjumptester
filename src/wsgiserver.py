"""
Simple multithreaded WSGI HTTP server.
"""

from wsgiref.simple_server import make_server, WSGIServer
from SocketServer import ThreadingMixIn

class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    daemon_threads = True

class Server:
    def __init__(self, wsgi_app, listen='0.0.0.0', port=8080):
        self.wsgi_app = wsgi_app
        self.listen = listen
        self.port = port
        self.server = make_server(self.listen, self.port, self.wsgi_app,
                                  ThreadingWSGIServer)

    def serve_forever(self):
        self.server.serve_forever()