#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import re
import subprocess

currpath = os.path.join(os.getcwd(),os.path.dirname(__file__))
if currpath not in sys.path:
    sys.path.append(currpath)
from base import Page,stow,session,web
import settings
from libcommon import clusgrouplib
from libcommon import clusnodelib
from libcommon import clusservicelib

class clusterguide(Page):
    def _logic(self):
        self.content = stow({

        })
        self.setup = stow({
            'template':'clusterguide'
        })
    def GET(self):
        return self.render()

class clusterguidegroup(Page):
    def _logic(self):
        self.content = stow({

        })
        self.setup = stow({
            'template':'clusterguide_group',
        })
    def GET(self):
        return self.render()

class clusterguidegroupload(Page):
    def _logic(self):
        clustergroups = clusgrouplib.func_group_list_all()
        self.content = stow({
            'nodewithoutgroupname':settings.nodewithoutgroupname,
            'clustergroups':clustergroups
        })
        self.setup = stow({
            'template':'clusterguide_groupload',
            'jstemplate':['datatable_ZH']
        })
    def GET(self):
        return self.render(ajax=True)

class clusterguidenode(Page):
    def _logic(self):
        self.content = stow({
        })
        self.setup = stow({
            'template':'clusterguide_node',
        })

    def GET(self):
        return self.render()

class clusterguidenodeload(Page):
    def _logic(self):
        clusternodes = clusnodelib.func_node_list_all('True')
        self.content = stow({
            'clusternodes':clusternodes
        })
        self.setup = stow({
            'template':'clusterguide_nodeload',
            'jstemplate':['datatable_ZH']
        })
    def GET(self):
        return self.render(ajax=True)
class clusterguidenodecreate(Page):
    def _logic(self):
        clustergroups = clusgrouplib.func_group_list_all()
        self.content = stow({
            'clustergroups':clustergroups
        })
        self.setup = stow({
            'template':'clusternodecreate'
        })
    def _action(self):
        params = web.input()
        clusternodeipaddr = params['clusternodeipaddr']
#        if clusnodelib.func_node_status
        clustergroupname = params['clustergroupname']
        if not clusternodeipaddr:
            return _("fillupclusternodeipaddr")
        if 'clusternodehostname' in params:
            clusternodehostname = params['clusternodehostname']
            retcode = clusnodelib.func_node_create(clusternodeipaddr,clustergroupname,clusternodehostname)
        else:
            retcode = clusnodelib.func_node_create(clusternodeipaddr,clustergroupname)
            return retcode
    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)

class clusterguidenodedeletesingle(Page):
    def _action(self):
        params = web.input()
        clusternodeipaddr = params['clusternodeipaddr']
        retcode = clusnodelib.func_node_delete(clusternodeipaddr)
        return retcode
    def POST(self):
        return self.action(ajax=True)

class clusterguideservice(Page):
    def _logic(self):
        self.content = stow({

        })
        self.setup = stow({
            'template':'clusterguide_service'
        })

    def GET(self):
        return self.render()

class clusterguideserviceload(Page):
    def _logic(self):
        unit = session.runtime.unit
        clusterservices = clusservicelib.func_service_list_all(unit)
        self.content = stow({
            'clusterservices':clusterservices,
            'unit':unit
        })
        self.setup = stow({
            'template':'clusterguide_serviceload',
            'jstemplate':['datatable_ZH']
        })
    def _action(self):
        params = web.input()
        unit = 'unit' in params and params['unit'] or None
        if unit:
            session.runtime.unit = unit
            clusterservices = clusservicelib.func_service_list_all(unit)
            return simplejson.dumps(clusterservices)
    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)

class clusterservicecreateguide_a(Page):
    def _logic(self):
        self.content = stow({
        })
        self.setup = stow({
            'template':'clusterservicecreateguide_a'
        })
    def GET(self):
        return self.render(ajax=True)

class clusterservicecreateguide_b(Page):
    def _logic(self):
        self.content = stow({

        })
        self.setup = stow({
            'template':'clusterservicecreateguide_b'
        })
    def GET(self):
        return self.render(ajax=True)

class clusterservicecreateguide_c(Page):
    def _logic(self):
        clusterservicediskinfo = []
        clusterservicedisk = clusnodelib.func_node_disk_info()
        for disk in clusterservicedisk:
            if disk['status'] == 'unused':
                clusterservicediskinfo.append(disk)
                self.content = stow({
                    'clusterservicediskinfo':clusterservicediskinfo
                })
                self.setup = stow({
                    'template':'clusterservicecreateguide_c'
                })
    def GET(self):
        return self.render(ajax=True)
class clusterservicecreateguide_c_afr(Page):
    def _logic(self):
        clusterservicediskinfo = []
        clusterservicedisk = clusnodelib.func_node_disk_info()
        for disk in clusterservicedisk:
            if disk['status'] == 'unused':
                clusterservicediskinfo.append(disk)
                self.content = stow({
                    'clusterservicediskinfo':clusterservicediskinfo
                })
                self.setup = stow({
                    'template':'clusterservicecreateguide_c_afr'
                })
    def GET(self):
        return self.render(ajax=True)
