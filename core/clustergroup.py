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

class clustergroup(Page):
    def _logic(self):
        self.content = stow({

        })
        self.setup = stow({
            'template':'clustergroup',
            'breadcrumbs':['clustergroup']
        })
    def GET(self):
        return self.render()

class clustergroupload(Page):
    def _logic(self):
        clustergroups = clusgrouplib.func_group_list_all()
        self.content = stow({
            'nodewithoutgroupname':settings.nodewithoutgroupname,
            'clustergroups':clustergroups
        })
        self.setup = stow({
            'template':'clustergroupload',
            'jstemplate':['datatable_ZH']
        })
    def GET(self):
        return self.render(ajax=True)

class clustergroupcreate(Page):
    def _logic(self):
        self.content = stow({
            'nodewithoutgroup':clusgrouplib.func_get_group(settings.nodewithoutgroupname)
        })
        self.setup = stow({
            'template':'clustergroupcreate'
        })

    def _action(self):
        params = web.input(clustergroupnodes=[])
        clustergroupname = params['clustergroupname']
        clustergroupnodes = params['clustergroupnodes']
        retcode = clusgrouplib.func_group_create(clustergroupname,clustergroupnodes)
        return retcode

    def GET(self):
        return self.render(ajax=True)

    def POST(self):
        return self.action(ajax=True)

class clustergroupedit(Page):
    def _logic(self):
        params = web.input()
        clustergroupname = params['clustergroupname']
        clustergroupnode = clusgrouplib.func_group_list_all(clustergroupname)
        self.content = stow({
            'clustergroupname':clustergroupname,
            'clustergroupnode':clustergroupnode
        })
        self.setup = stow({
            'template':'clustergroupedit'
        })

    def _action(self):
        retcode = 0
        params = web.input(clustergroupnodetodel=[])
        clustergroupoldname = params['clustergroupoldname']
        clustergroupname = params['clustergroupname']
        clustergroupnodetodel = params['clustergroupnodetodel']
        retcode_0 = clusgrouplib.func_group_del_node(clustergroupnodetodel)
        if clustergroupname != clustergroupoldname:
            retcode_1 = clusgrouplib.func_group_rename(clustergroupoldname,clustergroupname)
        else:
            retcode_1 = '0'
        if retcode_0 != '0':
            retcode = retcode_0
        elif retcode_1 != '0':
            retcode = retcode_1
        return retcode

    def GET(self):
        return self.render(ajax=True)

    def POST(self):
        return self.action(ajax=True)
class clustergroupadd(Page):
    def _logic(self):
        self.content = stow({
            'nodewithoutgroup':clusgrouplib.func_get_group(settings.nodewithoutgroupname)
        })
        self.setup = stow({
            'template':'clustergroupadd'
        })

    def _action(self):
        params = web.input(clustergroupnodes=[])
        clustergroupname = params['clustergroupname']
        clustergroupnodes = params['clustergroupnodes']
        retcode = clusgrouplib.func_group_add_node(clustergroupname,clustergroupnodes)
        return retcode

    def GET(self):
        return self.render(ajax=True)

    def POST(self):
        return self.action(ajax=True)

class clustergroupdelete(Page):
    def _action(self):
        params = web.input()
        clustergroupname = params['clustergroupname']
        retcode = clusgrouplib.func_group_delete(clustergroupname)
        return retcode
    def POST(self):
        return self.action(ajax=True)
