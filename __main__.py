#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 
# (c) Roberto Gambuzzi
# Creato:          13/02/2012 11:44:21
# Ultima Modifica: 13/02/2012 11:44:21
# 
# v 0.0.1.0
# 
# file: /root/vboxmanager/__main__.py
# auth: Roberto Gambuzzi <gambuzzi@gmail.com>
# desc: 
# 
# $Id: __main__.py 13/02/2012 11:44:21 Roberto $
# --------------

from bottle import route, run

@route('/hello')
@route('/hello/:name')
def index(name='World'):
    return '<b>Hello %s!</b>' % name

run(host='192.168.1.70', port=8008)
