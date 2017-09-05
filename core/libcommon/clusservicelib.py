#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import subprocess
import re
import copy
import pickle
import simplejson
from decimal import *
from logger import logger
from logger import Ologger
from libcommon import utils
from findir import myFile

currpath = os.path.join(os.getcwd(),os.path.dirname(__file__))
if not currpath in sys.path:
    sys.path.append(currpath)
homepath = currpath[:currpath.find('libcommon')]
if not homepath in sys.path:
    sys.path.append(homepath)
import settings
from base import _
#########################################################################################################
#
#   Function: func_service_create
#   Variable: clusterservicename, clusterserviceraidlv, clusterservicedata
#   Purpose: add a new service for the cluster
#   Data structure: type: str or int
#
#########################################################################################################

def func_service_create(clusterservicename, clusterserviceraidlv, clusterservicelocalpor, clusterservicedata, option):
    retcode = 'operation failed'
    try:
        if clusterservicename:
            cmd = "sudo python %s service create %s %s %s %s %s" % (settings.digimanager, clusterservicename, clusterserviceraidlv, clusterservicelocalpor, clusterservicedata, option)
            proc = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            Ologger.info(cmd)
        else:
            cmd = "sudo python %s node add %s" % (settings.digimanager, clusternodeipaddr)
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
            Ologger.info(cmd)
        retcode = proc.stdout.readlines()[0].strip()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        proc.wait()
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_service_list_all
#   Variable: unit(not-essential)
#   Purpose: to list all services info
#   Data structure: type: list
#                   ex: [{'servicename': servicename, 'totalsize': toatlsize, 'usesize': usesize, 'raidlv': raidlv, 'status': status, 'usage': usage, 'abmormal_status': abnormal_status}#                       ,{...},...]
#
#########################################################################################################

