#-*- coding: utf-8 -*-
#index.py

import os
import sys
import time
import simplejson
import subprocess
import threading 

from inotify_reports import *
import settings
import syslog
import traceback
from threading import Thread as th

currpath = os.path.join(os.getcwd(),os.path.dirname(__file__))
if currpath not in sys.path:
    sys.path.append(currpath)
from base import Page,stow,session,web,render,_

import settings
from libcommon import clusindex
from libcommon import clusnodelib
from libcommon import clusservicelib
from operator import attrgetter
#--------------------------------
class index(Page):
    def _logic(self):
        self.content = stow({})
        self.setup = stow({
            'template':'index',
            'breadcrumbs':['clusterhome']
        })
    def GET(self):
        return self.render()

class indexgetnode(Page):
    def _action(self):
        params = web.input()
        clustergroupname = params['groupname']
        clustergroupnode = func_group_list_all(clustergroupname)
        return simplejson.dupms(clustergroupnode)
    def POST(self):
        return self.action(ajax=True)
    
class indexgetdisk(Page):
    def _action(self):
        params = web.input()
        clusternodename = params['clusternodename']
        clusternodedisk = clusnodelib.func_node_disk_info(clusternodename)
        clusternodedisklight_status = clusnodelib.func_node_get_disk_lightstatus(clusternodename)
        diskinfo = []
        for disk in clusternodedisk:
            if disk['position'] == "-1":
                if disk['devname'] not in clusternodedisklight_status:
                    disk['light_status'] = 'greenlight'
                else:
                    disk['light_status'] = 'redlight'
                diskinfo.append(disk)
                print >> sys.stderr, disk
            else:
                if disk['devname'] not in clusternodedisklight_status:
                    disk['light_status'] = 'greenlight'
                else:
                    disk['light_status'] = 'redlight'
                diskinfo.append(disk)
        print >> sys.stderr, '---------------------------------------------------'
        print >>sys.stderr, diskinfo
        print >> sys.stderr, '---------------------------------------------------'
        return simplejson.dumps(diskinfo)
    def POST(self):
        return self.action(ajax=True)    

class indexgetraid(Page):
    def _action(self):
        params = web.input()
        clusternodename = params['clusternodename']
        clusternodedisk = clusnodelib.func_node_raid_info(clusternodename)
        raiddict = {}
        diskinfo = []
        for disk in clusternodedisk:
            if disk['raidname'] not in raiddict.keys():
                raiddict[disk['raidname']] = []
                raiddict[disk['raidname']].append(disk)
            else:
                raiddict[disk['raidname']].append(disk)
        return simplejson.dumps(raiddict)
    def POST(self):
        return self.action(ajax=True)    
    
class indexgetreport(Page):
    def __init__(self):
        Page.__init__(self)
        try:
            for t in threading.enumerate():
                print >> sys.stderr, t.name
                #print >> sys.stderr, dir(t)
            print >> sys.stderr, threading.currentThread().name
            th1 = th(target=self.inotify_th, name='inotify_th')
            th1.daemon = True
            th1.start()
            print >> sys.stderr, threading.enumerate()
        except Exception, e:
            print >> sys.stderr, e

    def _action(self):
        try:
            params = web.input()
            nowait = params['nowait']
            if nowait == 'false':
                ret = settings.rqueue.get()#timeout=100)
                session.global_v.rlist.append(ret)
                session.global_v.new_msg_num += 1
            else:
                ret = settings.rqueue.get_nowait()
            print >> sys.stderr, session.global_v
            print >> sys.stderr, '%s-nodata----------------------------------------'% ret
        except Exception,e:
            ret = None
        return session.global_v.new_msg_num

    def inotify_th(self):
        nty = notify(WATCH_DIR)
        nty.run()

    def POST(self):
        return self.action(ajax=True)

class indexgetreportmsg(Page):
    def _action(self):
        return simplejson.dumps(session.global_v.rlist)

    def POST(self):
        return self.action(ajax=True)

