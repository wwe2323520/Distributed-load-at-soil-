# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 19:39:36 2024

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

model('basic', '-ndm', 2, '-ndf' , 3)

soilLength = 0.125
rho = 2000 #kg/m^3
Vp = 374.166 #m/s
Vs = 200 #m/s

ny = 1
yMesh = soilLength/ny # Y row MeshSize
dcell = yMesh / Vs 
dt = dcell/10.0
print(f'yMesh = {yMesh}; dt = {dt}')

# ======= Totla Analysis Time ============================
analysisTime = (soilLength/Vs)*8
analystep = analysisTime/dt # int(800*(ny/10))
print(f"dt = {dt}; Analysis Total Time = {analysisTime} ;Analysis_step = {analystep}")

# ============= Bottom Beam element Dashpot ==========================
BotTDash_Start = 1
BotNDash_Start = BotTDash_Start + 2*(1+1)
print(f'BotTDash_Start= {BotTDash_Start}; BotNDash_Start={BotNDash_Start}')


for l in range(2):
    # ------------- traction dashpot -> for S wave------------
    node(BotTDash_Start+2*l, 0.125*l, 0.0)
    node((BotTDash_Start+1)+2*l, 0.125*l, 0.0)
    # =============== dashpot dir: Vs -> x dir ---------------------     
    fix(BotTDash_Start+2*l, 0, 1, 1)      # x dir dashpot　
    fix((BotTDash_Start+1)+2*l, 1, 1, 1)      # fixed end to let soil fix

    # ------------- Normal dashpot -> for P wave ------------
    node(BotNDash_Start+2*l, 0.125*l, 0.0)
    node((BotNDash_Start+1)+2*l, 0.125*l, 0.0)
    # ---------- dashpot dir: Vp -> y dir---------------------     
    fix(BotNDash_Start+2*l, 1, 0, 1)      # y dir dashpot　
    fix((BotNDash_Start+1)+2*l, 1, 1, 1)      # fixed end to let soil fix   


# ------------------- ZeroLength to Build dashpot: Material ----------------------------------
# B_Cmp = 1.0*rho*Vp*sizeX      # Bottom Center node dashpot :N (newton)
# B_Cms = 1.0*rho*Vs*sizeX      # Bottom Center node dashpot :N (newton)


sizeX = 0.125  # m 
Dp = 1.0*rho*Vp*sizeX      # lower Left and Right corner node dashpot :N (newton) 0.5
Ds = 1.0*rho*Vs*sizeX      # lower Left and Right corner node dashpot :N (newton) 0.5

uniaxialMaterial('Viscous',4000, Dp, 1)    # P wave: Side node
uniaxialMaterial('Viscous',4001, Ds, 1)    # S wave: Side node

# uniaxialMaterial('Viscous',4002, B_Cmp, 1)    # P wave: Center node
# uniaxialMaterial('Viscous',4003, B_Cms, 1)    # S wave: Center node

#----------- dashpot elements: Vs with x dir / Vp with y-dir------------------
xdir = 1
ydir = 2
# ------ Traction dashpot element: Vs with x dir
BotTEle_Start = 1
BotTEle_End = BotTEle_Start + 1

element('zeroLength',BotTEle_Start,(BotTDash_Start+1),BotTDash_Start, '-mat',4001,'-dir',xdir)  # node 1: Left side    ele1
element('zeroLength',BotTEle_End,(BotTDash_Start+1)+2*1,BotTDash_Start+2*1, '-mat',4001,'-dir',xdir)  # node 1: Left side ele2

# ------ Normal dashpot element: Vp with y dir (98~106)
BotNEle_Start = BotTEle_End+1
BotNEle_End = BotNEle_Start+1

element('zeroLength',BotNEle_Start,(BotNDash_Start+1),BotNDash_Start, '-mat',4000,'-dir',ydir)   #ele3
element('zeroLength',BotNEle_End,(BotNDash_Start+1)+2*1,BotNDash_Start+2*1, '-mat',4000,'-dir',ydir) #ele4


