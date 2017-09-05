import os
import sys
import py_compile
import subprocess

args = sys.argv[1]

os.chdir(args)


p = subprocess.Popen('find -name "*.py"', stdout=subprocess.PIPE, shell=True)
p.wait()
flist = p.stdout.readlines()

for f in flist:
    if f.strip().find('app.py') < 0 and f.strip().find('mkpyc.py') < 0:
        print 'compile %s' % f.strip()
        py_compile.compile(f.strip())
        os.system('rm %s' % f.strip())
else:
    os.system('rm ./mkpyc.py')
        
