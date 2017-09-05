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
from base import Page,stow,session,web
import settings
from libcommon import clusnodelib
from libcommon import clusservicelib
from libcommon import findir
from findir import myFile

class Service(Page):
    def _checkservice(self):
        if not session.runtime.service:
            raise web.seeother('/clusterservice')

class clusterservice(Page):
    def _logic(self):
        self.content = stow({

        })
        self.setup = stow({
            'template':'clusterservice',
            'breadcrumbs':['clusterservice']
        })

    def GET(self):
        return self.render()

class clusterserviceview(Page):
    def _logic(self):
        params = web.input()
        service = 'service' in params and params['service'] or None
        if service:
            session.runtime.service = service
        self.content = stow({
            'servicename': service
        })
        self.setup = stow({
            'template':'clusterserviceview',
            'breadcrumbs':['clusterservice','clusterserviceview']
        })

    def GET(self):
        return self.render()

class clusterserviceviewtabspage(Page):
    def _logic(self):
        params = web.input()
        service = 'service' in params and params['service'] or None
        if service:
            session.runtime.service = service
        self.content = stow({
            'servicename': service
        })
        self.setup = stow({
            'template':'clusterserviceviewload'
        })
    def GET(self):
        return self.render(ajax=True)

class clusterserviceload(Page):
    def _logic(self):
        #unit = session.runtime.unit
        params = web.input()
        unit = 'unit' in params and params['unit'] or None		
        clusterservices = clusservicelib.func_service_list_all(unit)
        self.content = stow({
            'clusterservices':clusterservices,
            'unit':unit
        })
        self.setup = stow({
            'template':'clusterserviceload',
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

class clusterserviceviewloadrefresh(Page):
    def _action(self):
        params = web.input()
        service = session.runtime.service
        #print >>sys.stderr, params
        #print >>sys.stderr, params['expandarray'].decode('UTF-8')
        print >> sys.stderr, params
        print >> sys.stderr, params['expandarray']
        my_dict= clusservicelib.func_service_afr_info_search(service, '', params['expandarray'])
        return simplejson.dumps([my_dict], encoding="UTF-8")
    def POST(self):
        return self.action(ajax=True)

class clusterserviceviewload(Page):
    def _logic(self):
        params = web.input()
        service= session.runtime.service
        unit = session.runtime.unit
        mydict = {}
        #clusterservices = clusservicelib.func_service_list_disk(service)
        mydict = clusservicelib.func_service_afr_info_search(service,)
        print >> sys.stderr,mydict 
        self.content = stow({
        #    'clusterservices':clusterservices,
            'mydict':mydict
        })
        self.setup = stow({
            'template':'clusterserviceviewload',
        })

    def _action(self):
        params = web.input()
        unit = 'unit' in params and params['unit'] or None
        if unit:
            session.runtime.unit = unit
        service = session.runtime.service
        if 'PATH' in params:
            dirname = params['PATH']
            #print >>sys.stderr, params
            #print >>sys.stderr, dirname.decode('UTF-8')
            my_dict= clusservicelib.func_service_afr_info_search(service,dirname,'')
        else:
            my_dict= clusservicelib.func_service_afr_info_search(service)
        return simplejson.dumps({})

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
        self.setup = stow({
            'template':'clusterservicecreateguide_c'
        })
    def GET(self):
        return self.render(ajax=True)
    
class clusterservicecreatedisk(Page):
    def _action(self):
        clusterservicediskinfo = []
        clusterservicedisk = clusnodelib.func_node_disk_info()
        for disk in clusterservicedisk:
            if disk['status'] == 'unused':
                clusterservicediskinfo.append(disk)
        print >>sys.stderr, clusterservicediskinfo
        return simplejson.dumps(clusterservicediskinfo)
    def POST(self):
        return self.action(ajax=True)

class clusterservicecreateguide_c_afr_strip(Page):
    def _logic(self):
        self.setup = stow({
            'template':'clusterservicecreateguide_c_afr_strip'
        })
    def GET(self):
        return self.render(ajax=True)

class clusterservicecreateguide_c_strip_afr(Page):
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
            'template':'clusterservicecreateguide_c_strip_afr'
        })
    def GET(self):
        return self.render(ajax=True)

