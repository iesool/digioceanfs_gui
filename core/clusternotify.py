#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import re
import subprocess
import simplejson
import traceback

from inotify_reports import *
import settings
import syslog
import traceback
from threading import Thread as th

currpath = os.path.join(os.getcwd(),os.path.dirname(__file__))
if currpath not in sys.path:
    sys.path.append(currpath)
from base import Page,stow,session,web,_
import settings

from libcommon import clusnotifylib

class Node(Page):
    def _checknode(self):
        if not session.runtime.node:
            raise web.seeother('/clusternotify')
        
class clusternotify(Page):
    def _logic(self):
        self.content = stow({

        })
        self.setup = stow({
            'template':'clusternotify',
            'breadcrumbs':['clusternotify']
        })

    def GET(self):
        return self.render()
    
class clusternotifyload(Page):
    def _logic(self):
        self.content = stow({
            'clusternotify':clusternotify
        })
        self.setup = stow({
            'template':'clusternotifyload'
            #'jstemplate':['datatable_ZH']
        })
    def GET(self):
        return self.render(ajax=True)
    
class clusternotifyinit(Page):
    def __init__(self):
        Page.__init__(self)
        try:
            th1 = th(target=self.inotify_th, name='inotify_th')
            th1.daemon = True
            th1.start()
        except Exception, e:
            print >> sys.stderr, e

    def _action(self):
        try:
            params = web.input()
            nowait = params['nowait']
            if nowait == 'false':
                ret = settings.rqueue.get()#timeout=100)
                settings.unreadlist.append(ret)
                #session._load()
                #session.global_v.rlist.append(ret)
                #session.global_v.new_msg_num += 1
            else:
                ret = settings.rqueue.get_nowait()
        except Exception,e:
            ret = None
        #return session.global_v.new_msg_num
        #return len(settings.unreadlist)
        session.global_v.new_msg_num = len(clusnotifylib.func_getMsg('new'))
        return len(clusnotifylib.func_getMsg('new'))

    def inotify_th(self):
        nty = notify(WATCH_DIR)
        nty.run()

    def POST(self):
        return self.action(ajax=True)

class clusternotifymsg(Page):
    def _action(self):
        msg_dict_list = []
        #node = session.runtime.node
        msglist = clusnotifylib.func_getMsg('all')
        msg_dict = clusnotifylib.func_getMsgContent(msglist)
        if len(msg_dict) == 1:
            if 'nofile' in msg_dict[0]:
                return simplejson.dumps(msg_dict)
        for d in msg_dict:
            msg_d = simplejson.loads(d['filecontent'])
            node = msg_d['ErrNode']
            if msg_d['OP'] == 'RaidEvent':
                msg_d['OP'] = _(msg_d['OP'])
                msg_d['RaidEvent'] = _(msg_d['RaidEvent'])
                if msg_d['RaidDisk']:
                    os.system("touch %s-%s" % (os.path.join(settings.err_disks_dir, node), msg_d['RaidDisk']))
            elif msg_d['OP'] == 'DiskEvent':
                msg_d['OP'] = _(msg_d['OP'])
                msg_d['DiskEvent'] = _(msg_d['DiskEvent'])
                if msg_d['DiskName']:
                    os.system("touch %s-%s" % (os.path.join(settings.err_disks_dir, node), msg_d['DiskName']))
                if msg_d['DiskEvent'] == _('remove'):
                    ret = os.system("rm %s-%s" % (os.path.join(settings.err_disks_dir, node), msg_d['DiskName']))
            elif msg_d['OP'] == 'FileSystemEvent':
                msg_d['OP'] = _(msg_d['OP'])
                msg_d['FileEvent'] = _(msg_d['FileEvent'])
                if msg_d['ErrDiskName']:
                    ret = os.system("touch %s-%s" % (os.path.join(settings.err_disks_dir, node), msg_d['ErrDiskName']))
            elif msg_d['OP'] == 'NetLink':
                msg_d['OP'] = _(msg_d['OP'])
                msg_d['Event'] = _(msg_d['Event'])
            elif msg_d['OP'] == 'Ping':
                msg_d['OP'] = _(msg_d['OP'])
                msg_d['Event'] = _(msg_d['Event'])
            else:
                pass  
            d['filecontent'] = simplejson.dumps(msg_d)
            msg_dict_list.append(d)          
        return simplejson.dumps(msg_dict_list)

    def POST(self):
        return self.action(ajax=True)

class clusternotifyfocus(Page):
    def _action(self):
        args = web.input()
        msg_id = args['msg_id']
        msglist = clusnotifylib.func_getMsg('all')
        flist = clusnotifylib.func_getMsgContent(msglist)
        for msg in flist:
            if msg_id == msg['filectime']:
                clusnotifylib.func_tagFile(msg['filepath'])
        session.global_v.new_msg_num = len(clusnotifylib.func_getMsg('new'))
        return '0'
    def POST(self):
        return self.action(ajax=True)
    
class clusternotifyfocusall(Page):
    def _action(self):
        msglist = clusnotifylib.func_getMsg('new')
        if len(msglist)>0:
            print >> sys.stderr, msglist
            flist = clusnotifylib.func_getMsgContent(msglist)
            if not flist:
                return '0'
            for msg in flist:
                clusnotifylib.func_tagFile(msg['filepath'])
            session.global_v.new_msg_num = len(clusnotifylib.func_getMsg('new'))
        return '0'
    def POST(self):
        return self.action(ajax=True)
    
class clusternotifydelall(Page):
    def _action(self):
        msglist = clusnotifylib.func_getMsg('old')
        print >> sys.stderr, msglist
        if len(msglist)>0:
            flist = clusnotifylib.func_getMsgContent(msglist)
            if not flist:
                return '0'
            for msg in flist:
                clusnotifylib.func_delTagFile(msg['filepath'])
            session.global_v.new_msg_num = len(clusnotifylib.func_getMsg('new'))
        return '0'
    def POST(self):
        return self.action(ajax=True)