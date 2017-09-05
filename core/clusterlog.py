import os
import sys
import re
import subprocess

currpath = os.path.join(os.getcwd(),os.path.dirname(__file__))
if currpath not in sys.path:
    sys.path.append(currpath)
from base import Page,stow,session,web
import settings
from libcommon import clusloglib

class clusterlog(Page):
    def _logic(self):
        self.content = stow({

        })
        self.setup = stow({
            'template':'clusterlog',
            'breadcrumbs':['clusterlog']
        })
    def GET(self):
        return self.render()
    
class clusterlogload(Page):
    def _logic(self):
        clusterlogs = clusloglib.func_log_filter()
        self.content = stow({
            'clusterlogs':clusterlogs
        })
        self.setup = stow({
            'template':'clusterlogload'
            #'jstemplate':['datatable_ZH']
        })
    def GET(self):
        return self.render(ajax=True)