class clusterservice_afr_syn(Page):
    def _action(self):
        params = web.input()
        service = params['servicename']
        retcode = clusservicelib.func_service_afr_syn(service)
        return retcode
    def POST(self):
        return self.action(ajax=True)

class clusterservicecreate(Page):
    def _action(self):
        params = web.input(afrdisknewdev=[],stripdisknewdev=[],defaultdisknewdev=[])
        if 'disks_num' in params:
            disks_num = params['disks_num']
        if 'sub_volume_num' in params:
            sub_volume_num = params['sub_volume_num']
        clusterservicetype = params['clusterservicetype']
        clusterservicelocalpor = params['clusterservicelocalpor']

        if clusterservicetype == 'clusterservicetype_afr':
            clusterservicenewdev = params['afrdisknewdev'][0].split(',')
        elif clusterservicetype == 'clusterservicetype_strip':
            clusterservicenewdev = params['stripdisknewdev'][0].split(',')
        else:
            clusterservicenewdev = params['defaultdisknewdev'][0].split(',')
        
        if clusterservicelocalpor == 'clusterservicelocalpor_no':
            clusterservicelocalpor = '0'
            print >> sys.stderr, 'clusterservicelocalpor=' +clusterservicelocalpor
        else:
            clusterservicelocalpor = '1'
        
        if clusterservicetype == 'clusterservicetype_default':
            clusterserviceraidlv = '2'
            option = '' #'-a ' + disks_num  + ' -s ' + sub_volume_num
#        elif clusterservicetype == 'clusterservicetype_strip' and disks_num == '1':
#            clusterserviceraidlv = '0'
#            option = '-a ' + sub_volume_num  + ' -m ' + '-s ' + disks_num
        elif clusterservicetype == 'clusterservicetype_afr' and disks_num == '1':
            clusterserviceraidlv = '1'
            option = '-a ' + sub_volume_num
#        elif clusterservicetype == 'clusterservicetype_strip' and disks_num != '1':
#            clusterserviceraidlv = '01'
#            option = '-a ' + sub_volume_num  + ' -m ' + '-s ' + disks_num
#        elif clusterservicetype == 'clusterservicetype_afr' and disks_num != '1':
#            clusterserviceraidlv = '01'
#            option = '-a ' + sub_volume_num + ' -m ' + '-s ' + disks_num
        clusterservicedata = ' '.join(clusterservicenewdev)
        clusterservicename = params['clusterservicename']
        retcode = clusservicelib.func_service_create(clusterservicename, clusterserviceraidlv, clusterservicelocalpor, clusterservicedata, option)
        return retcode
    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)

class clusterservicextend(Page):
    def _logic(self):
        #clusterservice = clusservicelib.func_service_list_all()
        #clusterservicename = []
        #for name in clusterservice:
        #    clusterservicename.append(name['servicename'])
        #clusternodeip = []
        #clusterdiskunused = []
        #for node in clusnodelib.func_node_list_all('False'):
        #    clusternodeip.append(node['nodename'])
        #self.content = stow({
        #    'clusterservice':clusterservicename,
        #    'clusternodeip':clusternodeip,
        #})
        self.setup = stow({
            'template':'clusterservicextend'
        })

    def _action(self):
        params = web.input(clusterexservicedev=[])
        clusterserviceraidlv = '2'
        clusterservicename = params['clusterservicename']
        if 'clusterservicetype_none' in params and params['clusterservicetype_none'] == 'on':
            clusterserviceraidlv = '2'
        elif 'clusterservicetype_afr' in params and params['clusterservicetype_afr'] == 'on':
            clusterserviceraidlv = '1'
        elif 'clusterservicetype_strip' in params and params['clusterservicetype_strip'] == 'on':
            clusterserviceraidlv = '0'
        clusterservicedata = ' '.join(params['clusterexservicedev'])
        retcode = clusservicelib.func_service_extend(clusterservicename, clusterservicedata)
        return retcode

    def GET(self):
        return self.render(ajax=True)

    def POST(self):
        return self.action(ajax=True)

