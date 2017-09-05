#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import re
import subprocess
import simplejson
import traceback

currpath = os.path.join(os.getcwd(),os.path.dirname(__file__))
if currpath not in sys.path:
    sys.path.append(currpath)
from base import Page,stow,session,web,_
import settings
from libcommon import clusnodelib
from libcommon import clusgrouplib
from libcommon import clusservicelib

gmenus = ['clusternodeinfo','fg','clusternodenetwork','fg','clusternodedisk']#,'fg','clusternodefileshare']

class Node(Page):
    def _checknode(self):
        if not session.runtime.node:
            raise web.seeother('/clusternode')

class clusternode(Page):
    def _logic(self):
        self.content = stow({

        })
        self.setup = stow({
            'template':'clusternode',
            'breadcrumbs':['clusternode']
        })

    def GET(self):
        return self.render()

class clusternodeload(Page):
    def _logic(self):
        clusternodes = clusnodelib.func_node_list_all('True')
        print >> sys.stderr, session
        self.content = stow({
            'clusternodes':clusternodes
        })
        self.setup = stow({
            'template':'clusternodeload'
            #'jstemplate':['datatable_ZH']
        })
    def GET(self):
        return self.render(ajax=True)

class clustergetnode(Page):
    def _action(self):
        clusternodes = clusnodelib.func_node_list_all('True')
        return simplejson.dumps(clusternodes)
    def POST(self):
        return self.action(ajax=True)

class clusternodecreate(Page):
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

class clusternodereplace(Page):
    def _logic(self):
        self.setup = stow({
            'template':'clusternodereplace'
        })
    def _action(self):
        params = web.input()
        clusternodeold = params['clusternodeold']
        clusternodenew = params['clusternodenew']
        if not clusternodenew:
            return _("fillupclusternodeipaddr")
        else:
            retcode = clusnodelib.func_node_replace(clusternodeold,clusternodenew)
        return retcode
    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)

class clusternodecreatebyconfig(Page):
    def _logic(self):
        self.content = stow({

        })
        self.setup = stow({
            'template':'clusternodecreatebyconfig'
        })
    def _action(self):
        params = web.input()

    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)

class clusternodeview(Node):
    def _logic(self):
        params = web.input()
        node = 'node' in params and params['node'] or None
        print >> sys.stderr, node
        if node:
            session.runtime.node = node
        self._checknode()
        unit = session.runtime.unit
        #clusternodeinfo = clusnodelib.func_node_info(node)
        self.content = stow({
            'node':node
        })
        self.setup = stow({
            'template':'clusternodeview',
            'jstemplate':['pythonsysinfo'],
            'breadcrumbs':['clusternode','clusternodeview','clusternodeinfo'],
            'menus':gmenus,
            'currmenu':'clusternodeinfo'
        })
    def GET(self):
        return self.render(layout='node')

class clusternodeviewstaticinfo(Node):
    def _logic(self):
        params = web.input()
        self._checknode()
        self.setup = stow({
            'template':'clusternodestaticinfo'
        })
    def GET(self):
        return self.render(ajax=True)

class clusternodeviewstaticinfoxml(Node):
    def _logic(self):
        params = web.input()
        self._checknode()
        clusternodeinfo = clusnodelib.func_node_info(session.runtime.node, 'static')
        return clusternodeinfo
    def GET(self):
        web.header('Content-type','text/xml')
        return self.render(notemplate=True)

class clusternodeviewdynamicinfo(Node):
    def _logic(self):
        params = web.input()
        self._checknode()
        self.setup = stow({
            'template':'clusternodedynamicinfo'
        })
    def GET(self):
        return self.render(ajax=True)

class clusternodeviewdynamicinfoxml(Node):
    def _logic(self):
        params = web.input()
        self._checknode()
        clusternodeinfo = clusnodelib.func_node_info(session.runtime.node, 'dynamic')
        return clusternodeinfo
    def GET(self):
        web.header('Content-type','text/xml')
        return self.render(notemplate=True)

