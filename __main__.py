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
    return '<ul>%s</ul>' % (''.join(ret))

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
    img = 'base64,'
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
