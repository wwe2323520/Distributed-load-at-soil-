# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 19:39:36 2024

@author: User
"""

import matplotlib.pyplot as plt
import time
import os 
import numpy as np
from openseespy.opensees import *


wipe()
# -------- Start calculaate time -----------------
start = time.time()
print("The time used to execute this is given below")

model('basic', '-ndm', 2, '-ndf' , 2)

E = 208000000 # (N/m^2)= (kg*m/s2)*(1/m2) = kg/(s2*m) 
nu = 0.0 #0.3
rho = 2000    # kg/m3 
nDMaterial('ElasticIsotropic', 2000, E, nu, rho)

soilLength = 10 #m
soilwidth =  0.125     #1.0

nx = int(soilwidth/0.125)
ny = 80 #80
e1 = 1
n1 = 1
eleArgs = [1, 'PlaneStrain', 2000]
points = [1, 0.0,   0.0, 
        2, soilwidth,  0.0, 
        3, soilwidth,  soilLength, 
        4, 0.0,   soilLength]
block2D(nx, ny, e1, n1,'quad', *eleArgs, *points)

# # -------- Soil B.C (Tie BC) ---------------
# for i in range(ny+1):
#     equalDOF((nx+1)*i+1,(nx+1)*i+(nx+1),1,2)

endNode = (1+nx) + (nx+1)*ny
endEle = ny
# print(endNode, endEle)

Vp = 374.166    # m/s 
Vs = 200     ;# m/s 

yMesh = soilLength/ny # Y row MeshSize
dcell = yMesh / Vs 
dt = dcell/10.0

# ======= Totla Analysis Time ============================
analysisTime = (soilLength/Vs)*8
analystep = analysisTime/dt # int(800*(ny/10))
print(f"dt = {dt}; Analysis Total Time = {analysisTime} ;Analysis_step = {analystep}")
                  
widthMesh = soilwidth/nx

# ------ Recorde Node/Element ID -----------------------------------------------
BottomEle = e1
CenterEle = e1 + int(ny/2)
TopEle = ny

LBNode =  n1
LCNode =  n1 + (n1+nx)*int(ny/2) 
LTNode =  n1 + (n1+nx)*ny

RBNode = (n1+nx)
RCNode = (n1+nx) + (n1+nx)*int(ny/2) 
RTNode =(n1+nx) + (n1+nx)*ny
print(f"BottomEle ={BottomEle}; CenterEle = {CenterEle}; TopEle = {TopEle}")
print(f"LBNode = {LBNode}; LCNode = {LCNode}; LTNode = {LTNode}")
print(f"RBNode = {RBNode}; RCNode = {RCNode}; RTNode = {RTNode}")

RayBotLEle = endEle+1
RayCenLEle = RayBotLEle + int(ny/2)
RayTopLEle = RayBotLEle + ny-1
print(f"RayBotLEle = {RayBotLEle}; RayCenLEle = {RayCenLEle}; RayTopLEle = {RayTopLEle}")

RayBotREle = RayBotLEle + ny
RayCenREle = RayBotREle + int(ny/2)
RayTopREle = RayBotREle + ny-1
print(f"RayBotREle = {RayBotREle}; RayCenREle = {RayCenREle}; RayTopREle = {RayTopREle}")

RayBBEle = RayTopREle + 1
print(f"RayBBEle = {RayBBEle}")
# ============== Apply virtual Quad element to apply Rayleigh Dashpot =======================
LeftNode = endNode+ 1 
RightNode = LeftNode + ny +1
BotNode = RightNode + ny +1

LeftELe = endEle + 1
RightELe = LeftELe + ny 
BotEle = RightELe + ny 
for i in range(ny+1):
# --------- Left Side ------------------------
    node(LeftNode+i, -0.125, 0.125*i) 
# --------- Right Side ------------------------
    node(RightNode+i, soilwidth+0.125, 0.125*i)

node(BotNode, 0.0, -0.125)
node(BotNode+1, soilwidth, -0.125)

for j in range(ny): #ny
# --------- Left Side ------------------------
    element('quad', LeftELe+j, LeftNode+j, 1+(1+nx)*j, (1+nx+1)+(1+nx)*j, (LeftNode+1)+j ,*eleArgs)
# --------- Right Side ------------------------
    element('quad', RightELe+j, (1+nx)+(1+nx)*j, RightNode+j, (RightNode+1)+j, (1+nx)*2+(1+nx)*j,*eleArgs)

# --------------- Bot Quad element -------------------------------
element('quad', BotEle, BotNode, BotNode+1, (nx+1), 1,*eleArgs)

# =========== Bottom Beam element ===================
BeamNode_Start = BotNode + 2
BeamEle_Start = BotEle + 1

model('basic', '-ndm', 2, '-ndf' , 3)

for j in range(nx+1):
    node(BeamNode_Start+j, widthMesh*j,0.0)
    mass(BeamNode_Start+j,1,1,1)
# -------- fix rotate dof ------------
    fix(BeamNode_Start+j,0,0,1)

# ------------- Beam parameter -----------------
A = 0.1*1
E1 = 1e-06 ;#1e-06
Iz = (0.1*0.1*0.1)/12
geomTransf('Linear', 1)


for k in range(nx):
    element('elasticBeamColumn', BeamEle_Start+k, BeamNode_Start+k, BeamNode_Start+1+k, A,E1,Iz, 1, '-release', 3)

# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(n1+k,BeamNode_Start+k,1,2)

# # ============= Bottom Beam element Dashpot ==========================
# BotTDash_Start = BeamNode_Start + (nx+1)
# BotNDash_Start = BotTDash_Start + 2*(nx+1)
# # print(f'BotTDash_Start= {BotTDash_Start}; BotNDash_Start={BotNDash_Start}')

# for l in range(nx+1):
#     # ------------- traction dashpot -> for S wave------------
#     node(BotTDash_Start+2*l, widthMesh*l, 0.0)
#     node((BotTDash_Start+1)+2*l, widthMesh*l, 0.0)
#     # =============== dashpot dir: Vs -> x dir ---------------------     
#     fix(BotTDash_Start+2*l, 0, 1, 1)      # x dir dashpot　
#     fix((BotTDash_Start+1)+2*l, 1, 1, 1)      # fixed end to let soil fix

#     # ------------- Normal dashpot -> for P wave ------------
#     node(BotNDash_Start+2*l, widthMesh*l, 0.0)
#     node((BotNDash_Start+1)+2*l, widthMesh*l, 0.0)
#     # ---------- dashpot dir: Vp -> y dir---------------------     
#     fix(BotNDash_Start+2*l, 1, 0, 1)      # y dir dashpot　
#     fix((BotNDash_Start+1)+2*l, 1, 1, 1)      # fixed end to let soil fix

# # ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
# for k in range(nx+1):
# # --------------traction dashpot: for S wave------------------
#     equalDOF(1+k,BotTDash_Start+2*k,1)
# # --------------Normal dashpot: for P wave------------------
#     equalDOF(1+k,BotNDash_Start+2*k,2)

# # ------------------- ZeroLength to Build dashpot: Material ----------------------------------
# sizeX = 0.125  # m ******
# B_Smp = 0.5*rho*Vp*sizeX      # lower Left and Right corner node dashpot :N (newton)
# B_Sms = 0.5*rho*Vs*sizeX      # lower Left and Right corner node dashpot :N (newton)

# B_Cmp = 1.0*rho*Vp*sizeX      # Bottom Center node dashpot :N (newton)
# B_Cms = 1.0*rho*Vs*sizeX      # Bottom Center node dashpot :N (newton)

# uniaxialMaterial('Viscous',4000, B_Smp, 1)    # P wave: Side node
# uniaxialMaterial('Viscous',4001, B_Sms, 1)    # S wave: Side node

# uniaxialMaterial('Viscous',4002, B_Cmp, 1)    # P wave: Center node
# uniaxialMaterial('Viscous',4003, B_Cms, 1)    # S wave: Center node

# #----------- dashpot elements: Vs with x dir / Vp with y-dir------------------
# xdir = 1
# ydir = 2
# # ------ Traction dashpot element: Vs with x dir
# BotTEle_Start = BeamEle_Start + nx
# BotTEle_End = BotTEle_Start + nx

# element('zeroLength',BotTEle_Start,(BotTDash_Start+1),BotTDash_Start, '-mat',4001,'-dir',xdir)  # node 1: Left side
# element('zeroLength',BotTEle_Start+1,(BotTDash_Start+1)+2*1,BotTDash_Start+2*1, '-mat',4001,'-dir',xdir)  # node 1: Left side

# # ------ Normal dashpot element: Vp with y dir (98~106)
# BotNEle_Start = BotTEle_End+1
# BotNEle_End = BotNEle_Start+nx

# element('zeroLength',BotNEle_Start,(BotNDash_Start+1),BotNDash_Start, '-mat',4000,'-dir',ydir)
# element('zeroLength',BotNEle_Start+1,(BotNDash_Start+1)+2*1,BotNDash_Start+2*1, '-mat',4000,'-dir',ydir)

# ================== Apply Rayleigh Dashpot =============================
alphaM = (6/yMesh)*(Vp*(1-2*nu) + Vs*(2*nu-2)) #(6/yMesh)*(Vp*(1-2*nu) + Vs*(2*nu-2))
betaK = (-4*yMesh)*((1+nu)*(1-2*nu)/E)*rho*(Vp-Vs) #-0.0008373317307692309
betaKinit = 0.0
betaKcomm = 0.0
print(f"alphaM = {alphaM}; betaK = {betaK}")
region(10000, '-nodeRange',LeftNode, BotNode+1, '-rayleigh',alphaM, betaK, betaKinit,betaKcomm)

# #=========================== Load Pattern 1: Shear wave / P wave ============================
# # timeSeries('Path',702, '-filePath','2fp.txt','-dt',1e-4)
# timeSeries('Path',702, '-filePath', f'TimeSeries/fs200_{ny}row.txt','-dt', dt)
# # timeSeries('Path',704, '-filePath','TopForce10row.txt','-dt',2.67e-4)
# # # # # timeSeries('Linear',705)

# pattern('Plain',703, 702)
# # load(95,0,-1)
# # ------------- P wave -----------------------------
# # for o in range(nx):
# #     eleLoad('-ele', BeamEle_Start+o, '-type','-beamUniform',20,0)

# # ------------- S wave -----------------------------
# for o in range(nx):
#     eleLoad('-ele', BeamEle_Start+o, '-type','-beamUniform',0,20,0)



# ===================== Load Pattern 2: TopForce on the top Middle Point ======================
UpperN_Center = 1 + (1+nx)*ny
tnscp = soilLength/Vp # wave transport time
dcellcp = tnscp/ny #each cell time
cpdt = round(dcellcp/10, 7) #eace cell have 10 steps
print(f"tnscp = {tnscp}; dcellcp= {dcellcp}, cp_dt = {cpdt}")

timeSeries('Path',704, '-filePath',f'TimeSeries/TopForce{ny}row.txt','-dt', cpdt)
pattern('Plain',703, 704)
load(UpperN_Center,0,-1)
load(UpperN_Center-1,0,-1)
print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")


# # # -------------- Recorder --------------------------------
# # ------------- Element Stress -------------
recorder('Element', '-file', f'Stress/ele{BottomEle}.out', '-time', '-ele',BottomEle, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{CenterEle}.out', '-time', '-ele',CenterEle, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{TopEle}.out', '-time', '-ele',TopEle, 'material ',1,'stresses')

# ============ Left Rayleigh Ele ======================
recorder('Element', '-file', f'Stress/ele{RayBotLEle}.out', '-time', '-ele',RayBotLEle, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{RayCenLEle}.out', '-time', '-ele',RayCenLEle, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{RayTopLEle}.out', '-time', '-ele',RayTopLEle, 'material ',1,'stresses')
# ============ Right Rayleigh Ele ======================
recorder('Element', '-file', f'Stress/ele{RayBotREle}.out', '-time', '-ele',RayBotREle, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{RayCenREle}.out', '-time', '-ele',RayCenREle, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{RayTopREle}.out', '-time', '-ele',RayTopREle, 'material ',1,'stresses')
# ============ Bottom Rayleigh Ele ======================
recorder('Element', '-file', f'Stress/ele{RayBBEle}.out', '-time', '-ele',RayBBEle, 'material ',1,'stresses')

# # ------------- Node Velocity -------------
# --------- Left Side -----------------
recorder('Node', '-file', f'Velocity/node{LBNode}.out', '-time', '-node',LBNode,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'Velocity/node{LCNode}.out', '-time', '-node',LCNode,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'Velocity/node{LTNode}.out', '-time', '-node',LTNode,'-dof',1,2,3,'vel')
# --------- Right Side -----------------
recorder('Node', '-file', f'Velocity/node{RBNode}.out', '-time', '-node',RBNode,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'Velocity/node{RCNode}.out', '-time', '-node',RCNode,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'Velocity/node{RTNode}.out', '-time', '-node',RTNode,'-dof',1,2,3,'vel')

system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)

analysis("Transient")
# analyze(int(analystep),dt)
analyze(int(analystep),cpdt)
print("finish analyze:0 ~ 0.8s")

end = time.time()
print(end - start)
