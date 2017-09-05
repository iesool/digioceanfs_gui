#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import re
import subprocess
import simplejson

currpath = os.path.join(os.getcwd(),os.path.dirname(__file__))
if currpath not in sys.path:
    sys.path.append(currpath)
from base import Page,stow,session,web,_
import settings
from libcommon import clusnodelib

class clusterlicense(Page):
    def _logic(self):
        self.content = stow({

        })
        self.setup = stow({
            'template':'clusterlicense'
        })

    def GET(self):
        return self.render()

class clustergetnodelist(Page):
    def _action(self):
        nodelist = []
        nodelist = clusnodelib.func_node_list_all(False)
        print >> sys.stderr, nodelist 
        return simplejson.dumps(nodelist)
    def POST(self):
        return self.action(ajax=True)

class clustergetdeviceid(Page):
    def _action(self):
        device_id = ''
        params = web.input()
        #nodename = params['nodename'] 
        nodename = 'node-1'
        device_id = clusnodelib.func_node_get_device_id(nodename)
        return device_id
    def POST(self):
        return self.action(ajax=True)

class clusterchecklicense(Page):
    def _action(self):
        params = web.input()
        nodename = params['nodename']
        nodelicense = params['license']
        retcode = clusnodelib.func_node_check_license(nodename, nodelicense)
        return retcode
    def POST(self):
        return self.action(ajax=True)

class clustergetprocessing(Page):
    def _action(self):
        process_word = clusnodelib.func_node_processing()
        print >> sys.stderr, _(process_word.strip())
        return _(process_word.strip())
    def POST(self):
        return self.action(ajax=True)

class clusterchecksession(Page):
    def _action(self):
        print >> sys.stderr, session.user.id
        if not session.user.id:
            return 'session expired' 
        else:
            return 0
    def POST(self):
        return self.action(ajax=True)
    