def func_service_list_all(unit=''):
    clusterservices = []
    #key = ['servicename','totalsize','usedsize','raidlv','status','usage','abnormal_status']
    try:
        p_status = 'name: (\S+)\s+service total size: (\S+)\s+service used size: (\S*)\s+service raid level: (\S+)\s+service status: (\S+)\s+'
        cmd = "sudo python %s service list" % (settings.digimanager)
        #print >> sys.stderr,cmd
        proc_status = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result_status = proc_status.stdout.readlines()
        proc_status.wait()
        '''retcode_ = result_status[0]
        if retcode_ == '0\n' and len(result_status) > 2:
            result_status.pop(0)
            result = ''.join(result_status).replace('\n','\t')
            retcode_ = result[0]
            result_ = result.split('\t\t')
            for s in result_[:-1]:
                clusterservice = s.split('\t')
                service = dict()
                service['abnormal_status'] = ''
                if len(clusterservice) > 2:
                    for v in clusterservice:
                        value = v.split(': ')
                        if value[0] == 'service name':
                            service['servicename'] = value[1]
                            continue
                        elif value[0] == 'service total size':
                            service['totalsize'] = utils.getUnit(unit, value[1])
                            continue
                        elif value[0] == 'service used size':
                            service['usedsize'] = utils.getUnit(unit, value[1])
                            continue
                        elif value[0] == 'service raid level':
                            if value[1] == '2':
                                service['raidlv'] = 'default'
                            if value[1] == '1':
                                service['raidlv'] = 'afr'
                            if value[1] == '0':
                                service['raidlv'] = 'strip'
                            if value[1] == '10':
                                service['raidlv'] = 'strip'
                            if value[1] == '01':
                                service['raidlv'] = 'afr'
                            continue
                        elif value[0] == 'service export cifs status':
                            service['cifs_status'] = value[1]
                            continue
                        elif value[0] == 'service export nfs status':
                            service['nfs_status'] = value[1]
                            continue
                        elif value[0] == 'service status':
                            service['status'] = value[1]
                            continue
                        else:
                            service['abnormal_status'] += v + '<br />'
                            continue
                if service['status'] == 'start':
                    service['usage'] = round(Decimal(str(service['usedsize']))/Decimal(str(service['totalsize'])), 2)
                elif service['status'] == 'Warnning':
                    service['usage'] = '0'
                else:
                    service['totalsize'] = '0'
                    service['usedsize'] = '0'
                    service['usage'] = '0'
                clusterservices.append(service)
            return clusterservices
        else:
            clusterservices = [{'startword':'Create Service'}]
            return clusterservices'''
        if len(result_status)>1:
            #print >> sys.stderr, result
            
            for i in range(len(result_status)):
                arr=result_status[i].replace('\n','')
                index=arr.split(': ')
                if index[0]=='Volume Name':
                    x=0
                    end=''
                    while end!='Bricks':
                        end=result_status[i+x].replace('\n','')
                        end=end.split(':')
                        end=end[0]
                        #print >> sys.stderr,end
                        x+=1
                    #print >> sys.stderr,x-1
                    service=dict()						
                    service['servicename']=index[1]
                    for j in range(x-1):
                        r=result_status[i+j].replace('\n','')
                        s=r.split(': ')
                        #print >> sys.stderr,s[0]					
                        if s[0]=='Type':		
                            service['raidlv']=s[1]
                            continue
                        elif s[0]=='Replica Number':	
                            service['afr']=s[1]
                            continue
                        elif s[0]=='Volume ID':		
                            service['vid']=s[1]
                            continue
                        elif s[0]=='Status':		
                            service['status']=s[1]
                            continue
                        elif s[0]=='Number of Bricks':		
                            service['disknum']=s[1]
                            continue
                        elif s[0]=='Transport-type':		
                            service['type']=s[1]
                            continue
                        elif s[0]=='Free Size':		
                            service['freesize']=s[1]
                            continue
                        elif s[0]=='Total Size':		
                            service['totalsize']=s[1]
                            continue
                        else:
                            pass
                    try:
                        service['afr']
                    except:    
                        service['afr']='NaN'
                    #service['cifs_status']='start'
                    #service['nfs_status']='stop'
                    if 	service['freesize']=='N/A':
                        service['usage']=0
                        service['freesize']=0.0
                        service['totalsize']=0.0
                        service['usedsize']=0.0
                    else:
                        if float(service['totalsize'])==0:
                            service['usedsize']=0						
                            service['usage']=0
                        else:	
                            service['usedsize']=float(service['totalsize'])-float(service['freesize'])
                            service['usage']=round(Decimal(str(service['usedsize']))/Decimal(str(service['totalsize'])), 2)	
                        service['freesize']=utils.getUnit_2(unit, service['freesize'])
                        service['totalsize']=utils.getUnit_2(unit, service['totalsize'])
                        service['usedsize']=utils.getUnit_2(unit, service['usedsize'])
                    service['client']=len(func_client_node_list_all(service['servicename']))
					
                    #cmd2 = "sudo python %s service afr_info %s" % (settings.digimanager,service['servicename'])
                    #proc2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)
                    #Ologger.info(cmd2)
                    #result2 = proc2.stdout.readlines()
                    #proc2.wait()
                    #print >> sys.stderr,result2[1]
                    service['afr_info']='0'#result2[1].strip()
                    clusterservices.append(service)
        else:
            clusterservices=[]
        print >> sys.stderr,clusterservices
        #clusterservices=[]		
        return clusterservices
    except Exception,e:
        logger.debug(e)
        return clusterservices

#########################################################################################################
#
#   Function: func_service_list_disk
#   Variable: servicename
#   Purpose: to list all disks info in a service
#   Data structure: type: dict
#                   ex: {'mirrorname': mirrorname, 'disks': ['sda','sdb','sdc',...]}
#
#########################################################################################################

