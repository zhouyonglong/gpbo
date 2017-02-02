import gpbo
import numpy as np
import scipy as sp
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--offset', dest='offset', action='store', default=0,type=int)

args = parser.parse_args()
#mode='run'
mode=['run','plot'][1]
vers=[2,3][0]
D=2
nreps=1
s=1e-6
lb = sp.array([-1.,-1.])
ub = sp.array([1.,1.])

from objective import f

from objective import truemin
all2confs=[]
all3confs=[]
rpath='results4'


#pesbs----------------------------
C=gpbo.core.config.pesbsdefault(f,D,50,s,rpath,'null.csv')
C.stoppara = {'tmax': 60 * 60 * 3}
C.stopfn = gpbo.core.optimize.totaltstopfn
C.aqpara['overhead']='last'
C.aqpara['nrandinit']=20
C.reccfn=gpbo.core.reccomenders.gphinasargminrecc

all2confs.append(['pesbs_argmin',C])
#----------------------#pesbs
C=gpbo.core.config.pesbsdefault(f,D,50,s,rpath,'null.csv')
C.stoppara = {'tmax': 60 * 60 * 3}
C.stopfn = gpbo.core.optimize.totaltstopfn
C.aqpara['overhead']='last'
C.aqpara['nrandinit']=20


all2confs.append(['pesbs_predmin',C])

if mode=='run':
    if vers==2:
        gpbo.runexp(f,lb,ub,rpath,nreps,all2confs,indexoffset=args.offset*nreps)
    else:
        gpbo.runexp(f,lb,ub,rpath,nreps,all3confsindexoffset=args.offset*nreps)
elif mode=='plot':
    gpbo.plotall(all2confs+all3confs,4,rpath,trueopt=truemin)
else:
    pass
import tensorflow as tf
tf.select