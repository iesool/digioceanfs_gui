#coding=utf-8
import os
import re
#MY_PATH = "/home/ballma/ly/work_ly"
MY_PATH = "/root/test"
#MY_PATH = "/home/ballma/ly"
pathList = []
def getDir(path):
    path_info = os.walk(MY_PATH)
    for _dir, _dir_list,_dir_file in path_info:
        f = myFile()
        f.setPath(_dir)
        f.setType("dir")
        f.setStatus("syncing")
        f.setSrc("node-1-10001")
        f.setTarget("node-1-10032")
        pathList.append(f)
        if len(_dir_file) != 0:
            for c_dir_file in _dir_file:
                fc = myFile()
                fc.setPath(_dir)
                fc.setFile(c_dir_file)
                fc.setType("file")
                fc.setStatus("syncing")
                fc.setSrc("node-1-10001")
                fc.setTarget("node-1-10032")
                pathList.append(fc)
    return pathList

class myFile():

    def __init__(self):

        self.PATH = ""
        self.PARENT = None
        self.FILE = ""
        self.CHILD = []
        self.TYPE = ""
        self.STATUS = ""
        self.SRC = ""
        self.TGT = ""
        self.TSIZE = ""
        self.SPEED = ""
    def __cmp__(self,mf):
            return -cmp((self.PATH+self.TYPE), (mf.PATH+mf.TYPE))
    def setPath(self, path):
        self.PATH = path
    def setFile(self, filename):
        self.FILE = filename
    def setParent(self):
        my_f = myFile()
        self.PARENT = my_f
    def setCHILD(self, child):
        if not child in self.CHILD:
            self.CHILD.append(child)
    def setType(self, Type):
        self.TYPE = Type
    def setStatus(self, status):
        self.STATUS = status
    def setSrc(self, src):
        self.SRC = src
    def setTarget(self, target):
        self.TGT = target
    def setTsize(self, targetSize):
        self.TSIZE = targetSize
    def setSpeed(self, speed):
        self.SPEED = speed
    def initParent(self):
        self.setParent()
        p = '\/'
        if self.TYPE == 'file':
            self.PARENT.PATH = self.PATH
            self.PARENT.TYPE = 'dir'
            self.PARENT.fileAttr = (len(re.findall(p, self.PATH)), '/'.join(re.split(p, self.PATH)[:-1]))
        else:
            self.PARENT.PATH = self.fileAttr[1]
            self.PARENT.TYPE = 'dir'
            self.PARENT.fileAttr = (len(re.findall(p, self.PATH)) -1, '/'.join(re.split(p, self.PATH)[:-2]))
    def obj2dict(self):
        objdict = {}
        objdict['PATH'] = self.PATH
        objdict['FILE'] = self.FILE
        objdict['TYPE'] = self.TYPE
        objdict['STATUS'] = self.STATUS
        objdict['SRC'] = self.SRC
        objdict['TGT'] = self.TGT
        objdict['TSIZE'] = self.TSIZE
        objdict['SPEED'] = self.SPEED
        return objdict

if __name__ == "__main__":
    f = file("test.txt.bak", "w")
    for ff in getDir(MY_PATH):
        f.write("PATH=" + ff.PATH + "\n")
        f.write("FILE=" + ff.FILE + "\n")
        f.write("TYPE=" + ff.TYPE + "\n")
        f.write("STATUS=" + ff.STATUS + "\n")
        f.write("SRC=" + ff.SRC + "\n")
        f.write("TGT=" + ff.TGT + "\n")
        f.write("TSIZE=" + str(ff.TSIZE) + "\n")
        f.write("SPEED=" + str(ff.SPEED) + "\n")
        f.write("\n")