class clusternodenetwork(Node):
    def _logic(self):
        self._checknode()
        node = session.runtime.node
        clusternodeifaceinfo = clusnodelib.func_node_iface_info(node)
        self.content = stow({
            'clusternodeifaceinfo':clusternodeifaceinfo
        })
        self.setup = stow({
            'template':'clusternodenetwork',
            'breadcrumbs':['clusternode','clusternodeview','clusternodenetwork'],
            'menus':gmenus,
            'currmenu':'clusternodenetwork'
        })
    def GET(self):
        return self.render(layout='node')

class clusternodenetworkload(Node):
    def _logic(self):
        self._checknode()
        node = session.runtime.node
        clusternodeifaceinfo = clusnodelib.func_node_iface_info(node)
        self.content = stow({
            'clusternodeifaceinfo':clusternodeifaceinfo
        })
        self.setup = stow({
            'jstemplate':['datatable_ZH'],
            'template':'clusternodenetworkload'
        })
    def GET(self):
        return self.render(ajax=True)

class clusternodesetipaddr(Node):
    def _logic(self):
        self._checknode()
        node = session.runtime.node
        clusternodenicinfo = clusnodelib.func_node_iface_info(node)
        for iface in clusternodenicinfo:
            if re.match('^bond',iface['devname']):
                clusternodenicinfo.pop(clusternodenicinfo.index(iface))
        self.content = stow({
            'clusternodenicinfo': clusternodenicinfo
        })
        self.setup = stow({
            'template':'clusternodesetipaddr'
        })
    def _action(self):
        params = web.input()
        node = session.runtime.node
        ifaceinfo = [params['clusternodenicinfo'],params['newipaddr'],params['newmask'],params['newgateway'],params['newbroadcast']]
        newifaceinfo = ' '.join(ifaceinfo)
        retcode = clusnodelib.func_node_ipaddr_set(node, newifaceinfo)
        return retcode
    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)

class clusternodesetipaddr_single(Node):
    def _logic(self):
        params = web.input()
        ifacename = params['iface']
        self._checknode()
        node = session.runtime.node
        clusternodenicinfo = clusnodelib.func_node_iface_info(node)
        clusternodeniciface = {}
        for iface in clusternodenicinfo:
            if ifacename in iface.values():
                clusternodeniciface = iface
        self.content = stow({
            'clusternodeniciface': clusternodeniciface
        })
        self.setup = stow({
            'template':'clusternodesetipaddr_single'
        })
    def _action(self):
        params = web.input()
        node = session.runtime.node
        ifaceinfo = [params['iface'],params['newipaddr'],params['newmask'],params['newgateway'],params['newbroadcast']]
        newifaceinfo = ' '.join(ifaceinfo)
        retcode = clusnodelib.func_node_ipaddr_set(node, newifaceinfo)
        return retcode

    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)

class clusternodesetbond(Node):
    def _logic(self):
        self._checknode()
        node = session.runtime.node
        clusternodenicinfo = clusnodelib.func_node_iface_info(node)
        self.content = stow({
            'clusternodenicinfo': clusternodenicinfo
        })
        self.setup = stow({
            'template':'clusternodesetbond'
        })
    def _action(self):
        params = web.input(clusternewifacedev=[])
        node = session.runtime.node
        ifaceinfo = ' '.join(params['clusternewifacedev'])
        level_str = params['clusternewifacelevel']
        if level_str == 'Balance Round-Robin':
            level = '0'
        elif level_str =='Active Backup':
            level = '1'
        elif level_str =='Balance - XOR':
            level = '2'
        elif level_str =='Broadcast':
            level = '3'
        elif level_str =='802.3ad':
            level = '4'
        elif level_str =='Balance-tlb':
            level = '5'
        elif level_str =='Balance-alb':
            level = '6'
        retcode = clusnodelib.func_node_bond_set(node, level, ifaceinfo)
        return retcode
    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)

class clusternodebonddel(Node):
    def _action(self):
        node = session.runtime.node
        params = web.input()
        clusternodebondname = params['clusternodebondname']
        retcode = clusnodelib.func_node_bond_del(node, clusternodebondname)
        return retcode
    def POST(self):
        return self.action(ajax=True)