class indexgetfocus(Page):
    def _action(self):
        args = web.input()
        msg_id = args['msg_id']
        for msg in session.global_v.rlist:
            print >> sys.stderr, type(msg_id)
            print >> sys.stderr, type(msg['timest'])
            if float(msg_id) == msg['timest']:
                msg['isread'] = "Y"
                if session.global_v.new_msg_num > 0:
                    session.global_v.new_msg_num -= 1
        return '0'
    def POST(self):
        return self.action(ajax=True)

class indexgetservice(Page):
    def _action(self):
        params = web.input()
        #clusterservicename = params['clusterservicename']
        clusterservicelist = clusservicelib.func_service_list_all()
        print >> sys.stderr, clusterservicelist
        servicedatalist = []
        if not 'startword' in clusterservicelist[0]:
            for service in clusterservicelist:
                clusterservicedata = {}
                clusterservicedata['name'] = service['servicename'] 
                diskdata = clusservicelib.func_service_list_disk(service['servicename'])
                clusterservicedata['iconSkin'] = 'diy03' 
                clusterservicedata['childs'] = diskdata['childs']
                servicedatalist.append(clusterservicedata)
            else:
                return simplejson.dumps(servicedatalist)
        else:
            return simplejson.dumps({'name':'noservice', 'iconSkin':'diy03'})
    def POST(self):
        return self.action(ajax=True)
    
class indexgetupsinfo(Page):
    def _action(self):
        from libcommon import clusupslib
        try:
            port    = "/dev/ttyS0"
            timeout = 20
            ser  = clusupslib.open_serial(port, timeout)
            time.sleep(1)
            res1 = clusupslib.read_serial_data(ser,'Q1')
            if not res1:
                return simplejson.dumps({})
            upsinfo1 = clusupslib.format_Q1(res1)
            res6 = clusupslib.read_serial_data(ser,'Q6')
            if not res6:
                return simplejson.dumps({})
            upsinfo6 = clusupslib.format_Q6(res6)
            clusterupsdata = {}
            if upsinfo1['UPS Status'][6] == '':
                clusterupsdata['charge'] = True
            else:
                clusterupsdata['charge'] = False
            clusterupsdata['time_remaining'] = float(upsinfo6['Battery Capacity Percentage(%)']) * 100
            clusterupsdata['estimated_runtime'] = upsinfo6['Estimated Runtime(s)']
            clusupslib.close_serial(ser)
        except:
            clusterupsdata = {}
        return simplejson.dumps(clusterupsdata)
    def POST(self):
        return self.action(ajax=True)
        

class login(Page):
    def GET(self):
        params = web.input()
        lang = session.user.lang
        self._jsrender()
        content = stow({
            'title':settings.procname,
            'lang': lang,
            'javascript_files':self.setup['javascript_files']
        })
        if 'redirect_url' in params:
           content['redirect_url'] = params['redirect_url']
        return render.login(content)

    def POST(self):
        params = web.input()
        name = None
        passwd = None
        enpasswd = None
		
        
        if os.path.exists("/usr/local/digioceanfs_gui/password"):		
           f=open("/usr/local/digioceanfs_gui/password")
           old_password=f.read().replace("\n","")		
           f.close()
        else:
           os.system("sudo touch /usr/local/digioceanfs_gui/password")
           os.system("sudo chmod 777 /usr/local/digioceanfs_gui/password")
           old_password=""
        
        if old_password=="":
            old_password='e10adc3949ba59abbe56e057f20f883e'

        user = {
            'name':'admin',
            #'pass':'3be314d2f6fec7fa64af9ac5d2e1e279', # perabytes
            'pass':old_password,  # 123456
            'skin':'redmond',
            'lang':'zh_CN',
            'time': time.time()
        }
        if 'name' in params:
            name = params['name'].strip()
        if 'passwd' in params:
            passwd = params['passwd'].strip()
        if not name or not passwd:
            raise web.seeother('/login')
        try:
            from hashlib import md5
            enpasswd = md5(passwd)#.hexdigest()
        except:
            import md5
            enpasswd = md5.new(passwd)
        #retcode = clusindex.func_login(name, enpasswd)
        #if retcode == '0':
        if name != user['name']:
            retcode = _('15001')
            return simplejson.dumps(retcode)
        elif enpasswd.hexdigest() != user['pass']:
            retcode = _('15002')
            return simplejson.dumps(retcode)
        elif name == user['name'] and enpasswd.hexdigest() == user['pass']:
            session.user.id = 1
            session.user.name = name
            session.runtime.unit = 'GB'
            retcode = 0
            #if 'redirect_url' in params:
            #    raise web.seeother(params['redirect_url'])
            #else:
            #    raise web.seeother('/clusterhome')
        #else:
            #raise web.seeother('/login')
            return simplejson.dumps(retcode)
            #if 'redirect_url' in params:
            #    return simplejson.dumps(params['redirect_url'])
            #else:
            #    return simplejson.dumps('/clusterhome')
        #else:
            #raise web.seeother('/login')
            #return simplejson.dumps(retcode)

