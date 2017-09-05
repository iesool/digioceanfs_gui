#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import subprocess
import re
import copy
import utils
import traceback 
from threading import Thread 
from logger import logger
from logger import Ologger
from xml.dom import minidom
from read_from_pipe import *
import xml.etree.ElementTree as etree

currpath = os.path.join(os.getcwd(),os.path.dirname(__file__))
if not currpath in sys.path:
    sys.path.append(currpath)
homepath = currpath[:currpath.find('libcommon')]
if not homepath in sys.path:
    sys.path.append(homepath)
import settings
from base import _

def execute(cmd, tmp):
    proc = subprocess.Popen(cmd, shell=True, stdout=tmp)
    proc.wait()
    tmp.seek(0)

#########################################################################################################
#
#   Function: func_node_create
#   Variable: clusternodeipaddr, clustergroupname(non-essential), clusternodehostname(non-essential)
#   Purpose: add a new node for the cluster
#   Data structure: type: str or int
#
#########################################################################################################
def func_node_create(clusternodeipaddr, clustergroupname=None, clusternodehostname = ''):
    try:
        if clusternodehostname and clustergroupname != "none":
            cmd = "sudo python %s node add_by_hostname %s %s %s" % (settings.digimanager,clusternodeipaddr, clusternodehostname, clustergroupname)
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            Ologger.info(cmd)
        elif clusternodehostname and clustergroupname == "none":
            cmd = "sudo python %s node add_by_hostname %s %s" % (settings.digimanager,clusternodeipaddr, clusternodehostname)
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            Ologger.info(cmd)
        elif clustergroupname != "none":
            cmd = "sudo python %s node add %s %s" % (settings.digimanager,clusternodeipaddr,clustergroupname)
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            Ologger.info(cmd)
        else:
            cmd = "sudo python %s node add %s" % (settings.digimanager,clusternodeipaddr)
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            Ologger.info(cmd)
        retcode = proc.stdout.read().strip()
        proc.wait()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_node_replace
#   Variable: clusternodeold, clusternodenew
#   Purpose: to replace a old node(this maybe broken or has broken disks)
#   Data structure: type: str or int
#
#########################################################################################################
def func_node_replace(clusternodeold, clusternodenew):
    try:
        cmd = "sudo python %s node replace %s %s" % (settings.digimanager, clusternodeold, clusternodenew)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.read().strip()
        proc.wait()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

def func_node_createbyconfig(clusternodeconfig):
    try:
        cmd = "sudo python %s node add %s" % (settings.digimanager,clusternodeipaddr)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.read().strip()
        proc.wait()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_node_list_all
#   Variable: list_status(this variable is to decide if data is sent to the servers side ),
#             clusternodes
#   Purpose: to list all nodes info
#   Data structure: type: list,
#                   ex: [{'nodename':node1, 'ipaddr':ipaddr, 'diskinfo':diskinfo, 'status':status}, {...}, ...]
#
#########################################################################################################
def func_node_list_all(list_status):
    clusternodes = []
    key = ['nodename','ipaddr','diskinfo','cifsstatus','nfsstatus','status']
    if list_status == 'True':
        clusternodes_status = func_node_status()
        clusternodes_cifs_status = func_node_cifs_status()
        #clusternodes_nfs_status = func_node_nfs_status()clusternodes_nfs_status[value[0]],
        try:
            cmd = "sudo python %s node list" % settings.digimanager
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            Ologger.info(cmd)
            result = proc.stdout.readlines()
            proc.wait()
            retcode = result.pop(0).strip()
            if retcode != '0':
                return retcode
            else:
                result.pop(-1)
                p = '^(\S+)\s(\S+)\s+$'
                for v in result:
                    m = re.match(p, v)
                    if m:
                        value = list(m.groups())
                        nodeinfo = [[],clusternodes_cifs_status[value[0]],'',clusternodes_status[value[0]]]
                        value.extend(nodeinfo)
                        d = dict(zip(key,value))
                        clusternodes.append(d)
                return clusternodes
        except Exception,e:
            logger.debug(e)
            return clusternodes
    else:
        try:
            cmd = "sudo python %s node list" % settings.digimanager
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            Ologger.info(cmd)
            result = proc.stdout.readlines()
            proc.wait()
            retcode = result.pop(0).strip()
            if retcode != '0':
                return retcode
            else:
                result.pop(-1)
                p = '^(\S+)\s(\S+)\s+$'
                for v in result:
                    m = re.match(p, v)
                    if m:
                        value = list(m.groups())
                        nodeinfo = [[],'false']
                        value.extend(nodeinfo)
                        d = dict(zip(key,value))
                        clusternodes.append(d)
                return clusternodes
        except Exception,e:
            logger.debug(e)
            return clusternodes

