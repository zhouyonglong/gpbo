import gpbo
import numpy as np
import scipy as sp

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--offset', dest='offset', action='store', default=0,type=int)

args = parser.parse_args()


mode=['run','plot'][1]
#mode='plot'
vers=[2,3][0]

nreps=4
D=2

s=1e-5
lb = sp.array([-1.,-1.])
ub = sp.array([1.,1.])

from objective import f

#from objective import truemin
all2confs=[]
all3confs=[]
rpath='results0'

#-----------------------
#eimle
C=gpbo.core.config.eimledefault(f,D,12,s,rpath,'null.csv')
C.aqpara['nrandinit']=C.reccpara['onlyafter']=10
C.stoppara = {'tmax': 60*60*10}
C.stopfn = gpbo.core.optimize.totaltstopfn

all2confs.append(['eimle',C])

#pesfs
C=gpbo.core.config.pesfsdefault(f,D,12,s,rpath,'null.csv')
C.aqpara['nrandinit']=C.reccpara['onlyafter']=10
C.stoppara = {'tmax': 60*60*10}
C.stopfn = gpbo.core.optimize.totaltstopfn

all2confs.append(['pesfs',C])

#pesbs----------------------------
C=gpbo.core.config.pesbsdefault(f,D,50,s,rpath,'null.csv')
C.stoppara = {'tmax': 60 * 60 * 10}
C.stopfn = gpbo.core.optimize.totaltstopfn
C.aqpara['overhead']='predict'
C.aqpara['nrandinit']=C.reccpara['onlyafter']=20

all2confs.append(['pesbs',C])


#-----------------
#mtbo
C={'lowtask':4,
   'ninit':15,
   'nsteps':40}

#all3confs.append(['mtbo4',C])

#-----------------
#mtbo
C={'lowtask':16,
   'ninit':15,
   'nsteps':40}

#all3confs.append(['mtbo16',C])

#-----------------
#mtbo
C={'lowtask':64,
   'ninit':15,
   'nsteps':80}

#all3confs.append(['mtbo64',C])
#---------------
#fabolas
C={'ninit':20,
   'nsteps':60}
#all3confs.append(['fabolas',C])



if mode=='run':
    if vers==2:
        gpbo.runexp(f,lb,ub,rpath,nreps,all2confs,indexoffset=args.offset*nreps)
    else:
        gpbo.runexp(f,lb,ub,rpath,nreps,all3confs,indexoffset=args.offset*nreps)
elif mode=='plot':
    gpbo.plotall(all2confs+all3confs,1,rpath)
else:
    pass