class logout(object):
    def GET(self):
        try:
            session.kill()
            retcode = clusindex.func_logout()
        except:
            pass
        raise web.seeother('/login')

class manager_check(Page):
    def _action(self):
        params = web.input()
        ipaddr = params["ipaddr"]
        ret = clusindex.func_manager_check(ipaddr)
        return ret
    def POST(self):
        return self.action(ajax=True)

class manager_set(Page):
    def _action(self):
        params = web.input()
        ipaddr = params["ipaddr"]
        ret = clusindex.func_manager_set(ipaddr)
        return ret
    def POST(self):
        return self.action(ajax=True)

class manager_get(Page):
    def _action(self):
        ret = clusindex.func_manager_get()
        return ret
    def POST(self):
        return self.action(ajax=True)

class changelanguage(Page):
    def _action(self):
        params = web.input()
        language = params['pagelang']
        session.user.lang = language
        return 0
    def POST(self):
        return self.action(ajax=True)

#�޸�����		
class password_modify(Page):
    def _logic(self):
        self.setup = stow({
            'template':'password_modify'
        })
    def _action(self):
        params = web.input()
        from hashlib import md5
		
        if os.path.exists("/usr/local/digioceanfs_gui/password"):		
           f=open("/usr/local/digioceanfs_gui/password")
           old_password=f.read().replace("\n","")		
           f.close()
        else:
           os.system("sudo touch /usr/local/digioceanfs_gui/password")
           os.system("sudo chmod 777 /usr/local/digioceanfs_gui/password")
           old_password=""
        
        if old_password=="":
            old_password=md5("123456").hexdigest()
        #print >> sys.stderr,old_password			
			
        if old_password==md5(params['old_password']).hexdigest():
            f=open("/usr/local/digioceanfs_gui/password","r+")
            f.write(md5(params['new_password']).hexdigest())
            f.close()			
            return 0
    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)

#������		
class password_check(Page):
    def _action(self):
        params = web.input()
        from hashlib import md5
			
        if os.path.exists("/usr/local/digioceanfs_gui/password"):		
           f=open("/usr/local/digioceanfs_gui/password")
           old_password=f.read().replace("\n","")		
           f.close()
        else:
           os.system("sudo touch /usr/local/digioceanfs_gui/password")
           os.system("sudo chmod 777 /usr/local/digioceanfs_gui/password")
           old_password=""
        
        if old_password=="":
            return 0
    def POST(self):
        return self.action(ajax=True)
    
class initleftnav(Page):
    def _action(self):
        zNodes = [{'name':'_("clustergroup")',isParent:"true", 'fullName':'_("clustergroup")'},{'name':'_("clusterservice")',isParent:"true", 'fullName':'_("clusterservice")'}];
        return simplejson.dumps(zNodes)
    
    def POST(self):
        return self.action(ajax=True)