#客户端节点列表	
class clusterclientnodeload(Page):
    def _logic(self):
        params = web.input()
        clusterclientnodes = clusservicelib.func_client_node_list_all(params['service_name'])
        #print >> sys.stderr, clusterclientnodes
        self.content = stow({
            'clusterclientnodes':clusterclientnodes
        })
        self.setup = stow({
            'template':'clusterclientnodeload',
            #'jstemplate':['datatable_ZH']
        })
    def _action(self):
        #删除时判断是否有启动中的客户端节点
        service_arr=[]
        params = web.input()
        clusterservice=clusservicelib.func_service_list_all()
        for service in clusterservice:            	
            clusterclientnodes = clusservicelib.func_client_node_list_all(service['servicename'])
            for node in clusterclientnodes:
                if params['node_name']==node['node_name']:
                    if node['status']=='1':
                        service_arr.append(service['servicename'])
        if service_arr:
            retcode=','.join(service_arr)
        else:
            retcode='0'
        return retcode

    def GET(self):
        return self.render(ajax=True)

    def POST(self):
        return self.action(ajax=True)		

#客户端节点添加
class clusterclientnodecreate(Page):
    def _logic(self):      
        self.setup = stow({
            'template':'clusterclientnodecreate'
        })

    def _action(self):
        params = web.input()			
        retcode = clusservicelib.func_client_node_create(params['service_name'],params['node_name'])
        return retcode

    def GET(self):
        return self.render(ajax=True)

    def POST(self):
        return self.action(ajax=True)		

#客户端节点删除
class clusterclientnodedelete(Page):
    def _action(self):
        params = web.input()			
        retcode = clusservicelib.func_client_node_delete(params['service_name'],params['node_name'])
        return retcode

    def GET(self):
        return self.render(ajax=True)

    def POST(self):
        return self.action(ajax=True)
		
#客户端节点cifs
'''
class clusterclientnodecifs(Page):
    def _action(self):
        params = web.input()			
        retcode = clusservicelib.func_client_node_cifs(params['op'],params['service_name'],params['node_name'])
        return retcode

    def GET(self):
        return self.render(ajax=True)

    def POST(self):
        return self.action(ajax=True)

#客户端节点nfs
class clusterclientnodenfs(Page):
    def _action(self):
        params = web.input()			
        retcode = clusservicelib.func_client_node_nfs(params['op'],params['service_name'],params['node_name'])
        return retcode

    def GET(self):
        return self.render(ajax=True)

    def POST(self):
        return self.action(ajax=True)
'''
		
#客户端节点状态
class clusterclientnodestatus(Page):
    def _action(self):
        params = web.input()			
        retcode = clusservicelib.func_client_node_status(params['op'],params['service_name'],params['node_name'])
        return retcode

    def GET(self):
        return self.render(ajax=True)

    def POST(self):
        return self.action(ajax=True)

		
#服务磁盘块
class clusterserviceraidlvdetail(Page):
    def _logic(self):       
        params = web.input()
        bricks = clusservicelib.func_raidlv_detail(params['service_name'])
        #print >> sys.stderr,  bricks
        self.content = stow({
            'bricks': bricks,
            'service_name':params['service_name'],
            'afr':params['afr'],
			'key':0
        })
        self.setup = stow({
            'template':'clusterserviceraidlvdetail',
            #'jstemplate':['datatable_ZH']
        })
    def _action(self):
        params = web.input()
    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)
		
#服务磁盘替换
class clusterservicediskreplace(Page):
    def _logic(self):       
        params = web.input()
        unit = session.runtime.unit
        disk_arr = clusnodelib.func_node_disk_info('',unit)
        unuse_disk=[]
        for disk in disk_arr:
            if disk['status']=='unused':
                unuse_disk.append(disk['nodename']+':'+disk['devname'])
        unuse_disk_str=','.join(unuse_disk)			
        self.content = stow({
            'service_name':params['service_name'],
            'disk':params['disk'],
            'unuse_disk_str':unuse_disk_str,
        })
        self.setup = stow({
            'template':'clusterservicediskreplace',
        })
    def _action(self):
        params = web.input()
    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)
		