def func_service_list_disk(servicename):
    clusterserviceinfo = {}
    cmd = 'sudo python %s service list_disk %s ' % (settings.digimanager, servicename)
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    Ologger.info(cmd)
    result = proc.stdout.readlines()
    proc.wait()
    retcode = result[0]
    clusterserviceinfo['disks'] = []
    servicedata = {}
    servicedata['childs'] = []
    servicedata['iconSkin'] = 'diy03'
    if retcode == '0\n' and len(result[1:]) > 3:
        for s in result[1:3]:
            s = s.strip()
            if len(s.split(': ')) > 1:
                key = s.split(': ')[0]
                value = s.split(': ')[1]
                if key == "service name":
                    servicedata['name'] = value
        for s in result[4:-2]:
            print >> sys.stderr, s
            s = s.strip()
            if len(s.split(': ')) > 1:
                mirrordata = {}
                mirrordata['childs'] = []
                key = s.split()[0]
                value = s.split()[1]
                mirrordata['name'] = value
                mirrordata['iconSkin'] = 'diy01'
                print >> sys.stderr, mirrordata
            elif len(s.split(' <=> ')) > 1:
                for disk in s.split(' <=> '):
                    mirrordata['childs'].append({'name':disk, 'iconSkin':'diy02'})
                    print >> sys.stderr, mirrordata
                servicedata['childs'].append(mirrordata)
            else:
                servicedata['childs'].append({'name':s,'iconSkin':'diy02'})
        return servicedata
    else:
        return {}

#########################################################################################################
#
#   Function: func_service_afr_info
#   Variable: servicename, unit
#   Purpose: provide info of afr service
#   Data structure: type: list or str or int
#
#########################################################################################################

def func_service_afr_info(servicename, path=''):
    retcode = 'operation failed'
    clusterservicemirrorinfo = []
    cmd = 'sudo python %s service afr_info_topage %s ' % (settings.digimanager, servicename)
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    Ologger.info(cmd)
    result = proc.stdout.readlines()
    proc.wait()
    retcode = result[0]
    mirrorname = ''
    #ss = simplejson.loads('\n'.join(result[1:]))
    if retcode == '0\n':
        ss = result[1]#.strip()
        #print >> sys.stderr, type(eval(ss))#.replace('\'', "\"")
        #print >> sys.stderr, simplejson.loads(ss)
        if not ss:
            return retcode == '0' and retcode or _(retcode)
        if not path:
            return eval(ss)
        else:
            t_dict = eval(ss)
            #print >> sys.stderr, getChild(t_dict, path)
            return getChild(t_dict, path)
    else:
        return retcode == '0' and retcode or _(retcode)

def getChild(t_dict, path):
    if path == t_dict['PATH']:
        if 'childs' in t_dict:
            return t_dict['childs']
    else:
        for t in t_dict['childs']:
            #if t['TYPE'] == 'dir':
            if 'childs' in t and t['childs']:
                if len(path.split('/')) >= len(t['PATH'].split('/')):
                    if getChild(t, path):
                        return getChild(t, path)
                    else:
                        continue
                else:
                    continue
        else:
            return None

def func_service_afr_info_search(servicename, path='', expandarray=''):
    retcode = 'operation failed'
    import urllib
    clusterservicemirrorinfo = []
    opendir = []
    try:
        if expandarray:
            for e in expandarray.split('|')[1:-1]:
                if e != '':
                    opendir.append("\'%s\'" % e)
            cmd = 'sudo python %s service afr_info_topage_search %s %s' % (settings.digimanager, servicename, ' '.join(opendir))
        else:
            cmd = 'sudo python %s service afr_info_topage_search %s %s' % (settings.digimanager, servicename, '/cluster2/' + servicename)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        mirrorname = ''
        #ss = simplejson.loads('\n'.join(result[1:]))
        if retcode == '0\n':
            ss = result[1]#.strip()
            if not path:
                if ss:
                    my_dict = eval(ss)
                    return my_dict
                else:
                    return {'name':'Error', 'errmesg':'getdataerror'}
            else:
                t_dict = eval(ss)
                return getChild(t_dict, path)
        else:
            return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_service_afr_syn
#   Variable: service
#   Purpose: touch off synchronizing
#   Data structure: type: str or int
#
#########################################################################################################
def func_service_afr_syn(service):
    retcode = 'operation failed'
    try:
        cmd = 'sudo python %s service afr_syn %s' % (settings.digimanager, service)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_service_extend