#########################################################################################################
#
#   Function: func_node_status
#   Variable: list_status(this variable is to decide if data is sent to the servers side ),
#             clusternodes
#   Purpose: to replace a old node(this maybe broken or has broken disks)
#   Data structure: type: list,
#                   ex: [{'nodename':node1, 'ipaddr':ipaddr, 'diskinfo':diskinfo, 'status':status}, {...}, ...]
#
#########################################################################################################
def func_node_status():
    '''{'node-1':'start', 'node-2':'stop'}'''
    nodes_status = dict()
    try:
        cmd = 'sudo python %s node status' % settings.digimanager
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        retcode = result[0].strip()
        if retcode == '0':
            p = '^(\S+)\t(\S+)\s+'
            for line in result[1:-1]:
                status = re.findall(p, line)
                nodes_status[status[0][0]] = status[0][1]
            return nodes_status
        else:
            return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return nodes_status
    
def func_node_cifs_status():
    '''{'node-1':'start', 'node-2':'stop'}'''
    nodes_status = dict()
    try:
        cmd = 'sudo python %s node cifs_status' % settings.digimanager
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        retcode = result[0].strip()
        if retcode == '0':
            p = '^(\S+)\t(\S+)\s+'
            for line in result[1:-1]:
                status = re.findall(p, line)
                nodes_status[status[0][0]] = status[0][1]
            return nodes_status
        else:
            return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return nodes_status
    
def func_node_cifs_restart(nodename):
    try:
        cmd = 'sudo python %s node cifs_restart %s' % (settings.digimanager, nodename)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.readlines()[0].strip()
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)
    
def func_node_nfs_status():
    '''{'node-1':'start', 'node-2':'stop'}'''
    nodes_status = dict()
    try:
        cmd = 'sudo python %s node nfs_status' % settings.digimanager
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        retcode = result[0].strip()
        if retcode == '0':
            p = '^(\S+)\t(\S+)\s+'
            for line in result[1:-1]:
                status = re.findall(p, line)
                nodes_status[status[0][0]] = status[0][1]
            return nodes_status
        else:
            return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return nodes_status

def func_node_nfs_restart(nodename):
    try:
        cmd = 'sudo python %s node nfs_restart %s' % (settings.digimanager, nodename)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.readlines()[0].strip()
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

def func_node_info(node, infotype):
    try:
        cmd = 'sudo python %s node list_%s_info %s' % (settings.digimanager, infotype, node)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        proc.wait()
        result_proc = proc.stdout.readlines()
        retcode = result_proc[0].strip()
        f = open('/etc/digioceanfs_manager/nodes/' + node + '_' + infotype + 'sysinfo','r')
        str = f.read()
        result_xml = str.split('\n')
        xml_str = ''.join(str.split('\n')[1:])
        xml_dom = minidom.parseString(xml_str)
        if retcode == '0':
            return xml_dom.toxml()#.replace('\t','')
        else:
            return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_node_raid_info
