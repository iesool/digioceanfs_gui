#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import subprocess
import re
import copy
from logger import logger
from logger import Ologger

currpath = os.path.join(os.getcwd(),os.path.dirname(__file__))
homepath = currpath[:currpath.find('libcommon')]
if not homepath in sys.path:
    sys.path.append(homepath)
import settings
from base import _

def initglobal():
    pass

#########################################################################################################
#
#   Function: func_get_group
#   Variable: clustergroupname(non-essential), clustergroup
#   Purpose: return groupname of current cluster
#   Data structure: type: list, ex: [group1, group2, group3, ..., groupN ]
#
#########################################################################################################

def func_get_group(clustergroupname=None):
    clustergroup = {}
    try:
        cmd = "sudo python %s group list %s" % (settings.digimanager,clustergroupname)
        proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result.pop(0).strip()
        if retcode == '0':
            clustergroup['name'] = clustergroupname
            clustergroup['node'] = []
            for line in result:
                m = re.match('^\s+(\S+)\s+(\S+)\s$',line)
                if m:
                    clustergroup['node'].append(m.groups())
    except Exception,e:
        logger.debug(e)
        return clustergroup
    return clustergroup

#########################################################################################################
#
#   Function: func_group_list_all
#   Variable: groupname(non-essential), clustergroups, clustergroup_nodes
#   Purpose: return groupnames and nodenames of current cluster for the page of listing all group
#   Data structure: type: dict; ex: { group1: [node1, node2, ...,nodeN],
#                                     group2: [],
#                                     group3: [],
#                                     ...,
#                                     groupN: [] }
#
#########################################################################################################

def func_group_list_all(groupname=''):
    clustergroups = {}
    clustergroup_nodes = []
    if not groupname:
        try:
            cmd = "sudo python %s group list" % settings.digimanager
            proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
            Ologger.info(cmd)
            result = proc.stdout.readlines()
            proc.wait()
            retcode = result.pop(0).strip()
            if retcode == '0':
                clustergroup = None
                clustergroupnodes = []
                for line in result:
                    m = re.match('^\s+(\S+)\s+(\S+)\s+$',line)
                    if m:
                        clustergroupnodes.append(m.groups())
                    else:
                        m = re.match('^(\S+)\s+$',line)
                        if m:
                            if clustergroup:
                                clustergroups[clustergroup] = clustergroupnodes
                            clustergroup = m.group(1)
                            clustergroupnodes = copy.deepcopy([])
                clustergroups[clustergroup] = clustergroupnodes
                return clustergroups
        except Exception,e:
            logger.debug(e)
            return clustergroups
    else:
        try:
            cmd = "sudo python %s group list %s" % (settings.digimanager, groupname)
            proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
            Ologger.info(cmd)
            result = proc.stdout.readlines()
            proc.wait()
            retcode = result.pop(0).strip()
            if retcode == '0':
                for line in result[1:]:
                    m = re.match('^\s+(\S+)\s+(\S+)\s+$',line)
                    if m:
                        clustergroup_nodes.append(m.groups())
                return clustergroup_nodes
        except Exception,e:
            logger.debug(e)
            return clustergroup_nodes

#########################################################################################################
#
#   Function: func_group_rename
#   Variable: clustergroupoldname, clustergroupnewname
#   Purpose: rename the groupname
#   Data structure: type: str or int
#
#########################################################################################################

def func_group_rename(clustergroupoldname,clustergroupnewname):
    try:
        cmd = "sudo python %s group rename %s %s" % (settings.digimanager,clustergroupoldname,clustergroupnewname)
        proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
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
#   Function: func_group_add_node
#   Variable: clustergroupname, clusternodename(non-essential)
#   Purpose: add new or old node for a group
#   Data structure: type: str or int;
#
#########################################################################################################

def func_group_add_node(clustergroupname,clusternodename=[]):
    retcode = '0'
    try:
        for nodename in clusternodename:
            cmd = "sudo python %s node setgroup %s %s" % (settings.digimanager, nodename, clustergroupname)
            proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
            Ologger.info(cmd)
            ret = proc.stdout.read().strip()
            proc.wait()
            if ret != '0':
                retcode = ret.split(':')
                retcode=retcode[0]	
                break
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_group_del_node
#   Variable: clustergroupname, clusternodename(non-essential)
#   Purpose: add new or old node for a group
#   Data structure: type: str or int;
#
#########################################################################################################

def func_group_del_node(clusternodename=[]):
    retcode = '0'
    try:
        for nodename in clusternodename:
            cmd = "sudo python %s node setgroup %s" % (settings.digimanager, nodename)
            print >> sys.stderr, cmd
            proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
            Ologger.info(cmd)
            ret = proc.stdout.read().strip()
            print >> sys.stderr, ret
            proc.wait()
            if ret != '0':
                retcode = ret.split(':')
                retcode=retcode[0]	
                break
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_group_create
#   Variable: clustergroupname, clustergroupnodes(non-essential)
#   Purpose: create a new group with clustergroupname
#   Data structure: type: str or int;
#
#########################################################################################################

def func_group_create(clustergroupname,clustergroupnodes=[]):
    try:
        cmd = "sudo python %s group add %s %s" % (settings.digimanager,clustergroupname,' '.join(clustergroupnodes))
        proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
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
#   Function: func_group_delete
#   Variable: clustergroupname
#   Purpose: delete a group with clustergroupname
#   Data structure: type: str or int;
#
#########################################################################################################

def func_group_delete(clustergroupname):
    try:
        cmd = "sudo python %s group del %s" % (settings.digimanager,clustergroupname)
        proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
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
