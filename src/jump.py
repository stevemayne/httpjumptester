#!/usr/bin/env python
import bottle
from bottle import request, route, run, template
import urllib2
import os

bottle.TEMPLATE_PATH.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'views'))

our_name = os.environ.get('IDENTIFIER', 'Unnamed')

def get_remote_ip():
    request.environ.get('HTTP_X_FORWARDED_FOR') or request.environ.get('REMOTE_ADDR')

def do_next_hop(host, hops, timeout=5):
    url = 'http://{0}/jump/'.format(host)
    if hops:
        url += '/'.join(hops) + '?timeout={0}'.format(timeout-1)
    try:
        response = urllib2.urlopen(url, timeout=timeout)
        return template('jump_success', response=response.read(), host=host, name=our_name)
    except Exception as e:
        return template('jump_error', error=str(e), host=host, name=our_name)

@route('/')
def identify():
    return template('id_display', name=our_name)

@route('/jump/')
def jump_terminator():
    client_ip = get_remote_ip()
    return template('termination', name=our_name, ip=client_ip)

@route('/jump/<hoproute:path>')
def jump(hoproute):
    try:
        timeout = int(request.query.timeout) or 10
    except ValueError:
        timeout = 10
    
    hops = hoproute.split('/')
    if hops:
        next_hop = hops[0]
        hops = hops[1:]
        return do_next_hop(next_hop, hops, timeout=timeout)
    else:
        client_ip = get_remote_ip()
        return template('termination', name=our_name, ip=client_ip)
    
if __name__ == '__main__':
    run(host='0.0.0.0', port=8080)
    
    
