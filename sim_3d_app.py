# -*- coding: utf-8 -*-
"""
Created on Thu Aug 29 09:38:48 2019

@author: ramsr
"""

from sim_3d import *
import pychrono as chrono
#import pychrono.mkl as mkl
import pychrono.irrlicht as chronoirr
#import numpy as np
import time
from datetime import datetime
#import os

#%% Visualization Setup

dat_tim = str(datetime.now())[0:19]

#os.mkdir('Sim_out_dir'+"_"+ dat_tim[0:10] + "_" + dat_tim[11:13] +
#         "-" + dat_tim[14:16] + "-" + dat_tim[17:19])

chrono.SetChronoDataPath("C:/Users/ramsr/Anaconda3/Library/data/")

myapplication = chronoirr.ChIrrApp(my_system, 'Test FEA beams', chronoirr.dimension2du(640,480))

#application.AddTypicalLogo()
myapplication.AddTypicalSky(chrono.GetChronoDataPath() + 'skybox/')
#myapplication.AddTypicalLogo(chrono.GetChronoDataPath() + 'logo_pychrono_alpha.png')
myapplication.AddTypicalCamera(chronoirr.vector3df(5,-2,3))
myapplication.AddTypicalLights()
#myapplication.SetShowInfos(True)
#myapplication.SetShowProfiler(True)
#myapplication.SetShowExplorer(True)


myapplication.AssetBindAll()

myapplication.AssetUpdateAll()

my_system.SetupInitial()

#msolver = mkl.ChSolverMKLcsm()
#my_system.SetSolver(msolver)


my_system.SetSolverType(chrono.ChSolver.Type_MINRES)
my_system.SetSolverWarmStarting(True)
my_system.SetMaxItersSolverSpeed(200)
my_system.SetMaxItersSolverStab(200)
my_system.SetTolForce(1e-9)
my_system.SetTimestepperType(chrono.ChTimestepper.Type_EULER_IMPLICIT_LINEARIZED)

t_step = 1
myapplication.SetTimestep(t_step);
timer = chrono.ChRealtimeStepTimer()
t_end = 300.00

#%% Data Collection Setup

l = list(nod.values())
sim_count = 0
state_pos= []
state_vel = []
state_force = []



# To log output into text files for reference purposes

#file_pos = open('Position_Output'+ 
#                "_"+ dat_tim[0:10] + "_" + dat_tim[11:13] +
#                "-" + dat_tim[14:16] + "-" + dat_tim[17:19] +
#                ".txt", "w+")
#
#file_rate = open('Rate_output'+ 
#                 "_"+ dat_tim[0:10] + "_" + dat_tim[11:13] +
#                "-" + dat_tim[14:16] + "-" + dat_tim[17:19] +
#                ".txt", "w+")
#
#file_force = open('Force_output'+ 
#                 "_"+ dat_tim[0:10] + "_" + dat_tim[11:13] +
#                "-" + dat_tim[14:16] + "-" + dat_tim[17:19] +
#                ".txt", "w+")



#%% Call and run Sim

myapplication.SetTimestep(1)
myapplication.SetTryRealtime(True)


while(myapplication.GetDevice().run()):
    myapplication.BeginScene()
    myapplication.DrawAll()
    for substep in range(0,5):
        myapplication.DoStep()
    myapplication.EndScene()

#while(myapplication.GetDevice().run()):
#  time = myapplication.GetSystem().GetChTime()
##  print(time)
#  if (time >= t_end):
#    break
#  
#  myapplication.BeginScene()
#  myapplication.DrawAll()
#  
##  node_force = 0.1309
##  
##  for i in range(0, num_hor):
##    nod["sys_nodex{}y{}".format(num_ver-1,i)].SetForce(chrono.ChVectorD(node_force, 0, 0))  
#  
#  myapplication.DoStep()
#  
#  for i in range(len(l)):
#    state_pos.append(l[i].GetPos())
#    state_vel.append(l[i].GetPos_dt())
#    state_force.append(l[i].GetForce())
##    file_pos.write("%s " % l[i].GetPos())
##    file_rate.write("%s " % l[i].GetPos_dt())
##    file_force.write("%s " % l[i].GetForce())
##  file_pos.write('\n')  
###  file_rate.write('\n')
#  myapplication.EndScene()
##  myapplication.SetVideoframeSave(True)
#    
##file_pos.close()
##file_rate.close()
##file_force.close()
##