#   Variable: node,
#             unit(this variable is to decide unit of return value),
#             clusternoderaidinfo
#   Purpose: to list disks info in a raid
#   Data structure: type: list,
#                   ex: [{'status':status, 'devname':devname, 'type':type, 'vandor':vandor, 'sn_number':sn_number, 'size':size, 'type_in_raid':type_in_raid, 'raidname':raidname},
#                        {...},
#                        ...]
#
#########################################################################################################
def func_node_raid_info(node,unit=''):
    clusternoderaidinfo = []
    key = ['position','status','devname','type','vandor','sn_number','size','type_in_raid','raidname','nodename']
    try:
        cmd = 'sudo python %s node list_disk %s' % (settings.digimanager, node)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        proc.wait()
        result = proc.stdout.readlines()
        #print >> sys.stderr, result
        if result[0].strip() != '0':
            return retcode == '0' and retcode or _(retcode)
        else:
            disklist = []
            flag = -1
            for raid in result[1:-1]:
                raidinfo = raid.split()
                #print >> sys.stderr, raidinfo
                diskinfo = raid.split('\t')
                if len(diskinfo) < 2:
                    disklist.append(diskinfo[0].strip())
                    flag += 1
					
                if 'in_raid' in raidinfo:
                    d = dict(zip(key,raidinfo))
                    d['size'] = utils.getUnit(unit, d['size'])
                    if node=='':
                        d['nodename'] = disklist[flag]
                    else:
                        d['nodename']=node
                    clusternoderaidinfo.append(d)
            return clusternoderaidinfo
    except Exception,e:
        logger.debug(e)
        return clusternoderaidinfo

def func_node_list_raid(node, unit=''):
    clusternoderaidinfo = {}
    try:
        cmd = 'sudo python %s node list_raid %s' % (settings.digimanager, node)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0].strip()
        p = 'hot_spare'
        if retcode == '0':
            for line in result[1:-1]:
                if p in line.split():
                    dataline = line.split()
                    raidname = dataline[-1].strip()
                    if raidname not in clusternoderaidinfo:
                        clusternoderaidinfo[raidname] = []
                        clusternoderaidinfo[raidname].append(dataline[2].strip())
                    else:
                        clusternoderaidinfo[raidname].append(dataline[2].strip())
            else:
                return clusternoderaidinfo
        else:
            return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

def func_node_raid_status():
    event_dict = readFromRaidPipe()
    raidstatus = event_dict
    if raidstatus:
        return raidstatus


#########################################################################################################
#
#   Function: func_node_raid_progress
#   Variable: node,
#             clusternoderaidinfo
#   Purpose: to check out the status of raid that is synchronizing
#   Data structure: type: list,
#                   ex: [{'name':name, 'level':level, 'status':status, 'progress':progress},
#                        {...},
#                        ...]
#
#########################################################################################################
def func_node_raid_progress(node, raidname):
    clusternoderaidprogress = {}
    try:
        cmd = 'sudo python %s node raid_info %s %s' % (settings.digimanager, node, raidname)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        if retcode == '0\n':
            for res in result[1:5]:
                res = res.strip()
                res = res.split(': ')
                if res[0] == 'raid name':
                    clusternoderaidprogress['name'] = res[1]
                elif res[0] == 'raid level':
                    clusternoderaidprogress['level'] = res[1]
                elif res[0] == 'raid status':
                    clusternoderaidprogress['status'] = res[1]
                else:
                    clusternoderaidprogress['progress'] = res[1]
        return clusternoderaidprogress
    except Exception,e:
        logger.debug(e)
        return clusternoderaidprogress

