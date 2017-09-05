#*- coding: utf-8 -*-
#base.py

import os
import sys
import time
import gettext
import traceback
import re

currpath = os.path.join(os.getcwd(),os.path.dirname(__file__))
if currpath not in sys.path:
    sys.path.append(currpath)
import settings
from libcommon import web
from libcommon import utils
from libcommon.logger import logger
from urls import urls

#i18n
alltranslations = web.storage()
localedir = os.path.join(currpath,'i18n')
#gettext.install('messages', localedir, unicode=True)
#gettext.translation('messages', localedir, languages=['zh_CN']).install(True)
def get_translations(lang='zh_CN'):
    if lang in alltranslations:
        translation = alltranslations[lang]
    elif lang is None:
        translation = gettext.NullTranslations()
    else:
        try:
            translation = gettext.translation('messages',localedir,languages=[lang])
        except Exception,e:
            translation = gettext.NullTranslations()
    return translation
def load_translations(lang):
    lang = str(lang)
    translation = alltranslations.get(lang)
    if translation is None:
        translation = get_translations(lang)
        alltranslations[lang] = translation

        for lk in alltranslations.keys():
            if lk != lang:
                del alltranslations[lk]
    return translation
def custom_gettext(string):
    translation = load_translations(session.user.get('lang'))
    if translation is None:
        return unicode(string)
    return translation.ugettext(string)

#config template
web.template.Template.globals['ELT'] = '$'
web.template.Template.globals['DOUBLEELT'] = '$$'
web.template.Template.globals['range'] = range
web.template.Template.globals['os'] = os
web.template.Template.globals['re'] = re
web.template.Template.globals['str'] = str
web.template.Template.globals['int'] = int
web.template.Template.globals['time'] = time
web.template.Template.globals['_'] = custom_gettext

#config session
web.config.session_parameters['cookie_name'] = 'peratools'
web.config.session_parameters['cookie_domain'] = None
web.config.session_parameters['timeout'] = 1800, #30 * 60, # 30 minutes in seconds
web.config.session_parameters['ignore_expiry'] = False
web.config.session_parameters['ignore_change_ip'] = False
web.config.session_parameters['secret_key'] = 'fLjUfxqXtfNoIldA0A0J'
web.config.session_parameters['expired_message'] = 'Session expired'

#config debug
web.config.debug = False

#globals
stow = web.storage
render = web.template.render(settings.TEMPLATEDIR,cache=False)
jsrender = web.template.render(settings.JSTEMPLATEDIR,cache=False)
layout = 'default'
app_info = {
	'mapping':urls,
	'fvars':globals(),
	#'reloader':web.reloader,
}
app = web.application(**app_info)
app_db = settings.conn
#session
session_info = {
    'app':app,
    'store':web.session.DiskStore(settings.sessionpath),
    'initializer':{
        'user':stow({
            'id':None,
            'name':None,
            'skin':'redmond',
            'lang':'zh_CN'
        }),
        'runtime':stow({
            'node':'',
            'unit':'',
            'service':'',
            'managercheck':False
        }),
        'global_v':stow({
            'rlist':list(),
            'new_msg_num':0
        })
    }}
if web.config.get('_session') is None:
    session = web.session.Session(**session_info)
    web.config._session = session
else:
    session = web.config._session
application = app.wsgifunc()

#custom 404 and 505
def not_found():
    content = stow({
        'title':'DigiOceanFS Error Page'
    })
    return web.notfound(render.notfound(content))

def internal_error():
    content = stow({
        'title':'DigiOceanFS Error Page'
    })
    return web.internalerror(render.internalerror(content))

#app.internalerror = internal_error
#app.notfound = not_found

_ = custom_gettext
from libcommon.clusindex import func_manager_check 
defnavigators = []
defmenus = {}
def _initpageparams():
    global defnavigators
    global defmenus
    defnavigators = [
        #['clusterhome',_("clusterhome"),'/clusterhome'],
        #['clustergroup',_("clustergroup"),'/clustergroup'],
        ['clusternode',_("clusternode"),'/clusternode'],
        ['clusterservice',_("clusterservice"),'/clusterservice'],
        ['clusternotify',_("clusternotify"),'/clusternotify']
    ]

    defmenus = {
        #'clusterhome':[_("clusterhome"),'/clusterhome'],
        #global
        #'clustergroup':[_("clustergroup"),'/clustergroup'],
        'clusternode':[_("clusternode"),'/clusternode'],
        'clusterservice':[_("clusterservice"),'/clusterservice'],
        'clusternotify':[_("clusternotify"),'/clusternotify'],
        #clusternode
        'clusternodenetwork':[_("clusternodenetwork"),'/clusternodenetwork'],
        'clusternodenetbond':[_("clusternodenetbond"),'clusternodenetbond'],
        'clusternodedisk':[_("clusternodedisk"),'/clusternodedisk'],
        'clusternoderaid':[_("clusternoderaid"),'/clusternoderaid'],
        'clusternodeview':[session.runtime.node,'/clusternodeview?node=%s' % session.runtime.node],
        'clusternodeinfo':[_("clusternodeinfo"),'/clusternodeview?node=%s' % session.runtime.node],
#       clusterserviceview
        'clusterserviceview':[session.runtime.service,'/clusterserviceview?service=%s' % session.runtime.service]
    }
