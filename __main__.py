#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 
# (c) Roberto Gambuzzi
# Creato:          13/02/2012 11:44:21
# Ultima Modifica: 13/02/2012 16:54:22
# 
# v 0.0.1.1
# 
# file: /root/vboxmanager/__main__.py
# auth: Roberto Gambuzzi <gbinside@gmail.com>
# desc: 
# 
# $Id: __main__.py 13/02/2012 16:54:22 Roberto $
# --------------

import sys
from time import sleep
from bottle import route, run, redirect, response
from vboxapi import VirtualBoxManager

virtualBoxManager = VirtualBoxManager('XPCOM', None)
virtualBox = virtualBoxManager.vbox

@route('/')
def index():
    ret = []
    machines = virtualBox.getMachines()
    for machine in machines:
        machineName = machine.name
        machineStatus = "null"
        machineStatuses = {
                0: 'null',
                1: 'powered off <a href="/start/%(name)s">START</a>',
                2: 'saved <a href="/start/%(name)s">START</a>',
                3: 'teleported',
                4: 'aborted <a href="/start/%(name)s">START</a>',
                5: 'running <a href="/savestate/%(name)s">SAVE</a> <a href="/stop/%(name)s">STOP</a>',
                6: 'paused <a href="/start/%(name)s">START</a>',
                7: 'stuck',
                8: 'teleporting',
                9: 'live snapshotting',
                10: 'starting',
                11: 'stopping',
                12: 'saving',
                13: 'restoring'
                 }
        machineStatus = machineStatuses.get(machine.state)
        if '%(name)s' in machineStatus:
            machineStatus = machineStatus % {'name':machineName}
        ret.append ( "<li><a href=\"/sshot/%s\"><img src=\"/sshot/%s/200/150\" /></a> " % (machineName,machineName) +machineName + " - " + machineStatus+" - "+str(machine.memorySize)+"mem - " +str(machine.CPUCount)+"cpus </li>")
    return '<meta http-equiv="refresh" content="5"><ul>%s</ul>' % (''.join(ret))

@route('/start/:name')
def start(name=None):
    if name:
        machine = virtualBox.findMachine(name)
        session = virtualBoxManager.mgr.getSessionObject(virtualBox)
        prog = machine.launchVMProcess(session,"headless","")
        if prog:        
            prog.waitForCompletion(5000)
    redirect('/')

@route('/savestate/:name')
def savestate(name=None):
    if name:
        machine = virtualBox.findMachine(name)        
        session = virtualBoxManager.mgr.getSessionObject(virtualBox)
        machine.lockMachine(session, 1)
        prog = session.console.saveState()
        if prog:
            prog.waitForCompletion(5000)
        session.unlockMachine()
    redirect('/')

@route('/stop/:name')
def stop(name=None):
    if name:
        machine = virtualBox.findMachine(name)
        session = virtualBoxManager.mgr.getSessionObject(virtualBox)
        machine.lockMachine(session, 1)
        prog = session.console.powerButton()
        if prog:
            prog.waitForCompletion(5000)
        session.unlockMachine()
    redirect('/')

@route('/sshot/:name')
@route('/sshot/:name/:x/:y')
def screen_shot(name=None,x=800,y=600):
    response.content_type = "image/png"
    img = '\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00\x10\x08\x06\x00\x00\x00w\x00}Y\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x06bKGD\x00\xff\x00\xff\x00\xff\xa0\xbd\xa7\x93\x00\x00\x00\tpHYs\x00\x00\x0b\x13\x00\x00\x0b\x13\x01\x00\x9a\x9c\x18\x00\x00\x00\x07tIME\x07\xdc\x02\r\x11\x085\xa2\x0cz%\x00\x00\x00\x1diTXtComment\x00\x00\x00\x00\x00Created with GIMPd.e\x07\x00\x00\x00\xd4IDATH\xc7\xed\xd4MJBQ\x18\xc6\xf1_\x91Pk\xb0F\x96\x13/\x96k\x11\x02\x17\x91-\xc1U\xb4\x85t\x11\xb5\x10\xa7\nv\xb3yA\x93\xdb\xe4-\xa4\x0f\xcfM=3\x1f8\x9c\xaf?/\xcf\x81\xf3>\xec\xf5S]\xdcc\x81\xf7\x98\xc7\xb8\xfc\x85\xad\xd6\x8c\xff0_\xba\xc63nq\x86\x06N1D\x19\xf7\xdf\r\xa4T\xd5}\xf99\x96(\xfe\xb8/\xf0\x12\\\x16\x03w\x18%\x98QpY\x0cL\xd1I0EpY\x0c\xbc\xe18\xc1\x9c\xe0\xb5\xc6\x07S\x979\xdaA\xd7\x1cl\xc3\x1c\xae\xacgh%\n\xb50\xdfe\xcf\xaf\x1axD?\xc1\xf7\xf1\x90+\x80\xda\xd1f\xa96\xbc\xc8\xf5\ta\x10A4\x8c\x00j\xa0\x89\x9b8\x1f\xe4\x0c\xa2O]a\x82\xa7\x88\xe22\xf6\xbd\r\x8bW\xf6Z\xa3\x0f\x16<GG7x$\xe1\x00\x00\x00\x00IEND\xaeB`\x82'
    if name:
        machine = virtualBox.findMachine(name)
        session = virtualBoxManager.mgr.getSessionObject(virtualBox)
        machine.lockMachine(session, 1)
        try:
            display = session.console.display 
            img = display.takeScreenShotPNGToArray(0,x,y)
        #img = '<img alt="Embedded Image" src="data:image/png;base64,' + \
        #       img.encode('base64') + '" />'
        except:
            pass
        session.unlockMachine()
    return img

if __name__=="__main__":
    run(host='192.168.1.70', port=8008 , reloader=True, quiet=True)