#########################################################################################################
#
#   Function: func_node_disk_info
#   Variable: node(if this is default, list all the disk in cluster),
#             unit(this variable is to decide unit of return value),
#             clusternoderaidinfo
#   Purpose: to list disks info in a node or a cluster
#   Data structure: type: list,
#                   ex: [{'status':status, 'devname':devname, 'type':type, 'vandor':vandor, 'sn_number':sn_number, 'size':size, 'port':port,'servicename':raidname, 'istart':istart, 'pid':pid},
#                        {...},
#                        ...]
#
#########################################################################################################
def func_node_disk_info(node='',unit=''):
    retcode = '0'
    clusternodediskinfo = []
    key_nodisk = ['position','nodisk', 'devname']
    key_raid = ['position','status','devname','type','vandor','sn_number','size','port','raidname','istart','pid']
    key_service = ['position','status','devname','type','vandor','sn_number','size','port','servicename','istart','pid']
    try:
        if node != '':
            cmd = 'sudo python %s node list_disk %s' % (settings.digimanager, node)
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            Ologger.info(cmd)
            result = proc.stdout.readlines()
            proc.wait()
            for res in result[1:-1]:
                print >> sys.stderr,'1111111111111111111111111111111111'
                print >> sys.stderr,res.split()
                if len(res.split()) <= 3:
                    diskinfo = res.split()
                    '''diskinfo.extend(['-','-','-','-','-','-','-','-'])
                    #d = dict(zip(key_nodisk,diskinfo))
                    d = dict(zip(key_raid,diskinfo))
                    d['nodename'] = node
                    d['size'] = utils.getUnit(unit, d['size'])
                    print >> sys.stderr,d'''
                    disk = dict()
                    disk['position'] = '-'
                    disk['status'] = diskinfo[1].strip()
                    disk['devname'] = diskinfo[2].strip()
                    disk['type'] = '-'
                    disk['vandor'] = '-'
                    disk['sn_number'] = '-'
                    disk['size'] = '-'
                    disk['port'] = '-'
                    disk['nodename'] = '-'
                    disk['size'] = '-'
                    clusternodediskinfo.append(disk)
                    continue
                diskinfo = res.split()
                for i in range(len(diskinfo)):
                    diskinfo[i] = diskinfo[i].strip()
                if diskinfo[1] == "in_raid":
                    d = dict(zip(key_raid,diskinfo))
                else:
                    d = dict(zip(key_service,diskinfo))
                d['nodename'] = node
                d['size'] = utils.getUnit(unit, d['size'])
                clusternodediskinfo.append(d)
                print >> sys.stderr,clusternodediskinfo
            return clusternodediskinfo
        else:
            cmd = 'sudo python %s node list_disk %s' % (settings.digimanager, node)
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            Ologger.info(cmd)
            result = proc.stdout.readlines()
            proc.wait()
            disklist = []
            flag = -1
            retcode = result[0]
            if retcode == '0\n':
                for res in result[1:-1]:
                    disk = dict()
                    diskinfo = res.split('\t')
                    #print >> sys.stderr, diskinfo
                    if len(diskinfo) < 2:
                        disklist.append(diskinfo[0].strip())
                        flag += 1
                    elif len(diskinfo) == 3:
                        disk['position'] = diskinfo[0].strip()
                        disk['status'] = diskinfo[1].strip()
                        disk['devname'] = diskinfo[2].strip()
                        disk['type'] = '-'
                        disk['vandor'] = '-'
                        disk['sn_number'] = '-'
                        disk['size'] = '-'
                        disk['port'] = '-'
                        disk['nodename'] = '-'
                        disk['size'] = '-'
                        clusternodediskinfo.append(disk)
                    elif len(diskinfo) <= 8:
                        disk['position'] = diskinfo[0].strip()
                        disk['status'] = diskinfo[1].strip()
                        disk['devname'] = diskinfo[2].strip()
                        disk['type'] = diskinfo[3].strip()
                        disk['vandor'] = diskinfo[4].strip()
                        disk['sn_number'] = diskinfo[5].strip()
                        disk['size'] = diskinfo[6].strip()
                        disk['port'] = diskinfo[7].strip()
                        disk['nodename'] = disklist[flag]
                        disk['size'] = utils.getUnit(unit, disk['size'])
                        clusternodediskinfo.append(disk)
                    else:
                        if diskinfo[1].strip()=='no_disk':
                            disk['position'] = '-'
                            disk['status'] = diskinfo[1].strip()
                            disk['devname'] = diskinfo[2].strip()
                            disk['type'] = '-'
                            disk['vandor'] = '-'
                            disk['sn_number'] = '-'
                            disk['size'] = '-'
                            disk['port'] = '-'
                            disk['nodename'] = '-'
                            disk['size'] = '-'
                        else:
                            disk['position'] = diskinfo[0].strip()
                            disk['status'] = diskinfo[1].strip()
                            disk['devname'] = diskinfo[2].strip()
                            disk['type'] = diskinfo[3].strip()
                            disk['vandor'] = diskinfo[4].strip()
                            disk['sn_number'] = diskinfo[5].strip()
                            disk['size'] = diskinfo[6].strip()
                            disk['port'] = diskinfo[7].strip()
                            if disk['status'] == 'in_raid':
                                disk['raidname'] = diskinfo[8].strip()
                            else:
                                disk['servicename'] = diskinfo[8].strip()
                            disk['istart'] = diskinfo[9].strip()
                            disk['nodename'] = disklist[flag]
                            disk['size'] = utils.getUnit(unit, disk['size'])
                        clusternodediskinfo.append(disk)
                print >> sys.stderr, clusternodediskinfo
                return clusternodediskinfo
            else:
                return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)