class clusterservicedisk(Page):
    def _logic(self):
        #node = session.runtime.node
        node = ''
        unit = session.runtime.unit
        clusternodediskinfo = clusnodelib.func_node_disk_info(node,unit)
        clusternoderaidinfo = clusnodelib.func_node_raid_info(node,unit)
        self.content = stow({
            'clusternodediskinfo':clusternodediskinfo,
            'clusternoderaidinfo':clusternoderaidinfo,
			'is_service':'1'
        })
        self.setup = stow({
            'template':'clusternodedisk',
            #'breadcrumbs':['clusternode','clusternodeview','clusternodedisk'],
            #'menus':gmenus,
            #'currmenu':'clusternodedisk',
        })
    def GET(self):
        return self.render(ajax=True)
		
class clusterserviceraidload(Page):
    def _logic(self):
        #node = session.runtime.node
        node = ''
        unit = session.runtime.unit
        clusternodediskinfo = clusnodelib.func_node_disk_info(node,unit)
        clusternoderaidinfo = clusnodelib.func_node_raid_info(node,unit)
        self.content = stow({
            'clusternodediskinfo':clusternodediskinfo,
            'clusternoderaidinfo':clusternoderaidinfo,
            'unit':unit,
			'is_unused':'0'
        })
        self.setup = stow({
            'jstemplate':['datatable_ZH'],
            'template':'clusternoderaidload',
        })
    def _action(self):
        params = web.input()
        node = session.runtime.node
        unit = 'unit' in params and params['unit'] or None
        if unit:
            session.runtime.unit = unit
        clusternodediskinfo = clusnodelib.func_node_disk_info(node,unit)
        return simplejson.dumps(clusternodediskinfo)

    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)

class clusterserviceraidload_select(Page):
    def _logic(self):
        node = ''
        unit = session.runtime.unit
        clusternodediskinfo = clusnodelib.func_node_disk_info(node,unit)
        clusternoderaidinfo = clusnodelib.func_node_raid_info(node,unit)
        self.content = stow({
            'clusternodediskinfo':clusternodediskinfo,
            'clusternoderaidinfo':clusternoderaidinfo,
            'unit':unit,
			'is_unused':'1'
        })
        self.setup = stow({
            'jstemplate':['datatable_ZH'],
            'template':'clusternoderaidload',
        })
    def _action(self):
        params = web.input()
        node = session.runtime.node
        unit = 'unit' in params and params['unit'] or None
        if unit:
            session.runtime.unit = unit
        clusternodediskinfo = clusnodelib.func_node_disk_info(node,unit)
        return simplejson.dumps(clusternodediskinfo)

    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)			
		
class clusterservicextendservice(Page):
    def _action(self):
        clusterservice = clusservicelib.func_service_list_all()
        clusterservicename = []
        for name in clusterservice:
            clusterservicename.append(name['servicename']+'::'+name['afr'])
        return simplejson.dumps(clusterservicename)
    def POST(self):
        return self.action(ajax=True)

class clusterservicextendnode(Page):
    def _action(self):
        clusternode = clusnodelib.func_node_list_all('False')
        clusternodeip = []
        for node in clusternode:
            clusternodeip.append(node['nodename'])
        return simplejson.dumps(clusternodeip)
    def POST(self):
        return self.action(ajax=True)

class clusterservicecifs_status(Page):
    def _action(self):
        params = web.input()
        clusterservicename = params['clusterservicename']
        clusterserviceoption = params['clusterservicecifsoption']
        retcode = clusservicelib.func_service_export(clusterserviceoption, 'cifs', clusterservicename)
        return retcode
    def POST(self):
        return self.action(ajax=True)
    
class clusterservicecifsrestart(Page):
    def _action(self):
        params = web.input()
        clusterservicename = params['clusterservicename']
        retcode = clusservicelib.func_service_cifs_restart(clusterservicename)
        return retcode
    def POST(self):
        return self.action(ajax=True)

class clusterservicenfs_status(Page):
    def _action(self):
        params = web.input()
        clusterservicename = params['clusterservicename']
        clusterserviceoption = params['clusterservicenfsoption']
        retcode = clusservicelib.func_service_export(clusterserviceoption, 'nfs', clusterservicename)
        return retcode
    def POST(self):
        return self.action(ajax=True)