#   Variable: clusterservicename, clusterservicedata
#   Purpose: extend the capacity of a service by adding new disks
#   Data structure: type: str or int
#
#########################################################################################################
def func_service_extend(clusterservicename, clusterservicedata):
    retcode = 'operation failed'
    try:
        cmd = 'sudo python %s service add_disk %s %s' % (settings.digimanager, clusterservicename, clusterservicedata)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#�ͻ��˽ڵ��б�
def func_client_node_list_all(service_name):
    clusterclientnodes=[]
    try:
        cmd = 'sudo python %s service client_list %s' % (settings.digimanager, service_name)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        #retcode = result[0]
        if len(result)>1:
            #print >> sys.stderr, result
            for i in result:
                r=i.replace('\n','')
                if r!='0' and r!='':
                    s=r.split('\t')				
                    #print >> sys.stderr, s
                    node=dict()
                    node['service_name']=service_name
                    node['node_name']=s[0]
                    if s[1]=='started':
				        node['status']='1'
                    else:
                        node['status']='0'
                    clusterclientnodes.append(node)
        else:
            clusterclientnodes=[]
        print >> sys.stderr,clusterclientnodes
        #clusterclientnodes=[{'service_name':service_name,'node_name':'10.10.3.132','status':'start'}]		
        #clusterclientnodes=[{'service_name':service_name,'node_name':'192.168.1.1','cifs_status':'start','nfs_status':'start','status':'start'},{'service_name':service_name,'node_name':'192.168.1.2','cifs_status':'stop','nfs_status':'stop','status':'stop'}]	
        #clusterclientnodes=[]
        return clusterclientnodes
    except Exception,e:
        logger.debug(e)
        return clusterclientnodes

#�ͻ��˽ڵ����
def func_client_node_create(service_name, node_name):
    retcode = 'operation failed'
    try:
        cmd = 'sudo python %s service client_add %s' % (settings.digimanager, node_name)
        print >> sys.stderr, cmd
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]	
        #retcode = 0;
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)		

#�ͻ��˽ڵ�ɾ��		
def func_client_node_delete(service_name, node_name):
    retcode = 'operation failed'
    try:
        cmd = 'sudo python %s service client_destroy %s' % (settings.digimanager, node_name)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]	
        #retcode=0			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)			
	
#�ͻ��˽ڵ�cifs
'''
def func_client_node_cifs(op,service_name, node_name):
    retcode = 'operation failed'
    try:
        cmd = 'sudo python %s service add_disk %s %s' % (settings.digimanager, clusterservicename, clusterservicedata)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        retcode = 0;
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)			
	
#�ͻ��˽ڵ�nfs
def func_client_node_nfs(op,service_name, node_name):
    retcode = 'operation failed'
    try:
        cmd = 'sudo python %s service add_disk %s %s' % (settings.digimanager, clusterservicename, clusterservicedata)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        retcode = 0;
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)			
'''

