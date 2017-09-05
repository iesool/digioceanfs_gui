#-*- coding: utf-8 -*-

import os
import sys
import Queue
import __builtin__

currpath = os.path.join(os.getcwd(),os.path.dirname(__file__))
confpath = os.path.join(currpath,'conf')
logpath = os.path.join(currpath,'log')
sessionpath = os.path.join(currpath,'sessions')
libcommonpath = os.path.join(currpath,'libcommon')
digimanagerpath = '/usr/local'
abdownloadpath = os.path.join(currpath,'static','download')
redownloadpath = os.path.join('/static','download')

TEMPLATEDIR = os.path.join(currpath,'template')
JSTEMPLATEDIR = os.path.join(currpath,'jstemplate')                 #source
JSTEMPPATH = os.path.join(currpath,'static','js','temp')            #target
NOTIFYDIR = '/etc/digioceanfs_manager/reports/'

#---------------------------------configure product------------------------------
procname = "Storage Management System"
footer = "Cluster Storage Software: v-1.0.0"
#---------------------------------configure database-----------------------------
DATABASE_ENGINE = 'sqllite3'
DATABASE_NAME = 'digioceanfs'
#DATABASE_USER = ''
#DATABASE_PASSWORD = ''
#DATABASE_HOST = ''
#DATABASE_PORT = ''
#---------------------------------global varibles-----------------------------
rqueue=Queue.Queue()
rqlen=500
readlist=list()
unreadlist=list()
err_disks_dir='/etc/digioceanfs_manager/err_disks'

#conn = sqlite3.connect('ipparse.sqlite3')
#cursor = conn.cursor()
conn = None
mode = 'product'
DEBUG = True

#--------------------------------clustergroup-----------------------------------
nodewithoutgroupname = 'none'

#--------------------------------test or product---------------------------------
if mode == 'dev':
    digimanager = os.path.join(digimanagerpath,'digioceanfs_manager','manager','digi_manager.pyc')

elif mode == 'product':
    digimanager = os.path.join(digimanagerpath,'digioceanfs_manager','manager','digi_manager.pyc')