class clusternodedisk(Node):
    def _logic(self):
        node = session.runtime.node
        unit = session.runtime.unit
        clusternodediskinfo = clusnodelib.func_node_disk_info(node,unit)
        clusternoderaidinfo = clusnodelib.func_node_raid_info(node,unit)
        self.content = stow({
            'clusternodediskinfo':clusternodediskinfo,
            'clusternoderaidinfo':clusternoderaidinfo,
			'is_service':'0'
        })
        self.setup = stow({
            'template':'clusternodedisk',
            'breadcrumbs':['clusternode','clusternodeview','clusternodedisk'],
            'menus':gmenus,
            'currmenu':'clusternodedisk',
        })
    def GET(self):
        return self.render(layout = 'node')

class clusternoderaidload(Node):
    def _logic(self):
        node = session.runtime.node
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

class clusternoderaidprogress(Node):
    def _action(self):
        params = web.input()
        node = session.runtime.node
        clusternoderaidprogress = {}
        clusternoderaidprogress = clusnodelib.func_node_raid_progress(node,params['raidname'])
        return simplejson.dumps(clusternoderaidprogress)

    def POST(self):
        return self.action(ajax=True)
class clusternoderaidcreate(Node):
    def _logic(self):
        #node = session.runtime.node
        params = web.input()
        node = params['node']
        unit = session.runtime.unit
        clusternodediskunused = []
        for disk in clusnodelib.func_node_disk_info(node,unit):
            if disk['status'] == 'unused' and disk['type'] != 'raid':
                clusternodediskunused.append(disk['devname'])
        self.content = stow({
            'clusternodediskunused': clusternodediskunused,
        })
        self.setup = stow({
            'template':'clusternoderaidcreate'
        })
    def _action(self):
        #node = session.runtime.node
        params = web.input()
        node = params['node']
        params = web.input(clusternewraiddev=[])
        clusternewraiddev = ' '.join(params['clusternewraiddev'])
        clusterraidlv = params['clusterraidlv']
        if clusterraidlv == 'RAID0':
            clusterraidlv = '0'
        elif clusterraidlv == 'RAID1':
            clusterraidlv = '1'
        elif clusterraidlv == 'RAID10':
            clusterraidlv = '10'
        elif clusterraidlv == 'RAID5':
            clusterraidlv = '5'
        elif clusterraidlv == 'RAID6':
            clusterraidlv = '6'
        retcode = clusnodelib.func_node_raid_create(node, clusterraidlv, clusternewraiddev)
        return retcode
    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)

class clusternoderaiddel(Node):
    def _action(self):
        #node = session.runtime.node
        params = web.input()
        node=params['node']
        clusternoderaidname = params['clusternoderaidname']
        retcode = clusnodelib.func_node_raid_del(node, clusternoderaidname)
        return retcode
    def POST(self):
        return self.action(ajax=True)

class clusternoderaidset_hs(Node):
    def _logic(self):
        node = session.runtime.node
        clusternodediskunused = []
        clusternoderaid = []
        for disk in clusnodelib.func_node_disk_info(node):
            if disk['status'] == 'unused' and disk['type'] != 'raid':
                clusternodediskunused.append(disk['devname'])
            if disk['type'] == 'raid' and disk['vandor'] != '0':
                clusternoderaid.append(disk['devname'])
        self.content = stow({
            'clusternodediskunused': clusternodediskunused,
            'clusternoderaid': clusternoderaid
        })
        self.setup = stow({
            'template':'clusternoderaidset_hs'
        })
    def _action(self):
        node = session.runtime.node
        params = web.input(clusternewraiddev_hs=[])
        clusternewraiddev_hs = ' '.join(params['clusternewraiddev_hs'])
        clusterraidname = params['clusterraidname']
        retcode = clusnodelib.func_node_raid_set_hs(node, clusterraidname, clusternewraiddev_hs)
        return retcode
    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)

class clusternoderaiddel_hs(Node):
    def _logic(self):
        node = session.runtime.node
        unit = session.runtime.unit
        clusternoderaid = []
        clusternoderaidinfo = clusnodelib.func_node_list_raid(node, '')
        for raid in clusnodelib.func_node_disk_info(node):
            if raid['type'] == 'raid':
                clusternoderaid.append(raid['devname'])
        self.content = stow({
            'clusternoderaid': clusternoderaid
        })
        self.setup = stow({
            'template':'clusternoderaiddel_hs'
        })
    def _action(self):
        node = session.runtime.node
        params = web.input(clusterraiddev_hs=[])
        clusterraiddev_hs = ' '.join(params['clusterraiddev_hs'])
        clusterraidname = params['clusterraidname']
        retcode = clusnodelib.func_node_raid_del_hs(node, clusterraidname, clusterraiddev_hs)
        return retcode
    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)