#�ͻ��˽ڵ�״̬
def func_client_node_status(op,service_name, node_name):
    retcode = 'operation failed'
    try:
        cmd = 'sudo python %s service client_%s %s %s' % (settings.digimanager, op, service_name, node_name)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]	
        #retcode = 0;
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)			
		
		
#������̿�
def func_raidlv_detail(service_name):
    bricks=[]
    try:
        cmd = 'sudo python %s service list_disk %s' % (settings.digimanager, service_name)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        
        if len(result)>2:
            #print >> sys.stderr,len(result)
            for i in range(len(result)):
                index=result[i].replace('\n','')
                #print >> sys.stderr,index				
                if index=='------------------------------------------------------------------------------':
                    #print >> sys.stderr,index
                    brick=dict()				
                    for j in range(12):
                        r=result[i+j].replace('\n','')
                        s=r.split(":")
                        if s[0].strip()=='Brick':
                            brick_name=s[1].strip().split(' ')
                            brick['mount_point']=brick_name[1]+':'+s[2].strip()
                            mark=brick['mount_point'].split('/')
                            brick['mark']=mark[2]							
                            continue							
                        elif s[0].strip()=='Online':
                            brick['status']=s[1].strip()
                            continue
                        elif s[0].strip()=='File System':
                            brick['fs']=s[1].strip()
                            continue
                        elif s[0].strip()=='Device':
                            brick['interface']=s[1].strip()
                            continue
                        elif s[0].strip()=='Disk Space Free':
                            brick['free']=s[1].strip()
                            continue
                        elif s[0].strip()=='Total Disk Space':
                            brick['total']=s[1].strip()
                            continue
                        else:
                            pass
					
                    if brick['free']=='NaN' or brick['free']=='0Bytes':
                        brick['usage']='NaN'
                    else:
                        free=re.match('\d+.\d+',brick['free'])
                        free=free.group()
                        free_unit=brick['free'].replace(free,'')
                        free=float(free)
                        if free_unit=='KB':
                            free=free*1024
                        elif free_unit=='MB':
                            free=free*1024*1024
                        elif free_unit=='GB':
                            free=free*1024*1024*1024
                        elif free_unit=='TB':
                            free=free*1024*1024*1024*1024
                        else:
                            pass
					
                        total=re.match('\d+.\d+',brick['total'])
                        total=total.group()
                        total_unit=brick['total'].replace(total,'')
                        total=float(total)
                        if total_unit=='KB':
                            total=total*1024
                        elif total_unit=='MB':
                            total=total*1024*1024
                        elif total_unit=='GB':
                            total=total*1024*1024*1024
                        elif total_unit=='TB':
                            total=total*1024*1024*1024*1024
                        else:
                            pass
									
                        usedsize=total-free
                        #print >> sys.stderr,total
                        #print >> sys.stderr,free
                        #print >> sys.stderr,usedsize
                        brick['usage']=round(Decimal(str(usedsize))/Decimal(str(total)), 2)
                        #brick['usage']=0.32					
                        #print >> sys.stderr,float(brick['free'].replace('GB',''))							
                    bricks.append(brick)
        else:
            bricks=[]
        #bricks=[{'brick_name':'node-1','mount_point':'/digioceanfs/wwn-0x50014ee003001f1f','status':'Y','fs':'ext4','interface':'/dev/mapper/VolGroup00-lv_root','usage':'30%','total':'4.8GB'},{'brick_name':'node-1','mount_point':'/digioceanfs/wwn-0x50014ee05856d31a','status':'Y','fs':'xfs','interface':'/dev/sdc','usage':'20%','total':'465.5GB'}]	
        print >> sys.stderr, bricks 

        return bricks
    except Exception,e:
        logger.debug(e)
        return bricks
		
def func_service_cifs_add_user(clusterservicename, username, password):
    try:
        cmd= 'sudo python %s service cifs_add_user %s %s %s' % (settings.digimanager, clusterservicename, username, password)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)
        
def func_service_cifs_del_user(clusterservicename, username):
    retcode = 'operation failed'
    try:
        cmd= 'sudo python %s service cifs_del_user %s %s' % (settings.digimanager, clusterservicename, username)
        print >> sys.stderr, cmd
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

def func_service_cifs_list_user(clusterservicename):
    retcode = 'operation failed'
    try:
        cmd= 'sudo python %s service cifs_list_user %s' % (settings.digimanager, clusterservicename)
        #print >> sys.stderr, cmd
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
		
        cmd2= 'sudo python %s service cifs_list_links %s' % (settings.digimanager, clusterservicename)
        proc2 = subprocess.Popen(cmd2, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd2)
        result2 = proc2.stdout.readlines()
        proc2.wait()
        retcode2 = result2[0]
        #print >> sys.stderr, result2[1:-1]
		
        user_list = []
        #print >> sys.stderr, result[1:]
        if retcode == '0\n':
            for user in result[1:-1]:
                user_arr=dict()
                user_arr['user']=user.strip()
                linked=0;
                for link in result2[1:-1]:
                    link=link.split('\t')
                    #print >> sys.stderr, link[1]
                    if link[1].strip()==user.strip():
                        linked+=1
                        user_arr['node']=link[0]
                        user_arr['pid']=link[2]
                if linked>0:
                    user_arr['link']='linked'
                else:
                    user_arr['node']=''
                    user_arr['pid']=''
                    user_arr['link']='unlink'				
                user_list.append(user_arr)
            #print >> sys.stderr, user_list
            return user_list
        else:
            return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        
