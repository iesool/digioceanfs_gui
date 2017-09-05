import subprocess
import re
import copy

def parseGroup():
    clustergroups = {}
    proc = subprocess.Popen('python digimanage group list',shell=True,stdout=subprocess.PIPE)
    result = proc.stdout.readlines()
    proc.wait()
    retcode = result.pop(0).strip()
    if retcode == '0':
        clustergroup = None
        clustergroupnodes = []
        for line in result:
            m = re.match('^\s+(\S+)\s+$',line)
            if m:
                clustergroupnodes.append(m.group(1))
            else:
                m = re.match('^(\S+)\s+$',line)
                if m:
                    if clustergroup:
                        clustergroups[clustergroup] = clustergroupnodes
                    clustergroup = m.group(1)
                    clustergroupnodes = copy.deepcopy([])
        clustergroups[clustergroup] = clustergroupnodes
    return clustergroups           