#########################################################################################################
#
#   Function: func_node_iface_info
#   Variable: node,
#             clusternodeifaceinfo
#   Purpose: to list disks info in a raid
#   Data structure: type: list,
#                   ex: [{'status':status, 'devtype':devtype, 'mac':mac, 'ipaddr':ipaddr, 'broadcast':broadcast, 'netmask':netmask, 'status':status},
#                        {...},
#                        ...]
#
#########################################################################################################
def func_node_iface_info(node):
    clusternodeifaceinfo = []
    key = ['devname','devtype','mac','ipaddr','broadcast','netmask','status']
    try:
        cmd = 'sudo python %s node list_nic %s' % (settings.digimanager, node)
        proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        for res in result[1:-1]:
            nicinfo = res.split('\t')
            nicinfo.pop(-1)
            if len(nicinfo) == 2:
                nicinfo = [nicinfo[1],'','','','','down']
                d = dict(zip(key,nicinfo))
            elif len(nicinfo) == 7:
                nicinfo.append('ok')
                d = dict(zip(key,nicinfo[1:]))
            elif len(nicinfo) > 7:
                sub_nic = nicinfo[7:]
                nicinfo = nicinfo[:7]
                nicinfo.append('ok')
                d = dict(zip(key,nicinfo[1:]))
                d['sub_nic'] = sub_nic
            else:
                continue
            clusternodeifaceinfo.append(d)
        return clusternodeifaceinfo
    except Exception,e:
        logger.debug(e)
        return clusternodeifaceinfo

#########################################################################################################
#
#   Function: func_node_ipaddr_set
#   Variable: node,
#             newifaceinfo
#   Purpose: change an old ipaddr
#   Data structure: type: str or int
#
#########################################################################################################
def func_node_ipaddr_set(node, newifaceinfo):
    try:
        cmd = 'sudo python %s node ip_set %s %s' % (settings.digimanager, node, newifaceinfo)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.readlines()[0].strip()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_node_bond_set
#   Variable: node,
#             level,
#             newifaceinfo
#   Purpose: create a netcard bond
#   Data structure: type: str or int
#
#########################################################################################################
def func_node_bond_set(node, level, newifacename):
    try:
        cmd = 'sudo python %s node bond_set %s %s %s' % (settings.digimanager, node, level, newifacename)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.readlines()[0].strip()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_node_bond_set
#   Variable: node,
#             bondname
#   Purpose: delete a bond
#   Data structure: type: str or int
#
#########################################################################################################
def func_node_bond_del(node, bondname):
    try:
        cmd = 'sudo python %s node bond_del %s %s' % (settings.digimanager, node, bondname)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.readlines()[0].strip()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_node_raid_create
#   Variable: node,
#             clusterraidlv,
#             clusternewraiddev
#   Purpose: create a raid
#   Data structure: type: str or int
#
#########################################################################################################
def func_node_raid_create(node, clusterraidlv, clusternewraiddev):
    try:
        cmd = 'sudo python %s node raid_create %s %s 256 %s' % (settings.digimanager, node, clusterraidlv, clusternewraiddev)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.readlines()[0].strip()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_node_raid_del
#   Variable: node,
#             clusterraidlv,
#             clusternewraiddev
#   Purpose: delete a raid
#   Data structure: type: str or int
#
#########################################################################################################
def func_node_raid_del(node, raidname):
    try:
        cmd = 'sudo python %s node raid_del %s %s' % (settings.digimanager, node, raidname)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.readlines()[0].strip()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_node_raid_del