def func_service_nfs_list_user(clusterservicename):
    retcode = 'operation failed'
    try:
        cmd= 'sudo python %s service nfs_list_user %s' % (settings.digimanager, clusterservicename)
        print >> sys.stderr, cmd
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        #print >> sys.stderr,result
        retcode = result[0]
        user_list = []
        #print >> sys.stderr, result[1:]
        if retcode == '0\n':
            user_str=result[1].replace('\n','')
            if user_str != 'None':
                user_list=user_str.replace('None','').split(',')
                print >> sys.stderr, user_list
            return user_list
        else:
            return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)       
        return retcode == '0' and retcode or _(retcode) 
    
def func_service_list_nfs_links(clusterservicename):
    retcode = 'operation failed'
    try:
        cmd= 'sudo python %s service nfs_list_links %s' % (settings.digimanager, clusterservicename)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        links_list = []
        if retcode == '0\n':
            for link in result[1:-1]:
                linkdata = link.split('\t')
                print >> sys.stderr, linkdata
                linkdatadict = {}
                if len(linkdata) == 2:
                    linkdatadict['nodename'] = linkdata[0].strip()
                    linkdatadict['tar_ip'] = linkdata[1].strip()
                else:
                    linkdatadict['fatalerror'] = 'fatalerror'
                print >> sys.stderr, linkdatadict
                links_list.append(linkdatadict)
            return links_list
        else:
            return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)
    
def func_service_del_nfs_links(service_name, node_name, tar_ip):
    retcode = 'operation failed'
    try:
        cmd= 'sudo python %s service nfs_del_links %s %s %s' % (settings.digimanager, service_name, node_name, tar_ip)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        links_list = []
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

def func_service_nfs_add_user(clusterservicename, userip):
    retcode = 'operation failed'
    try:
        cmd= 'sudo python %s service nfs_add_user %s %s' % (settings.digimanager, clusterservicename, userip)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        if retcode == '0\n':
            return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)
        
def func_service_nfs_del_user(clusterservicename, userip):
    retcode = 'operation failed'
    try:
        cmd= 'sudo python %s service nfs_del_user %s %s' % (settings.digimanager, clusterservicename, userip)
        print >> sys.stderr, cmd
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        if retcode == '0\n':
            return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

def func_service_list_cifs_links(clusterservicename):
    retcode = 'operation failed'
    try:
        cmd= 'sudo python %s service cifs_list_links %s' % (settings.digimanager, clusterservicename)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        links_list = []
        if retcode == '0\n':
            for link in result[1:-1]:
                linkdata = link.split('\t')
                linkdatadict = {}
                if len(linkdata) > 2:
                    linkdatadict['nodename']  = linkdata[0]
                    linkdatadict['username']  = linkdata[1]
                    linkdatadict['pid']       = linkdata[2]
                    linkdatadict['linktime'] = linkdata[3]
                elif len(linkdata) == 2:
                    if linkdata[1] == 'nolink':
                        linkdatadict['nodename'] = linkdata[0]
                        linkdatadict['nolink'] = linkdata[1]
                    else:
                        linkdatadict['nodename'] = linkdata[0]
                        linkdatadict['error'] = linkdata[1]
                else:
                    linkdatadict['fatalerror'] = 'fatalerror'
                links_list.append(linkdatadict)
            return links_list
        else:
            return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)
    
def func_service_del_cifs_links(service_name, node_name, pid):
    retcode = 'operation failed'
    try:
        cmd= 'sudo python %s service cifs_del_links %s %s %s' % (settings.digimanager, service_name, node_name, pid)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        links_list = []
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)
            
#########################################################################################################
#
#   Function: func_service_export
#   Variable: clusterservicename, option
#   Purpose: export a serivce using cifs
#   Data structure: type: str or int
#
#########################################################################################################
def func_service_export(option, type, clusterservicename=''):
    if(type == 'cifs'):
        return func_service_cifs_export(option, clusterservicename)
    else:
        return func_service_nfs_export(option, clusterservicename)

