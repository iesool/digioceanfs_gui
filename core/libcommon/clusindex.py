#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import sys
import subprocess
import re
import copy
import utils
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

def func_login(username, passwd):
    try:
        cmd = "sudo python %s login %s %s -w" % (settings.digimanager, username, passwd)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.read().strip()
        print >> sys.stderr, retcode
        proc.wait()
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)
    
def func_logout():
    try:
        cmd = "sudo python %s logout"% (settings.digimanager)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        print >> sys.stderr, cmd
        Ologger.info(cmd)
        retcode = proc.stdout.read().strip()
        print >> sys.stderr, retcode
        proc.wait()
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

def func_manager_check(ipaddr):
    try:
        cmd = "sudo python %s manager_check %s" % (settings.digimanager, ipaddr)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.read().strip()
        proc.wait()
        print >> sys.stderr, retcode
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

def func_manager_set(ipaddr):
    try:
        cmd = "sudo python %s manager_set %s" % (settings.digimanager, ipaddr)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        retcode = proc.stdout.read().strip()
        print >> sys.stderr, retcode
        if retcode!='0':
            retcode=retcode.split(':')
            retcode=retcode[0]			
        proc.wait()
        return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)

def func_manager_get():
    try:
        cmd = "sudo python %s manager_get" % (settings.digimanager)
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        Ologger.info(cmd)
        result = proc.stdout.readlines()
        print >> sys.stderr, result
        retcode = result[0].strip()
        proc.wait()
        if retcode == "0":
            data = result[1].strip()
            print >> sys.stderr, data
            return data 
        else:
            return retcode == '0' and retcode or _(retcode)
    except Exception,e:
        logger.debug(e)
        return retcode == '0' and retcode or _(retcode)
