import os
import sys
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_DELETE, IN_CREATE, IN_CLOSE_WRITE, IN_MOVED_FROM, IN_MOVED_TO  
import signal  
import Queue
import settings
import time

WATCH_DIR = "/etc/digioceanfs_manager/reports"

def hand_hub(n=0, e=0):  
    print 'catch a hub SIGINT'  
       
               
class proc_evt(ProcessEvent):  
    def process_IN_CREATE(self, event):  
	file_path = event.path + '/' + event.name
        try:
            fd = open(file_path, 'r')
            #timest = String(time.time())
            #settings.rqueue.put({'timest': timest,'file_content':fd.read(), 'isread':'N'})
            settings.rqueue.put({'timest':time.time(),'file_content':fd.read(), 'isread':'N', 'file_path': file_path})
            fd.close()
            #os.system("sudo mv %s %s"%(file_path, file_path+'-r'))
        except Exception,e:
            fd.close()
            #os.system("sudo mv %s %s"%(file_path, file_path+'-r'))
            print >> sys.stderr, e
        str = event.maskname
	
class notify(object):  
    def __init__(self, local_rootpath):  
        self.wm = WatchManager()  
        mask = IN_CREATE
               
        self.notifier = Notifier(self.wm, proc_evt())  
        self.wm.add_watch(local_rootpath, mask, rec = True)  
               
    def run(self):  
               
        while (True):  
            try:  
                self.notifier.process_events()  
                if self.notifier.check_events():  
                    self.notifier.read_events()   
            except:  
                self.notifier.stop()  
                break  
                   
if __name__ == '__main__':  
    nty = notify(WATCH_DIR)  
    nty.run()  
