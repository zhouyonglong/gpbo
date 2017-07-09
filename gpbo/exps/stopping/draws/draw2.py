import gpbo
from gpbo.core import objectives
import numpy as np
import scipy as sp
#mode='run'

#gpbo.core.debugoutput['adaptive']=True
#gpbo.core.debugoutput['logstate']=True
mode=['run','plot'][1]
nreps=2
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--offset', dest='offset', action='store', default=0,type=int)

args = parser.parse_args()

vers=[2,3][0]
D=2

s=0.
lb = sp.array([-1.]*D)
ub = sp.array([1.]*D)
def nullfn(*args,**kwargs):
    print('exitnullfn')
    raise NotImplementedError


f, xm, truemin = objectives.genmat52ojf(D,lb,ub,ls=0.25,fixs=-1)
all2confs=[]
all3confs=[]
rpath='tmp2'
#-----------------------
C=gpbo.core.config.switchdefault(f,D,10,160,s,rpath,'null.csv')
C.chooser=gpbo.core.choosers.always0
all2confs.append(['switching_no',C])

#-----------------------
C=gpbo.core.config.switchdefault(f,D,10,160,s,rpath,'null.csv')
C.choosepara['regretswitch']=1e-2
#C.aqfn = [nullfn]*2
#C.stopfn=gpbo.core.nstopfn
#C.stoppara['n']=32
#out = gpbo.search(C,initdata='dbout/31.p')
all2confs.append(['switching_2',C])


#-----------------------
C=gpbo.core.config.switchdefault(f,D,10,160,s,rpath,'null.csv')
C.choosepara['regretswitch']=1e-4
all2confs.append(['switching_4',C])

#-----------------------
C=gpbo.core.config.switchdefault(f,D,10,160,s,rpath,'null.csv')
C.choosepara['regretswitch']=1e-6
all2confs.append(['switching_6',C])


if mode=='run':
    if vers==2:
        gpbo.runexp(f,lb,ub,rpath,nreps,all2confs,indexoffset=args.offset*nreps)
    else:
        gpbo.runexp(f,lb,ub,rpath,nreps,all3confs,indexoffset=args.offset*nreps)
elif mode=='plot':
    gpbo.plotall(all2confs+all3confs,10,rpath,trueopt=truemin+1e-99,logx=False,showends=True)
else:
    pass