class clusternoderaiddel_select(Node):
    def _action(self):
        node = session.runtime.node
        params = web.input()
        clusterraidname = params['clusterraidname']
        clusterraiddev_hs = clusnodelib.func_node_list_raid(node, '')
        if clusterraidname in clusterraiddev_hs:
            return simplejson.dumps(clusterraiddev_hs[clusterraidname])
        else:
            return simplejson.dumps([])
    def POST(self):
        return self.action(ajax=True)

class clusternoderaid_active(Node):
    def _logic(self):
        node = session.runtime.node
        clusternoderaid_inactive = clusnodelib.func_node_list_inactive(node)
        self.content = stow({
            'clusternoderaid_inactive': clusternoderaid_inactive
        })
        self.setup = stow({
            'template':'clusternoderaid_active'
        })
    def _action(self):
        node = session.runtime.node
        params = web.input(clusternoderaidname=[])
        raids = params['clusternoderaidname']
        raids = params['clusternoderaidname'][0].split(',')
        if len(raids) < 2:
            retcode = clusnodelib.func_node_raid_active(node, raids[0])
            return retcode
        else:
            retcodes = []
            for raid in raids:
                retcode = clusnodelib.func_node_raid_active(node, raid)
                if retcode == '0':
                    retcodes.append(retcode)
                else:
                    retcodes.append(raid)
            return simplejson.dumps(retcodes)
    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)

class clusternodedisk_active(Node):
    def _action(self):
        node = session.runtime.node
        params = web.input()
        disk = params['clusternodediskname']
        retcode = clusnodelib.func_node_disk_active(node, disk)
        return retcode
    def POST(self):
        return self.action(ajax=True)

class clusternodediskmap(Node):
    def _logic(self):
	'''try:
            node = session.runtime.node
            self.content = stow({
                'clusternodediskmap': clusternodediskmap
            })
            self.setup = stow({
                'template':'clusternodediskmap'
            })
        except:
            print >> sys.stderr, traceback.print_exc()'''
        unit = session.runtime.unit
        clusternodes=clusnodelib.func_node_list_all('True')
        params = web.input()	
        self.content = stow({
            'clusternodes':clusternodes,
            'node':params['node'],
            'disk':params['disk'],
            'unit':unit
        })
        self.setup = stow({
            'template':'clusternodediskmap'
        })
			
    def _action(self):
        unit = session.runtime.unit
        params = web.input()
        node=params['node']
        clusternodediskinfo = clusnodelib.func_node_disk_info(node,unit)
        return simplejson.dumps(clusternodediskinfo)

    def GET(self):
        return self.render(ajax=True)

    def POST(self):
        return self.action(ajax=True)

class clusternodedisk_update(Node):
    def _action(self):
        #node = session.runtime.node
        node = 'all'
        retcode = clusnodelib.func_node_disk_update(node)
        return retcode
    def POST(self):
        return self.action(ajax=True)
		
#¶àÑ¡²Ù×÷
class clusternodedisk_muti_op(Page):
    def _action(self):
        #node = session.runtime.node
        node = ''
        params = web.input()
        retcode = clusnodelib.func_node_disk_muti_op(params['type'],node,params['disk_str'])
        return retcode
    def POST(self):
        return self.action(ajax=True)

class clusternodedeletesingle(Page):
    def _action(self):
        params = web.input()
        clusternodeipaddr = params['clusternodeipaddr']
        retcode = clusnodelib.func_node_delete(clusternodeipaddr)
        return retcode
    def POST(self):
        return self.action(ajax=True)
    
class clusternodecifsrestart(Page):
    def _action(self):
        params = web.input()
        clusternodename = params['clusternodename']
        retcode = clusnodelib.func_node_cifs_restart(clusternodename)
        return retcode
    def POST(self):
        return self.action(ajax=True)
    