#   Variable: node,
#             clusterraidname,
#             clusternewraiddev_hs
#   Purpose: set a hot spire disk for a raid
#   Data structure: type: str or int
#
#########################################################################################################
def func_node_raid_set_hs(node, clusterraidname, clusternewraiddev_hs):
    try:
        cmd = 'sudo python %s node raid_hs_set %s %s %s' % (settings.digimanager, node, clusterraidname, clusternewraiddev_hs)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.readlines()[0].strip()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_node_raid_del_hs
#   Variable: node,
#             clusterraidname,
#             clusternewraiddev_hs
#   Purpose: delete a hot spire disk from a raid
#   Data structure: type: str or int
#
#########################################################################################################
def func_node_raid_del_hs(node, clusterraidname, clusterraiddev_hs):
    try:
        cmd = 'sudo python %s node raid_hs_del %s %s %s' % (settings.digimanager, node, clusterraidname, clusterraiddev_hs)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.readlines()[0].strip()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_node_disk_update
#   Variable: node
#   Purpose: update disks status
#   Data structure: type: str or int
#
#########################################################################################################
import sys
from subprocess import PIPE, Popen
from threading  import Thread

try:
    from Queue import Queue, Empty
except ImportError:
    from queue import Queue, Empty  # python 3.x

ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, queue):
    for line in iter(out.readline, ''):
        queue.put(line)
    #out.close()


def func_node_disk_update(node):
    try:
        cmd = 'sudo python %s node update_disk %s' % (settings.digimanager, node)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        retcode = proc.stdout.readlines()[0].strip()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        print traceback.print_exc()
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

def func_node_processing():
    process_word = readFromProcessPipe()
    if process_word:
        return process_word 

#########################################################################################################
#
#   Function: func_node_list_inactive
#   Variable: node,
#             clusternodedisk_inactive,
#             clusternoderaids
#   Purpose: list all the disks which status is inactive
#   Data structure: type: list
#                   ex: [{'devname':devname, 'disknum':disknum, 'child': [disk1, disk2, disk3,...]},
#                        {},...]
#
#########################################################################################################
def func_node_list_inactive(node):
    clusternoderaid_inactive = []
    inactivedisklist = []
    clusternoderaids = []
    flag = -1
    try:
        cmd = 'sudo python %s node list_inactive %s' % (settings.digimanager, node)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        retcode = result[0].strip()
        result_str = result[1:]
        if retcode == '0':
            for res in result_str[0:-1]:
                print >> sys.stderr, res 
                disk_inactive = {}
                disk_inactive['raidname'] = res.split()[0]
                disk_inactive['normal_count'] = res.split()[1]
                disk_inactive['diskname'] = res.split()[2]
                disk_inactive['disk_type'] = res.split()[3]
                disk_inactive['belong_raid_uuid'] = res.split()[-1]
                inactivedisklist.append(disk_inactive)
        else:
            return retcode
        if inactivedisklist:
            for disk in inactivedisklist:
                if not clusternoderaid_inactive:
                    raid_inactive = {}
                    raid_inactive['devname'] = disk['raidname']
                    raid_inactive['normal_count'] = int(disk['normal_count'])
                    raid_inactive['disk_num'] = 1 
                    raid_inactive['child'] = [{disk['diskname']: disk['disk_type']}]
                    raid_inactive['uuid'] = disk['belong_raid_uuid']
                    clusternoderaid_inactive.append(raid_inactive)
                else:
                    _clusternoderaid_inactive = clusternoderaid_inactive
                    flag = False
                    for raid in _clusternoderaid_inactive:
                        if raid['uuid'] == disk['belong_raid_uuid']:
                            raid['child'].append({disk['diskname']: disk['disk_type']})
                            raid['disk_num'] += 1
                            flag = True
                            break
                    if not flag:
                        raid_inactive = {}
                        raid_inactive['devname'] = disk['raidname']
                        raid_inactive['normal_count'] = int(disk['normal_count'])
                        raid_inactive['disk_num'] = 1 
                        raid_inactive['child'] = [{disk['diskname']: disk['disk_type']}]
                        raid_inactive['uuid'] = disk['belong_raid_uuid']
                        clusternoderaid_inactive.append(raid_inactive)
                            
            print >> sys.stderr, clusternoderaid_inactive
            return clusternoderaid_inactive
        else:
            return []
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_node_raid_update
#   Variable: node,
#             raids
#   Purpose: active raids that needed
#   Data structure: type: str or int
#
#########################################################################################################
def func_node_raid_active(node, raids):
    try:
        cmd = 'sudo python %s node raid_active %s %s' % (settings.digimanager, node, raids)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.readlines()[0].strip()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_node_disk_active
