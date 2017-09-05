import os
import sys
import time
import threading
import traceback
import subprocess

def readFromRaidPipe():
    fd_dir = "/usr/local/digioceanfs_gui/libcommon/monitor_pipe"
    if not fdOpenCheck(fd_dir):
        return 'timeout'
    try:
        start_time = time.time()
        pid = os.getpid()
        th = threading.Thread(target=overTimeCheck, args=(start_time, pid,))
        th.start()
        handle = os.open(fd_dir, os.O_RDONLY, 0700)
        fd = os.fdopen(handle, "r", 0)
        key_list = ["node_name", "raid_event", "raid_name", "disk_name","alert_time"]
        while True:
            content = fd.read()
            if content:
                line_list = content.split('\n')
                if line_list:
                    for message in line_list:
                        if message:
                            tmp_list = message.split("RAID:")
                            if len(tmp_list) >= 2:
                                str = tmp_list[1]
                                val_list = str.strip().split()
                                if len(val_list) == 3:
                                    val_list.append('')
                                time_now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                val_list.append(time_now)
                                event_dict = dict(zip(key_list, val_list))
                                return event_dict
    except:
        try:
            fd.close()
        finally:
            return {'overtime': 120}

def readFromProcessPipe():
    fd_dir = "/usr/local/digioceanfs_gui/libcommon/processing"
    if not fdOpenCheck(fd_dir):
        return 'timeout'
    try:
        start_time = time.time()
        pid = os.getpid()
        th = threading.Thread(target=overTimeCheck, args=(start_time, pid,))
        th.start()
        handle = os.open(fd_dir, os.O_RDONLY, 0700)
        fd = os.fdopen(handle, "r", 0)
        content = ''
        while True:
            #content = fd.readline()
            content = fd.read()
            if len(content) != 0:
                break
        return content.split(": ")[1]
                
    except Exception,e:
        try:
            fd.close()
        finally:
            return 'timeout' 

def overTimeCheck(start_time, pid):
    while True:
        time.sleep(0.1)
        if time.time() - start_time > 120:
            os.kill(pid, 2)
            break

def fdOpenCheck(fd_dir):
    #fd_dir = "/usr/local/digioceanfs_gui/libcommon/processing"
    pid_list = []
    cmd = []
    cmd.append('lsof')
    cmd.append(fd_dir)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    proc.wait()
    result = proc.stdout.readlines()
    if result:
        for res in result[1:]:
            process_line = res.split()
            pid_list.append(process_line[1])
        for pid in pid_list:
            try:
                os.kill(int(pid), 9)
            except Exception, e:
                return False
        else:
            return True
    else:
        return True

if __name__ == "__main__":
    #print readFromProcessPipe()
    #print readFromRaidPipe()
    print fdOpenCheck()
