#!/usr/bin/env python
#-*- coding: utf-8 -*-

import logging
import logging.config
import os, sys
import ConfigParser

class AppLogger:
    """
        Application log
    """
    working_dir = os.path.dirname(__file__).replace('libcommon','')
    __log_single = None
    __log_ini_file_temp = os.path.join(working_dir,'conf/log/log_config_temp.conf')
    __log_ini_file = os.path.join(working_dir,'conf/log/log_config.conf')
    filecontent = open(__log_ini_file_temp,'rb')
    config = ConfigParser.ConfigParser()
    config.readfp(filecontent)
    filecontent.close()
    config.set("handler_file","args",(os.path.join(working_dir,'log/app.log'),'d',1,'%Y-%m-%d'))
    configContent = open(__log_ini_file,'wb')
    config.write(configContent)
    configContent.close()
    def __init__(self):
        if not AppLogger.__log_single:
            try:
                logging.config.fileConfig(AppLogger.__log_ini_file)
            except:
                pass
            AppLogger.__log_single = logging.getLogger(None)
            
    def getHandler(self):
        return AppLogger.__log_single
        
logger = AppLogger().getHandler()

class OptionLogger:
    """
        Opration log
    """
    working_dir = os.path.dirname(__file__).replace('libcommon','')
    __log_single = None
    __log_ini_file_temp = os.path.join(working_dir,'conf/log/opration_log_config_temp.conf')
    __log_ini_file = os.path.join(working_dir,'conf/log/opration_log_config.conf')
    filecontent = open(__log_ini_file_temp,'rb')
    config = ConfigParser.ConfigParser()
    config.readfp(filecontent)
    filecontent.close()
    config.set("handler_file","args",(os.path.join(working_dir,'log/opration.log'),'d',1,'%Y-%m-%d'))
    configContent = open(__log_ini_file,'wb')
    config.write(configContent)
    configContent.close()
    def __init__(self):
        if not OptionLogger.__log_single:
            try:
                logging.config.fileConfig(OptionLogger.__log_ini_file)
            except:
                pass
            OptionLogger.__log_single = logging.getLogger(None)
            
    def getHandler(self):
        return OptionLogger.__log_single

Ologger = OptionLogger().getHandler()

