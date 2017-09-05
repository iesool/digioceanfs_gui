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

def func_getMsg(flag='new'):
    filelist = os.listdir(settings.NOTIFYDIR)
    new = list()
    old = list()
    for f in filelist:
        #print >> sys.stderr,f.find('<UNKNOWN>')
        if f.find('<UNKNOWN>') < 0:
            if f.find('-r') > 0:
                old.append(f)
            else:
                new.append(f)
    if flag == 'new':
        return new
    elif flag == 'old':
        return old
    else:
        return new + old
    
def func_getMsgContent(filelist):
    flist = []
    if not filelist:
        return [{'nofile':True}]
    else:
        for f in filelist:
            filepath = os.path.join(settings.NOTIFYDIR, f)
            try:
                fd = open(filepath, 'r')
                filecontent = fd.read()
                fd.close()
            except:
                filecontent = 'Notify missing'
                fd.close()
            try:
                filectime = simplejson.loads(filecontent)['CTime']
                #filectime = os.stat(filepath).st_ctime
            except:
                filectime = -1
            if filepath.find('-r') > 0:
                isread = 'Y'
            else:
                isread = 'N'
            fdict = {
                     'filepath': filepath,
                     'filecontent': filecontent,
                     'filectime': filectime,
                     'isread': isread
                     }
            flist.append(fdict)
    #ss = sorted(flist, key=lambda flist: flist['filectime'])
    while len(flist) > settings.rqlen:
        rfile = flist.pop(0)
        os.system('rm -rf %s' % rfile['filepath'])
    return flist

def func_tagFile(filepath, reverse=False):
    if reverse:
        pass
    else:
        if os.path.exists(filepath):
            os.system("sudo mv %s %s" % (filepath, filepath+'-r'))
            
def func_delTagFile(filepath):
    if os.path.exists(filepath):
        os.system("sudo rm %s" % (filepath))