# # =========== TimeSeries Load ==============================
# timeSeries('Path',702, '-filePath', f'One_fs.txt','-dt', dt)

# pattern('Plain',703, 702)
# load(1, 1,0,0)
# load(3, 1,0,0)
# # # ------------- S wave -----------------------------
# # for o in range(1):
# #     eleLoad('-ele', BeamEle_Start+o, '-type','-beamUniform',0,20,0)

# ============ Apply Velocity / Displacement TimeSeries ============================
iSupportNode = [1, 3]
iGMdirection = [1,1] # Control Apply direction
IDloadTag = 400   # load tag
IDgmSeries = 500  # for multipleSupport Excitation

timeSeries('Path',706, '-filePath', f'TimeSeries/Vel_fs.txt','-dt', dt) # Velocity_TimeSeries
timeSeries('Path',705, '-filePath', f'TimeSeries/Disp_fs.txt','-dt', dt) # Displacement_TimeSeries

pattern('MultipleSupport', IDloadTag)
for i in range(len(iSupportNode)):
    groundMotion(IDgmSeries+i, 'Plain', '-vel',706 ,'int', 'Trapezoidal') # 'Trapezoidal'/'Simpson'
    imposedMotion(iSupportNode[i], iGMdirection[i], IDgmSeries+i)
    # print(iSupportNode[i], iGMdirection[i], IDgmSeries+i)

# =============== Recorder =============================
recorder('Node', '-file', f'Velocity/Disp1.out', '-time', '-node',1,'-dof',1,2,'disp')
recorder('Node', '-file', f'Velocity/Disp2.out', '-time', '-node',2,'-dof',1,2,'disp')
recorder('Node', '-file', f'Velocity/Disp3.out', '-time', '-node',3,'-dof',1,2,'disp')
recorder('Node', '-file', f'Velocity/Disp4.out', '-time', '-node',4,'-dof',1,2,'disp')

recorder('Node', '-file', f'Velocity/Vel1.out', '-time', '-node',1,'-dof',1,2,'vel')
recorder('Node', '-file', f'Velocity/Vel2.out', '-time', '-node',2,'-dof',1,2,'vel')
recorder('Node', '-file', f'Velocity/Vel3.out', '-time', '-node',3,'-dof',1,2,'vel')
recorder('Node', '-file', f'Velocity/Vel4.out', '-time', '-node',4,'-dof',1,2,'vel')

recorder('Node', '-file', f'Velocity/accel1.out', '-time', '-node',1,'-dof',1,2,'accel')
recorder('Node', '-file', f'Velocity/accel2.out', '-time', '-node',2,'-dof',1,2,'accel')
recorder('Node', '-file', f'Velocity/accel3.out', '-time', '-node',3,'-dof',1,2,'accel')
recorder('Node', '-file', f'Velocity/accel4.out', '-time', '-node',4,'-dof',1,2,'accel')

# recorder('Element', '-file', f'Stress/ele{BotEle}.out', '-time', '-ele',BotEle, 'material ',1,'stresses')
recorder('Node', '-file', f'Stress/Reac2.out', '-time', '-node',2,'-dof',1,2,3,'reaction') # rayleighForces / reaction
recorder('Node', '-file', f'Stress/Reac4.out', '-time', '-node',4,'-dof',1,2,3,'reaction')

recorder('Node', '-file', f'Stress/Reac6.out', '-time', '-node',6,'-dof',1,2,3,'reaction')
recorder('Node', '-file', f'Stress/Reac8.out', '-time', '-node',8,'-dof',1,2,3,'reaction')
recorder('Element', '-file', f'Stress/ele{BotTEle_Start}.out', '-time', '-ele',BotTEle_Start,  'force')

recorder('Node', '-file', f'Stress/Reac1.out', '-time', '-node',1,'-dof',1,2,3,'reaction')
recorder('Node', '-file', f'Stress/Reac3.out', '-time', '-node',3,'-dof',1,2,3,'reaction')


system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(3200,dt)
# analyze(int(analystep),cpdt)
print("finish analyze:0 ~ 0.8s")

end = time.time()
print(end - start)
