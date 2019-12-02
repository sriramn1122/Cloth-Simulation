# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 13:54:16 2019

@author: ramsr
"""

import pychrono as chrono
import pychrono.fea as fea
import pychrono.mkl as mkl
#import pychrono.irrlicht as chronoirr
import numpy as np

class ssense_spring:
  # Only using class variables  
  k_1 = 346.6
  k_2 = 6862
  k_3 = 58220
  
def ramp_force(slope, t): #input force to the system
  return slope*t


def force_switch(F):
  if isinstance(F,float):
    if F < load_surface('thm'):
      return F
    else:
      return 0 
  else:
    for i in range(len(F)):
      if F[i] > load_surface('thm'):
        F[i] = 0
    return F
#def force_switch(F):
#    if F < load_surface('thm'):
#      return F
#    else:
#      return 0  


def load_surface(arg_1):
  
#  Material Index
#  thm - Thermal Black
#  gra - Graphite M55J
#  cfs - Carbon Fibre Sandwich Panel
#  kap - Reinforced Kapton
#  rkm - Reinforced Kapton MLI Film
#  wbc - White Beta Cloth
#  ccr - Copper Clad Rodgers
  
  surf = {'thm': 7.9E3, 'gra': 23.3E3, 'cfs': 18.3E3, 'kap': 6.7E3, 'rkm': \
          15E3 , 'wbc': 10E3, 'ccr': 11.7E3}
  for keys in surf:
    	surf.setdefault(keys,None)
  surf_stress = surf[arg_1]
  surf_area = 0.05 * 0.05
  return surf_stress * surf_area


chrono.SetChronoDataPath("C:/Users/ramsr/Anaconda3/Library/data")

my_system = chrono.ChSystemNSC()

my_mesh = fea.ChMesh();

#%% Set Beam  Properties 

msection = fea.ChBeamSectionAdvanced()

#beam_wy = 0.01
#beam_wz = 0.01
rad = 0.005
msection.SetAsCircularSection(rad)
#msection.SetAsRectangularSection(beam_wy, beam_wz)
msection.SetYoungModulus(2.5e5)
msection.SetGwithPoissonRatio(0.071)
#msection.SetGshearModulus(41e8)

msection.SetBeamRaleyghDamping(0.000)

beam_L = 0.5

#%% Create all nodes

nod = {}
num_ver = 5
num_hor = 5
num_out = 5

for i in range(0,num_ver):
  for j in range(0,num_hor):
      for k in range(0,num_out):
          nod["sys_nodex{}y{}z{}".format(i,j,k)] = fea.ChNodeFEAxyzrot(chrono.ChFrameD(chrono.ChVectorD(i * beam_L, j * beam_L, k*beam_L)))
          my_mesh.AddNode(nod["sys_nodex{}y{}z{}".format(i,j,k)])

#%% Create all beam elements 
  
bm = {}
bmc = 0

for k in range(0, num_out):
    
    for i in range(0, num_ver):
        for j in range(0, num_hor-1):
            bm["belement{}".format(bmc)] = fea.ChElementBeamEuler()
            bm["belement{}".format(bmc)].SetNodes(nod["sys_nodex{}y{}z{}".format(i,j,k)],
              nod["sys_nodex{}y{}z{}".format(i,j+1,k)])
            bm["belement{}".format(bmc)].SetSection(msection)
            my_mesh.AddElement(bm["belement{}".format(bmc)])
            bmc = bmc+1

    bmc = bmc+1

    for i in range(0, num_hor-1):
        for j in range(0, num_ver):
            bm["belement{}".format(bmc)] = fea.ChElementBeamEuler()
            bm["belement{}".format(bmc)].SetNodes(nod["sys_nodex{}y{}z{}".format(i,j,k)],
              nod["sys_nodex{}y{}z{}".format(i+1,j,k)])
            bm["belement{}".format(bmc)].SetSection(msection)
            my_mesh.AddElement(bm["belement{}".format(bmc)])
            bmc = bmc+1 
        

for i in range(0, num_ver):
    for j in range(0, num_hor):
        for k in range(0, num_out-1):
            bm["belement{}".format(bmc)] = fea.ChElementBeamEuler()
            bm["belement{}".format(bmc)].SetNodes(nod["sys_nodex{}y{}z{}".format(i,j,k)],
              nod["sys_nodex{}y{}z{}".format(i,j,k+1)])
            bm["belement{}".format(bmc)].SetSection(msection)
            my_mesh.AddElement(bm["belement{}".format(bmc)])
            bmc = bmc+1
            
  
#%% Creating Sphere element to test out elasticity
            
sphere_material = chrono.ChMaterialSurfaceNSC()
sphere_material.SetFriction(0.2)
sphere_material.SetDampingF(0.1)
sphere_material.SetCompliance (0.0000001)
sphere_material.SetComplianceT(0.0000001)


radius_sphere = 5
density_sphere = 1000
mass_sphere = density_sphere * (4/3) * np.pi * (radius_sphere**3)
inertia_sphere = (2/5) * mass_sphere * (radius_sphere**2)


body_sphere = chrono.ChBody()
body_sphere.SetPos(chrono.ChVectorD(10, 3, 2 ))
body_sphere.SetMass(mass_sphere)
body_sphere.SetInertiaXX(chrono.ChVectorD(inertia_sphere,inertia_sphere,inertia_sphere))
body_sphere.SetMaterialSurface(sphere_material)


body_sphere.GetCollisionModel().ClearModel() 
body_sphere.GetCollisionModel().AddBox(radius_sphere/2, radius_sphere/2, radius_sphere/2) # must set half sizes
body_sphere.GetCollisionModel().BuildModel()
body_sphere.SetCollide(True)


body_sphere_shape = chrono.ChSphereShape()
body_sphere_shape.GetSphereGeometry().rad = radius_sphere
body_sphere_texture = chrono.ChTexture()
body_sphere_texture.SetTextureFilename(chrono.GetChronoDataPath() + 'rock.jpg')
body_sphere.GetAssets().push_back(body_sphere_texture)
body_sphere.GetAssets().push_back(body_sphere_shape)


my_system.Add(body_sphere)

#%% Set forces and constraints 

mtruss = chrono.ChBody()
mtruss.SetBodyFixed(True)
my_system.Add(mtruss)

chrono.ChCollisionModel.SetDefaultSuggestedEnvelope(0.001)
chrono.ChCollisionModel.SetDefaultSuggestedMargin(0.001)


my_system.Set_G_acc(chrono.ChVectorD(0,-9.8,0))


#hnode3.SetTorque(chrono.ChVectorD(0, -0.04, 0))

#hnode1.SetFixed(True)


#constr_fixed = chrono.ChLinkMateGeneric()
constr_flexi = chrono.ChLinkMateGeneric()

#nod["sys_nodex{}y{}".format(0,0)].SetFixed(True)
#nod["sys_nodex{}y{}".format(0,4)].SetFixed(True)
#nod["sys_nodex{}y{}".format(4,0)].SetFixed(True)
#nod["sys_nodex{}y{}".format(4,4)].SetFixed(True)

#nod["sys_nodex{}y{}".format(2,2)].SetPos(chrono.ChVectorD(0,0,1))

#for i in range(0, num_hor):
##  nod["sys_nodex{}y{}".format(num_ver-1,i)].SetForce(chrono.ChVectorD(0.05, 0, 0))
#  nod["sys_nodex{}y{}".format(0,i)].SetFixed(True)
#  constr_fixed.Initialize(nod["sys_node{}{}".format(0,i)], mtruss, False, 
#                          nod["sys_node{}{}".format(0,i)].Frame(), nod["sys_node{}{}".format(0,i)].Frame())


#constr_fixed.SetConstrainedCoords(True, True, True,   # x, y, z
#                               True, True, True)   # Rx, Ry, Rz
#my_system.Add(constr_fixed)

nod["sys_nodex{}y{}z{}".format(0,0,0)].SetFixed(True)
nod["sys_nodex{}y{}z{}".format(0,0,4)].SetFixed(True)
nod["sys_nodex{}y{}z{}".format(0,4,0)].SetFixed(True)
nod["sys_nodex{}y{}z{}".format(4,0,0)].SetFixed(True)


nod["sys_nodex{}y{}z{}".format(4,4,4)].SetFixed(True)
nod["sys_nodex{}y{}z{}".format(4,4,0)].SetFixed(True)
nod["sys_nodex{}y{}z{}".format(4,0,4)].SetFixed(True)
nod["sys_nodex{}y{}z{}".format(4,0,0)].SetFixed(True)



for i in range(0,num_ver):
  for j in range(0, num_hor):
      for k in range(0, num_out):
          constr_flexi.Initialize(nod["sys_nodex{}y{}z{}".format(i,j,k)], mtruss, True,
                                      nod["sys_nodex{}y{}z{}".format(i,j,k)].Frame(),
                                      nod["sys_nodex{}y{}z{}".format(i,j,k)].Frame())
  
constr_flexi.SetConstrainedCoords(False, False, False,
                                  False, False, False)

my_system.Add(constr_flexi)

my_mesh.SetAutomaticGravity(False);

#%% Final Setup of system and attachment of visualization assets

my_system.Add(my_mesh)

mvisualizebeamA = fea.ChVisualizationFEAmesh(my_mesh)
mvisualizebeamA.SetFEMdataType(fea.ChVisualizationFEAmesh.E_PLOT_ELEM_BEAM_TX)
mvisualizebeamA.SetColorscaleMinMax(-0.4, 0.4)
mvisualizebeamA.SetSmoothFaces(True)
mvisualizebeamA.SetWireframe(False)
my_mesh.AddAsset(mvisualizebeamA)


mvisualizebeamC = fea.ChVisualizationFEAmesh(my_mesh)
mvisualizebeamC.SetFEMglyphType(fea.ChVisualizationFEAmesh.E_GLYPH_NODE_CSYS)
mvisualizebeamC.SetFEMdataType(fea.ChVisualizationFEAmesh.E_PLOT_NONE)
mvisualizebeamC.SetSymbolsThickness(0.006)
mvisualizebeamC.SetSymbolsScale(0.01)
mvisualizebeamC.SetZbufferHide(False)
my_mesh.AddAsset(mvisualizebeamC)


msolver = mkl.ChSolverMKLcsm()
my_system.SetSolver(msolver)


my_system.SetSolverType(chrono.ChSolver.Type_MINRES)
my_system.SetSolverWarmStarting(True)
my_system.SetMaxItersSolverSpeed(20)
my_system.SetMaxItersSolverStab(20)
my_system.SetTolForce(1e-5)
my_system.SetTimestepperType(chrono.ChTimestepper.Type_EULER_IMPLICIT_LINEARIZED)