def func_gen_menu(menulist):
    """
    wrapper to render menu
    """
    _initpageparams()
    menuitems = []
    for menu in menulist:
        if menu.endswith('!'):
            menuitems.append([menu] + defmenus[menu[:-1]])
        elif menu == 'fg':
            menuitems.append([menu])
        else:
            menuitems.append([menu] + defmenus[menu])
    return menuitems

def fun_gen_shotcuts(breadcrumbs):
    retbreadcrumbs = {}
    _initpageparams()
    for breadcrumb in breadcrumbs:
        retbreadcrumbs[breadcrumb] = defmenus[breadcrumb]
    return retbreadcrumbs

class Page:
    def __init__(self):
        self.request_method = web.ctx.env.get('REQUEST_METHOD')
        self.path = web.ctx.env.get('PATH_INFO')
        self.setup = stow({})
        self.content = stow({})
        self.skin = session.user.skin
        self.params = web.input(file=[])

    def _valid(self):
        if not session.user.id:
            if self.path and self.path not in ['/login']:
                pass
            raise web.seeother('/login?redirect_url=%s' % self.path)
        print >> sys.stderr, session
        '''if not session.runtime.managercheck:
            manager_check = func_manager_check(web.ctx.environ['SERVER_NAME'])
            if manager_check != '0':
                raise web.seeother('/login?redirect_url=%s' % self.path)
                session.runtime.managercheck = False 
            else:
                session.runtime.managercheck = True'''

    def _render(self,ajax=False,layout='default'):
        self.content.skin = self.skin
        self.content.session = session
        self.page_content = render.__getattr__(self.setup['template'])(self.content)
        self._jsrender()
        if ajax:
            return self.page_content
        page_setup = {
            'title':settings.procname,
            'footer':settings.footer,
            'breadcrumbs':[],
            'menu_title':'',
            'menus':[],
            'currmenu':'',
            'javascript':[],
            'jstemplate':[],
            'css':[],
            'skin':self.skin
        }
        for key,value in page_setup.iteritems():
            self.setup[key] = key in self.setup and self.setup[key] or value
        self.shortcuts = fun_gen_shotcuts(self.setup['breadcrumbs'])
        self.menu_items = func_gen_menu(self.setup['menus'])
        self.navigators = defnavigators
        content = stow({
            'page_setup':self.setup,
            'menu_items':self.menu_items,
            'shortcuts':self.shortcuts,
            'navigators':self.navigators,
            'page_content':self.page_content,
            'session':session,
        })
        #logger.debug(time.strftime("%Y-%m-%d %X",time.time()) + ':' + self.path)
        return render.__getattr__(layout)(content)

    def _jsrender(self):
        self.setup['javascript_files'] = []
        if not 'jstemplate' in self.setup: 
            self.setup['jstemplate']= []
            self.setup['jstemplate'].append('utils.js')
            self.setup['jstemplate'].append('datatable_ZH.js')
        else:
            self.setup['jstemplate'].append('utils.js')
            self.setup['jstemplate'].append('datatable_ZH.js')
        if 'jstemplate' in self.setup:
            import os
            for file in self.setup['jstemplate']:
                jsfile = ''
                jsfilename = ''
                if os.path.splitext(file)[1] == '.js':
                    if os.path.splitext(file)[0] != 'datatable_ZH':
                        jsfile = file
                    else:
                        jsfile = os.path.splitext(file)[0]
                    jsfilename = os.path.splitext(file)[0]
                else:
                    jsfile = file + '.js'
                    jsfilename = file
                try:
                    js_content = jsrender.__getattr__(jsfilename)(self.content)
                    jsfilepath = os.path.join(settings.JSTEMPPATH,jsfile)
                    #utils.upload_file(settings.JSTEMPPATH,jsfilepath,js_content)
                    f = open(os.path.join(settings.JSTEMPPATH,jsfilepath),'w')
                    f.write(str(js_content))
                    f.close()
                    self.setup['javascript_files'].append(jsfile)
                except Exception,e:
                    logger.debug(e)
                    self.setup['javascript_files'].append(jsfile)

    def render(self,ajax=False,debug=settings.DEBUG,layout=layout,notemplate=False):
        if debug:
            self._valid()
            if notemplate:
                return self._logic()
            self._logic()
            return self._render(ajax,layout)
        else:
            try:
                self._valid()
                if notemplate:
                    return self._logic()
                self._logic()
                return self._render(ajax,layout)
            except Exception,e:
                logger.debug(e)
                pass
    def _logic(self):
        self.content = stow({})
        self.setup = stow({

        })

    def _action(self):
        self.redirect_url = '/'
        raise web.seeother(self.redirect_url)

    def action(self,ajax=False,debug=settings.DEBUG):
        if debug:
            if ajax:
                return self._action()
            self._action()
        else:
            try:
                if ajax:
                    return self._action()
                self._action()
            except Exception,e:
                logger.debug(e)
                pass