class clusterservicexportstatus(Page):
    def _action(self):
        params = web.input()
        clusterservicename = params['clusterservicename']
        type = params['type']
        clusterserviceoption = 'status'
        retcode = clusservicelib.func_service_export(clusterserviceoption, type, clusterservicename)
        return simplejson.dumps(retcode)
    def POST(self):
        return self.action(ajax=True)

class clusterservicecreatedialog(Page):
    def _logic(self):
        clusterdiskunused = []
        clusternodediskinfo = []
        clusternodedisksize = []
        clusternewservicedev = {}
        params = web.input()
        disk = clusnodelib.func_node_disk_info(params['clusternodeipaddr'])
        for d in disk:
            if d['status'] == 'unused':
                dev = params['clusternodeipaddr'] + ':' + d['devname']
                diskinfo = 'model:' + d['vandor'] + '<br />' + 'serial_number:' +d['sn_number'] + '<br />' + 'size:' + d['size']
                clusternodediskinfo.append(diskinfo)
                clusterdiskunused.append(dev)
                clusternewservicedev['clusterdiskunused'] = clusterdiskunused
                clusternewservicedev['clusternodediskinfo'] = clusternodediskinfo
        return simplejson.dumps(clusternewservicedev)
    def GET(self):
        return self.render(ajax=True, notemplate=True)

class clusterservicecifsmanage(Page):
    def _logic(self):
        params = web.input()
        print >> sys.stderr, params
        service_name = params['service_name']
        self.setup = stow({
            'template':'clusterservicecifsmanage'
        })
        self.content = stow({
            'service_name':service_name
        })
    def GET(self):
        return self.render(ajax=True)
    
class clusterservicecifsusermanage(Page):
    def _logic(self):
        #params = web.input()
        #service_name = params['service_name']
        self.setup = stow({
            'template':'clusterservicecifsusermanage'
        })
        '''self.content = stow({
            'service_name':service_name
        })'''
    def GET(self):
        return self.render(ajax=True)
class clusterservicecifslistuser(Page):
    def _action(self):
        params = web.input()
        service_name = params['service_name']
        clusterservicename = params['service_name']
        userlist = clusservicelib.func_service_cifs_list_user(clusterservicename)
        return simplejson.dumps(userlist)
    def POST(self):
        return self.action(ajax=True)
    
class clusterservicecifsadduser(Page):
    def _action(self):
        params = web.input()
        service_name = params['service_name']
        clusterservicename = params['service_name']
        username = params['username']
        password = params['password']
        retcode = clusservicelib.func_service_cifs_add_user(clusterservicename, username, password)
        return retcode
    def POST(self):
        return self.action(ajax=True)
    
class clusterservicecifsdeluser(Page):
    def _action(self):
        params = web.input()
        service_name = params['service_name']
        clusterservicename = params['service_name']
        username = params['username']
        retcode = clusservicelib.func_service_cifs_del_user(clusterservicename, username)
        return retcode
    def POST(self):
        return self.action(ajax=True)

class clusterservicecifschecklinks(Page):
    def _logic(self):
        params = web.input()
        service_name = params['service_name']
        self.setup = stow({
            'template':'clusterservicecifschecklinks'
        })
        self.content = stow({
            'service_name':service_name
        })
    def GET(self):
        return self.render(ajax=True)
    
class clusterservicecifschecklinksdata(Page):
    def _action(self):
        params = web.input()
        servicename = params['service_name']
        cifschecklinksdata = clusservicelib.func_service_list_cifs_links(servicename)
        return simplejson.dumps(cifschecklinksdata)
    def POST(self):
        return self.action(ajax=True)
    
class clusterservicecifsdellink(Page):
    def _action(self):
        params = web.input()
        servicename = params['service_name']
        nodename = params['node_name']
        pid = params['pid']
        ret = clusservicelib.func_service_del_cifs_links(servicename, nodename, pid)
        return ret
    def POST(self):
        return self.action(ajax=True)
    
class clusterservicenfsmanage(Page):
    def _logic(self):
        params = web.input()
        print >> sys.stderr, params
        service_name = params['service_name']
        self.setup = stow({
            'template':'clusterservicenfsmanage'
        })
        self.content = stow({
            'service_name':service_name
        })
    def GET(self):
        return self.render(ajax=True)
    