#   Variable: node,
#             disk
#   Purpose: disactive disks that needed
#   Data structure: type: str or int
#
#########################################################################################################
def func_node_disk_active(node, disk):
    try:
        cmd = 'sudo python %s node raid_disactive %s %s' % (settings.digimanager, node, disk)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.readlines()[0].strip()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#¶àÑ¡²Ù×÷		
def func_node_disk_muti_op(type,node,disk_str):
    try:
        #print >> sys.stderr,disk_str
        arr={}
        disk_arr=disk_str.split(" ")
        for i in range(len(disk_arr)):
            node_arr=disk_arr[i].split(":")
            if node_arr[0] not in arr:
                arr[node_arr[0]]=[node_arr[1]]
            else:
                arr[node_arr[0]].append(node_arr[1])
        #print >> sys.stderr,arr
        #return '0'
        for node, disk_list in arr.iteritems():
            disk_str=" ".join(disk_list)
            if type=='active':
                cmd = 'sudo python %s node raid_disactive %s %s' % (settings.digimanager, node, disk_str)
            elif type=='format':
                cmd = 'sudo python %s node format_disk %s %s' % (settings.digimanager, node, disk_str)
            else:
                cmd = 'sudo python %s node reset_disk %s %s' % (settings.digimanager, node, disk_str)
            #print >> sys.stderr,cmd		
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            Ologger.info(cmd)
            retcode = proc.stdout.readlines()[0].strip()
            if retcode!='0':
                retcode=retcode.split(':')
                retcode=retcode[0]
                break
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)
#########################################################################################################
#
#   Function: func_node_delete
#   Variable: node,
#   Purpose: delete node in cluster
#   Data structure: type: str or int
#
#########################################################################################################
def func_node_delete(node):
    try:
        cmd = 'sudo python %s node del %s'% (settings.digimanager, node)
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.read().strip()
        proc.wait()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_node_get_device_id
#   Variable: node,
#   Purpose: get node device id in cluster
#   Data structure: type: str or int
#
#########################################################################################################
def func_node_get_device_id(node):
    try:
        cmd = 'sudo python %s node get_device_id %s' % (settings.digimanager, node)
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
        Ologger.info(cmd)
        proc.wait()
        result = proc.stdout.readlines()
        ret = result[0].strip()
        retcode = result[1].strip()
        if ret == "0":
            return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_node_check_license
#   Variable: node,
#   Purpose: check license on node in cluster
#   Data structure: type: str or int
#
#########################################################################################################
def func_node_check_license(node, nodelicense):
    try:
        cmd = 'sudo python %s node check_license %s %s' % (settings.digimanager, node, nodelicense)
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.read().strip()
        print >> sys.stderr, retcode
        proc.wait()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

def func_node_get_disk_lightstatus(node):
    disk_lightstatus = []
    if os.path.exists(settings.err_disks_dir):
        filelist = os.listdir(settings.err_disks_dir)
        for f in filelist:
            if f.find(node) >= 0:
                disk_lightstatus.append(f.split('-')[-1])
        return disk_lightstatus
    else:
        return []


def func_node_replace_nodisk(node,service,clusterreplacedisk,format=False):
    try:
        #cmd = 'sudo python %s node replace_nodisk %s %s %s' % (settings.digimanager, node, service, clusterreplacedisk)
        cmd = 'sudo python %s service replace_disk %s %s %s' % (settings.digimanager, service, clusterreplacedisk,format)
        print >> sys.stderr,cmd
        #return '0'
        proc = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.read().strip()
        #print >> sys.stderr, retcode
        proc.wait()
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

if __name__ == '__main__':
    func_node_disk_update('node-1')