class clusternodenfsrestart(Page):
    def _action(self):
        params = web.input()
        clusternodename = params['clusternodename']
        retcode = clusnodelib.func_node_nfs_restart(clusternodename)
        return retcode
    def POST(self):
        return self.action(ajax=True)

#class clusternodefileshare(Node):
#    def _logic(self):
#        node = session.runtime.node
#        clusternodediskinfo = clusnodelib.func_node_disk_info(node)
#        clusternoderaidinfo = clusnodelib.func_node_raid_info(node)
#        self.content = stow({
#            'clusternodediskinfo':clusternodediskinfo,
#            'clusternoderaidinfo':clusternoderaidinfo
#        })
#        self.setup = stow({
#            'template':'clusternodedisk',
#            'breadcrumbs':['clusternode','clusternodeview','clusternodefileshare'],
#            'menus':gmenus,
#            'currmenu':'clusternodefileshare',
#        })
#    def GET(self):
#        return self.render(ajax=True)

class clusternodereplacenodisk(Node):
    def _logic(self):
        node = session.runtime.node
        unit = session.runtime.unit
        clusternodediskunused = []
        clusterwarnservice = []
        clusterservice=[]
        for disk in clusnodelib.func_node_disk_info(node,unit):
            if disk['status'] == 'unused' and disk['type'] != 'raid':
                clusternodediskunused.append(disk['devname'])
        serviceinfos = clusservicelib.func_service_list_all()
        for serviceinfo in serviceinfos:
            clusterservice.append(serviceinfo['servicename'])
            if 'status' in serviceinfo and serviceinfo['status'] == 'Warnning':
                clusterwarnservice.append(serviceinfo['servicename'])
        self.content = stow({
            'clusternodediskunused': clusternodediskunused,
            'clusterwarnservice':clusterwarnservice,
            'clusterservice':clusterservice
        })
        self.setup = stow({
            'template':'clusternodereplacenodisk'
        })
    def _action(self):
        node = session.runtime.node
        #params = web.input(clusterreplacedisk=[])
        #clusterreplacedisk = ' '.join(params['clusterreplacedisk'])
        params = web.input()
        clusterreplacedisk = params['clusterreplacedisk']
        service = params['clusterservicename']
        format=params['format']
        ret = clusnodelib.func_node_disk_update(node)
        retcode = clusnodelib.func_node_replace_nodisk(node,service,clusterreplacedisk,format)
        return retcode
    def GET(self):
        return self.render(ajax=True)
    def POST(self):
        return self.action(ajax=True)

class clusternodegetservicenodiskinfo(Node):
    def _logic(self):
        params = web.input()
        nodisk_num = 0
        node = session.runtime.node
        servicename = params['servicename']
        retresult = clusservicelib.func_service_list_disk(servicename)
        if retresult and 'childs' in retresult:
            clusservicediskinfos = retresult['childs']
        for clusservicediskinfo in clusservicediskinfos:
            if 'childs' in clusservicediskinfo:
                for diskinfo in clusservicediskinfo['childs']:
                    disk = diskinfo['name'].split(':')
                    if disk[0] == node and disk[1] == 'no_disk':
                        nodisk_num += 1
        return nodisk_num
    def _action(self):
        params = web.input()
        servicename = params['servicename']
        service_disk=clusservicelib.func_raidlv_detail(servicename)
        #service_disk=clusservicelib.func_service_list_disk(servicename)
        service_disk_arr=[]
        for i in range(len(service_disk)):
            node=service_disk[i]['mount_point'].split(':')
            node=node[0]
            disk=service_disk[i]['interface'].replace('/dev/','')
            size=service_disk[i]['total']
            #print >> sys.stderr,service_disk[i]['total']
            #print >> sys.stderr,'/n'
            disk_str=node+':'+disk+'+'+size
            service_disk_arr.append(disk_str)
        service_disk_str=','.join(service_disk_arr)
        print >> sys.stderr,service_disk_str
        return service_disk_str
    def GET(self):
        return self.render(ajax=True,notemplate=True)
    def POST(self):
        return self.action(ajax=True)

class clusternodesession(Page):
    def _action(self):
        params = web.input()
        session.runtime.node=params['node']
    def POST(self):
        return self.action(ajax=True)