def func_service_cifs_export(option, clusterservicename=''):
    retcode = 'operation failed'
    nodes_status = []
    cmd = 'sudo python %s service export_cifs %s %s' % (settings.digimanager, clusterservicename, option)
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    Ologger.info(cmd)
    result = proc.stdout.readlines()
    proc.wait()
    retcode = result[0].strip()
    if retcode == '0' and option == 'status':
        for node_status in result[1:-1]:
            node_status = node_status.split()
            nodes_status.append(': '.join(node_status) + '<br />')
        return nodes_status
    else:
        success=result[1].split(' ')
        success=success[0].split(':')
        success=success[1].strip()
        print >>sys.stderr,success
        if retcode=='0' and success!='0':
            retcode='0'
        else:
            retcode='1'
        return retcode == '0' and retcode or _(retcode)

def func_service_cifs_restart_service(clusterservicename):
    retcode = 'operation failed'
    try:
        cmd = 'sudo python %s service cifs_restart_service %s' % (settings.digimanager, clusterservicename)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)
    
def func_service_cifs_restart_node(clusterservicename):
    retcode = 'operation failed'
    try:
        cmd = 'sudo python %s service cifs_restart_node %s' % (settings.digimanager, clusterservicename)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)        
        return retcode == '0' and retcode or _(retcode)
        
def func_service_nfs_export(option, clusterservicename=''):
    #nodes_status = []
    cmd = 'sudo python %s service export_nfs %s %s' % (settings.digimanager, clusterservicename, option)
    print >> sys.stderr,cmd
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    Ologger.info(cmd)
    result = proc.stdout.readlines()
    proc.wait()
    retcode = result[0]
    if retcode == '0\n' and option == 'status':
        '''for node_status in result[1:-1]:
            node_status = node_status.split()
            nodes_status.append(': '.join(node_status) + '<br />')'''
        nodes_status=result[1].replace('\n','').split(' : ')
        nodes_status=nodes_status[1].lower()
        print >> sys.stderr,nodes_status
        return nodes_status
    else:
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_service_start
#   Variable: clusterservicename
#   Purpose: start a service
#   Data structure: type: str or int
#
#########################################################################################################
def func_service_start(clusterservicename):
    retcode = 'operation failed'
    try:
        cmd = 'sudo python %s service start %s' % (settings.digimanager, clusterservicename)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_service_stop
#   Variable: clusterservicename
#   Purpose: stop a service
#   Data structure: type: str or int
#
#########################################################################################################
def func_service_stop(clusterservicename):
    retcode = 'operation failed'
    try:
        cmd = 'sudo python %s service stop %s' % (settings.digimanager, clusterservicename)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0].strip()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_service_destroy
#   Variable: clusterservicename
#   Purpose: destroy service that needed
#   Data structure: type: str or int
#
#########################################################################################################
def func_service_destroy(clusterservicename):
    retcode = 'operation failed'
    try:
        cmd = 'sudo python %s service destroy %s' % (settings.digimanager, clusterservicename)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0].strip()
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode =='0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

#########################################################################################################
#
#   Function: func_service_abnormal_status
#   Variable: none
#   Purpose: provide info of abnormal service status
#   Data structure: type: str
#
#########################################################################################################
def func_service_abnormal_status():
    abnormal_status = []
    try:
        cmd = 'sudo python %s service list' % settings.digimanager
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        result.pop(0)
        proc.wait()
        for res in result[5:-2]:
            value = res.split('\n')
            abnormal_status.append(value[0])
        return abnormal_status
    except Exception,e:
        logger.debug(e)
        return abnormal_status


#########################################################################################################
#
#   Function: func_service_restart
#   Variable: clusterservicename
#   Purpose: restart abnormal service
#   Data structure: type: str or int
#
#########################################################################################################
def func_service_restart(clusterservicename):
    retcode = 'operation failed'
    try:
        cmd = 'sudo python %s service restart %s' % (settings.digimanager, clusterservicename)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        proc.wait()
        retcode = result[0]
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode =='0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode =='0' and retcode or _(retcode)