class clusterservicenfsusermanage(Page):
    def _logic(self):
        #params = web.input()
        #service_name = params['service_name']
        self.setup = stow({
            'template':'clusterservicenfsusermanage'
        })
        '''self.content = stow({
            'service_name':service_name
        })'''
    def GET(self):
        return self.render(ajax=True)
class clusterservicenfslistuser(Page):
    def _action(self):
        params = web.input()
        service_name = params['service_name']
        clusterservicename = params['service_name']
        userlist = clusservicelib.func_service_nfs_list_user(clusterservicename)
        return simplejson.dumps(userlist)
    def POST(self):
        return self.action(ajax=True)
    
class clusterservicenfschecklinks(Page):
    def _logic(self):
        params = web.input()
        service_name = params['service_name']
        self.setup = stow({
            'template':'clusterservicenfschecklinks'
        })
        self.content = stow({
            'service_name':service_name
        })
    def GET(self):
        return self.render(ajax=True)

class clusterservicenfschecklinksdata(Page):
    def _action(self):
        params = web.input()
        servicename = params['service_name']
        nfschecklinksdata = clusservicelib.func_service_list_nfs_links(servicename)
        return simplejson.dumps(nfschecklinksdata)
    def POST(self):
        return self.action(ajax=True)
    
class clusterservicenfsdellink(Page):
    def _action(self):
        params = web.input()
        servicename = params['service_name']
        nodename = params['node_name']
        tar_ip = params['targetip']
        ret = clusservicelib.func_service_del_nfs_links(servicename, nodename, tar_ip)
        return ret
    def POST(self):
        return self.action(ajax=True)
    
    
class clusterservicenfsadduser(Page):
    def _action(self):
        params = web.input()
        service_name = params['service_name']
        clusterservicename = params['service_name']
        userip = params['userip']
        retcode = clusservicelib.func_service_nfs_add_user(clusterservicename, userip)
        return retcode
    def POST(self):
        return self.action(ajax=True)
    
class clusterservicenfsdeluser(Page):
    def _action(self):
        params = web.input()
        service_name = params['service_name']
        clusterservicename = params['service_name']
        userip = params['userip']
        retcode = clusservicelib.func_service_nfs_del_user(clusterservicename, userip)
        return retcode
    def POST(self):
        return self.action(ajax=True)
		
		
class clusterservicesharemanage(Page):
    def _logic(self):
        clusterservice=clusservicelib.func_service_list_all()
        '''clusterservice=[]
        serviceinfos = clusservicelib.func_service_list_all()
        for serviceinfo in serviceinfos:
            clusterservice.append(serviceinfo['servicename'])'''
        self.setup = stow({
            'template':'clusterservicesharemanage'
        })
        self.content = stow({
            'clusterservice':clusterservice
        })
    def _action(self):
        params = web.input()
    def POST(self):
        return self.action(ajax=True)
    def GET(self):
        return self.render(ajax=True)
		
class clusterservicestart(Page):
    def _action(self):
        params = web.input()
        clusterservicename = params['clusterservicename']
        retcode = clusservicelib.func_service_start(clusterservicename)
        return retcode
    def POST(self):
        return self.action(ajax=True)

class clusterservicestop(Page):
    def _action(self):
        params = web.input()
        clusterservicename = params['clusterservicename']
        retcode = clusservicelib.func_service_stop(clusterservicename)
        return retcode
    def POST(self):
        return self.action(ajax=True)

class clusterservicedestroy(Page):
    def _action(self):
        params = web.input()
        clusterservicename = params['clusterservicename']
        retcode = clusservicelib.func_service_destroy(clusterservicename)
        return retcode
    def POST(self):
        return self.action(ajax=True)

class clusterservicerestart(Page):
    def _action(self):
        params = web.input()
        clusterservicename = params['clusterservicename']
        retcode = clusservicelib.func_service_restart(clusterservicename)
        clusservicelib.func_service_list_all()[0]['status']
        return retcode
    def POST(self):
        return self.action(ajax=True)

