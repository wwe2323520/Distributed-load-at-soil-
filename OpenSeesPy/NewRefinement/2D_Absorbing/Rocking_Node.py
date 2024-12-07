# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 19:39:36 2023

@author: User
"""
import matplotlib.pyplot as plt
import time
import os 
import numpy as np
from openseespy.opensees import *
import vfo.vfo as vfo
import opstool as opst
import opstool.vis.plotly as opsvis

pi = np.pi
# ----------- Rayleigh Dashpot Cofficient ------------------
# Integrator = "Central"
# ---------- For 1D Transport / 2D Absorbing ------------------
PtimeNum = np.array([702, 704, 705, 706]) # For P wave TimeSeries 702, 704, 705, 706
StimeNum = np.array([707, 708, 709, 710]) # For S wave TimeSeries 707, 708, 709, 710

# # ---------- For 2D Absorbing ------------------
# Top_Ptime = np.array([711, 712, 713, 714]) # For P wave TimeSeries 709, 710, 711
# Top_Stime = np.array([715, 716, 717, 718]) # For S wave TimeSeries 712, 713, 714

Force_HZ = np.array([10, 20, 40, 80]) # 10, 20, 40, 80
Width = np.array([2.0, 5.0, 10.0, 20.0]) # 1D Transport: 2.0, 10.0, 20.0 ; 2D Absorbing: 2.0, 5.0, 10.0, 20.0
Y_MeshNumber= np.array([40]) # 1D Transport: 80, 40, 20, 10 ; 2D Absorbing: 80, 40, 20

Choose_Wave = f"NewMark_Linear/Rocking_N" # Pwave ; Vertical / Horizon / Rocking  
HZ = 80
# for i in range(len(Width)):
#     soilwidth = Width[i]
#     print(f"================ Now SoilWidth = {soilwidth} ================")

#     for j in range(len(Force_HZ)):
#         TimeSeries_Num = int(PtimeNum[j]) # PtimeNum / StimeNum ; Top_Ptime / Top_Stime
#         HZ = int(Force_HZ[j])
#         print(f"--------------------- Force td = 1/f = {HZ} -------------------")

#         for h in range(len(Y_MeshNumber)):
#             ny = int(Y_MeshNumber[h])
#             # print(soilwidth, TimeSeries_Num, HZ, ny)

wipe()
# -------- Start calculaate time -----------------
start = time.time()
print("The time used to execute this is given below")

model('basic', '-ndm', 2, '-ndf' , 2)
Vp = 400  #  => Vp = (E*(1-nu)/((1+nu)*(1-2*nu)*rho))**(0.5) ; 374.166 m/s (nu = 0.3) ; 400 m/s (nu =1/3)
Vs = 200  # m/s 

nu = 1/3
rho = 2000    # kg/m3 
G = rho*Vs*Vs
M = rho*Vp*Vp

E =  2*(1+nu)*G # (N/m^2)

nDMaterial('ElasticIsotropic', 2000, E, nu, rho)

soilLength = 10 #m
soilwidth = 10.0 # 2.0
ny = 40 # 80, 40, 20, 10

yMesh = soilLength/ny # Y row MeshSize
dcell = (yMesh / Vp) 

Dw = soilLength/ny # soilLength/80 , soilLength/ny
nx = int(soilwidth/Dw)# int(soilwidth/0.125)
print(f'x Column = {nx}; xMesh Size = {Dw}')

e1 = 1
n1 = 1
eleArgs = [1, 'PlaneStrain', 2000]
points = [1, 0.0,   0.0, 
        2, soilwidth,  0.0, 
        3, soilwidth,  soilLength, 
        4, 0.0,   soilLength]
block2D(nx, ny, e1, n1,'quad', *eleArgs, *points)

SoilNode_End = (nx+1)+ ny*(nx+1)
SoilEle_End = nx + nx*(ny-1)
print(f"Soil_NodeEnd = {SoilNode_End}; Soil_Ele_End = {SoilEle_End}")

# ---- Calculate dt -------------------
Dt_Size = 0.8 # C = 0.1, 0.4, 0.8, 1.0, 2.0

dt_Mesh = (soilLength/ny)
dt = (dt_Mesh/Vp)*Dt_Size # dcell*Dt_Size
print(f'dt_Mesh = {dt_Mesh}')

print(f"Pwave travel yMesh= {yMesh}; each ele = {dcell} ;dt_Size = {Dt_Size}; dt = {dt}")
# ======= Totla Analysis Time ============================
analysisTime = 0.8 # (soilLength/Vp)*8
analystep = analysisTime/dt # int(800*(ny/10))
print(f"Analysis Total Time = {analysisTime} ;Analysis_step = {analystep}")

# ================= Build Boundary File =====================
Boundary = f"{Choose_Wave}/W_{int(soilwidth)}m/HZ_{HZ}/Tie_Surface_{ny}row" # f"{Choose_Wave}/W_{int(soilwidth)}m/HZ_{HZ}/TieBC_{ny}row"
path1 = f'D:/shiang/opensees/20220330/OpenSeesPy/2D_Absorb/{Boundary}/Velocity' # f'E:/unAnalysisFile/RayleighDashpot/{Boundary}/DepthTest/H{Applt_D}/Ca{akz}_Cb{bkz}/Velocity'
path2 = f'D:/shiang/opensees/20220330/OpenSeesPy/2D_Absorb/{Boundary}/Stress' # f'E:/unAnalysisFile/RayleighDashpot/{Boundary}/DepthTest/H{Applt_D}/Ca{akz}_Cb{bkz}/Stress'
# path3 =  # f'E:/unAnalysisFile/RayleighDashpot/{Boundary}/DepthTest/H{Applt_D}/Ca{akz}_Cb{bkz}/SurfaceVelocity'

if not os.path.isdir(path1):
    os.makedirs(path1)
if not os.path.isdir(path2):
    os.makedirs(path2)
# if not os.path.isdir(path3):
#     os.makedirs(path3)

# ------ Recorde Node/Element ID -----------------------------------------------
LowerN_Left =  1
CenterN_Left = int(LowerN_Left + (nx+1)*(ny/2))
UpperN_Left = int(LowerN_Left + (nx+1)* ny)
print(f"LowerN_Left = {LowerN_Left},CenterN_Left = {CenterN_Left}, UpperN_Left = {UpperN_Left}")
LowerE_Left =  1
CenterE_Left = int(LowerE_Left + nx*(ny/2))
UpperE_Left = int(LowerE_Left + nx* (ny-1))
print(f"LowerE_Left = {LowerE_Left},CenterE_Left = {CenterE_Left}, UpperE_Left = {UpperE_Left}")

LowerN_Center =  int(1 + (nx/2))
CenterN_Center = int(LowerN_Center + (nx+1)*(ny/2))
UpperN_Center = int(LowerN_Center + (nx+1)* ny)
print(f"LowerN_Center = {LowerN_Center},CenterN_Center = {CenterN_Center}, UpperN_Center = {UpperN_Center}")
LowerE_Center =  int((nx/2)+1)
CenterE_Center = int(LowerE_Center + nx*(ny/2))
UpperE_Center = int(LowerE_Center + nx* (ny-1))
print(f"LowerE_Center = {LowerE_Center} ,CenterE_Center = {CenterE_Center}, UpperE_Center = {UpperE_Center}")

LowerN_Right =  int(nx+1)
CenterN_Right = int(LowerN_Right + (nx+1)*(ny/2))
UpperN_Right = int(LowerN_Right + (nx+1)* ny)
print(f"LowerN_Right = {LowerN_Right},CenterN_Right = {CenterN_Right}, UpperN_Right = {UpperN_Right}")
LowerE_Right =  int(nx)
CenterE_Right = int(LowerE_Right + nx*(ny/2))
UpperE_Right = int(LowerE_Right + nx* (ny-1))
print(f"LowerE_Right = {LowerE_Right} ,CenterE_Right = {CenterE_Right}, UpperE_Right = {UpperE_Right}")

# -------- Quarter(1/4) Node ------------------------
LowerN_LQuarter = int((nx/4)+1)
UpperrN_LQuarter = int(LowerN_LQuarter + (nx+1)* ny)
print(f"LowerN_LQuarter = {LowerN_LQuarter} ,UpperrN_LQuarter = {UpperrN_LQuarter}")
LowerE_LQuarter = int((nx/4)+1)
UpperrE_LQuarter = int(LowerE_LQuarter + (ny-1)* nx)
print(f"LowerE_LQuarter = {LowerE_LQuarter} ,UpperrE_LQuarter = {UpperrE_LQuarter}")
# -------- Quarter(3/4) Node ------------------------
LowerN_RQuarter = int((3*nx/4)+1)
UpperrN_RQuarter = int(LowerN_RQuarter + (nx+1)* ny)
print(f"LowerN_RQuarter = {LowerN_RQuarter} ,UpperrN_RQuarter = {UpperrN_RQuarter}")
LowerE_RQuarter = int((3*nx/4)+1)
UpperrE_RQuarter = int(LowerE_RQuarter + (ny-1)* nx)
print(f"LowerE_RQuarter = {LowerE_RQuarter} ,UpperrE_RQuarter = {UpperrE_RQuarter}")

# # -------- Left Side Beam Node Vel/Stress --------------------------
# LSideBeamNode_Center = LSideBeamNode_Start + 2*(ny/2) 
# LSideBeamNode_End  = LSideBeamNode_Start + 2*(ny)

# LSideBeam_Center = LSideBeam_Start + 2*(ny/2)
# LSideBeam_End = LSideBeam_Start + 2*(ny-1)
# print(f"LSideBeamNode_Start = {LSideBeamNode_Start} , LSideBeamNode_Center = {LSideBeamNode_Center}, LSideBeamNode_End={LSideBeamNode_End}")
# print(f"LSideBeam_Start = {LSideBeam_Start} , LSideBeam_Center = {LSideBeam_Center}, LSideBeam_End ={LSideBeam_End}")

# # -------- Left Side Beam Center Node Vel/Stress --------------------------
# LSideBeam_CenterNodeStart = LSideBeamNode_Start +1
# LSideBeam_CenterNodeStartplus = LSideBeamNode_Start +2

# LSideBeam_CenterNode = LSideBeamNode_Center +1
# LSideBeamNode_CenterNodeEnd = LSideBeamNode_End -1
# print(f"LSideBeam_CenterNodeStart = {LSideBeam_CenterNodeStart},LSideBeam_CenterNodeStartplus={LSideBeam_CenterNodeStartplus} , LSideBeam_CenterNode = {LSideBeam_CenterNode}, LSideBeamNode_CenterNodeEnd ={LSideBeamNode_CenterNodeEnd}")
# LSideNDash_CenterFree = LSideNDash_Start + 2*(ny/2)
# LSideNDash_EndFree = LSideNDash_Start + 2*(ny-1)  # 205
# print(f"LSideNDash_Start = {LSideNDash_Start} , LSideNDash_CenterFree = {LSideNDash_CenterFree}, LSideNDash_EndFree ={LSideNDash_EndFree}")
# # --------Left Side dash free/fix Velocity ----------------
# LSideNDash_StartFix = LSideNDash_Start +1
# LSideNDash_CenterFix = LSideNDash_CenterFree +1
# LSideNDash_EndFix = LSideNDash_EndFree +1 # 206
# print(f"LSideNDash_StartFix = {LSideNDash_StartFix} , LSideNDash_CenterFix = {LSideNDash_CenterFix}, LSideNDash_EndFix ={LSideNDash_EndFix}")

# # -------- Right Beam Node Velocity / Stress----------------
# RSideBeamNode_Center = RSideBeamNode_Start + 2*(ny/2) 
# RSideBeamNode_End  = RSideBeamNode_Start + 2*(ny)

# RSideBeamNode_Startplus = RSideBeamNode_Start +1 
# RSideBeamNode_Startplus2 = RSideBeamNode_Start +2 

# RSideBeam_Center = RSideBeam_Start + 2*(ny/2)
# RSideBeam_End = RSideBeam_Start + 2*(ny-1)
# print(f"RSideBeamNode_Start = {RSideBeamNode_Start} , RSideBeamNode_Center = {RSideBeamNode_Center}, RSideBeamNode_End={RSideBeamNode_End}")
# print(f"RSideBeamNode_Startplus = {RSideBeamNode_Startplus} , RSideBeamNode_Startplus2 = {RSideBeamNode_Startplus2}")
# print(f"RSideBeam_Start = {RSideBeam_Start} , RSideBeam_Center = {RSideBeam_Center}, RSideBeam_End ={RSideBeam_End}")

# # -------- Right Beam Center Node Velocity----------------
# RSideNDash_CenterFree = RSideNDash_Start + 2*(ny/2) #238
# RSideNDash_EndFree = RSideNDash_Start + 2*(ny-1)  # 246
# print(f"RSideNDash_Start = {RSideNDash_Start} , RSideNDash_CenterFree = {RSideNDash_CenterFree}, RSideNDash_EndFree ={RSideNDash_EndFree}")
# # --------Right Side dash free/fix Velocity ----------------
# RSideNDash_StartFix = RSideNDash_Start +1
# RSideNDash_CenterFix = RSideNDash_CenterFree +1 #239
# RSideNDash_EndFix = RSideNDash_EndFree +1 # 247
# print(f"RSideNDash_StartFix = {RSideNDash_StartFix} , RSideNDash_CenterFix = {RSideNDash_CenterFix}, RSideNDash_EndFix ={RSideNDash_EndFix}")

# -------- Soil B.C (Tie BC) ---------------
for i in range(ny+1):
    equalDOF((nx+1)*i+1,(nx+1)*i+(nx+1),1,2)

# #  ================ Make Find Stiffnes and Mass Matrix =============================
# Path = f'D:/shiang/opensees/20220330/OpenSeesPy/2D_Absorb/{Choose_Wave}/W_{int(soilwidth)}m/HZ_{HZ}/LKDash_Surface_{ny}row'  #/{Scale}{Compare_For}
# wipeAnalysis()
# system('FullGeneral')
# analysis('Transient')

# # Mass
# integrator('GimmeMCK',1.0,0.0,0.0) 
# analyze(1,0.0)

# # # Number of equations in the model
# # N = systemSize() # Has to be done after analyze

# # MASS = printA('-file', f'{Path}/M.out') #, '-ret' / Or use ops.printA('-file','M.out')

# # # Stiffness
# # integrator('GimmeMCK',0.0,0.0,1.0)
# # analyze(1,0.0)
# # K_Stiffness = printA('-file',f'{Path}/K.out') # ,'-ret'
# # # K = np.array(K)
# # # K.shape = (N,N)
# # # print(K)

# Nmodes = 20# SoilNode_End-1
# lam = eigen('-standard','-symmBandLapack',Nmodes) # With no considered Mass matrix
# # lam = eigen(Nmodes) # Full Generalize Eigen 
# # print('Computed eigenvalues:',lam)
# # omega = np.zeros(len(lam))
# # for i in range(len(lam)):
# #     omega[i] =(lam[i]**0.5)

# # Tperiod = np.zeros(len(omega))
# # for j in range(len(omega)):
# #     Tperiod[j] = (2*pi)/omega[j]

# # np.savetxt(f'{Path}/Tperiod.txt',Tperiod, delimiter = " ")
# # print(f"Tperiod = {Tperiod}")

# # print('Eigenvector 1')
# # print(nodeEigenvector(1,1), nodeEigenvector(2,1))

# # print('Eigenvector 2')
# # print(nodeEigenvector(1,2), nodeEigenvector(2,2))

# modalProperties('-print', '-file', f'{Path}/ModalReport3.txt', '-unorm')
    
# ============== Build Beam element (100~108) (ele 81~88) =========================
BeamNode_Start = SoilNode_End + 1
BeamEle_Start = SoilEle_End +1

model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(BeamNode_Start+j, Dw*j,0.0)
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

# ============================ Beam element dashpot =============================== #
BotTDash_Start = BeamNode_Start + (nx+1)
BotNDash_Start = BotTDash_Start + 2*(nx+1)

for l in range(nx+1):
# ------------- traction dashpot (node 109,110~ 125,126)-> for S wave------------
    node(BotTDash_Start+2*l, Dw*l, 0.0)
    node((BotTDash_Start+1)+2*l, Dw*l, 0.0)
# ---------- dashpot dir: Vs -> x dir ---------------------     
    fix(BotTDash_Start+2*l, 0, 1, 1)      # x dir dashpot　
    fix((BotTDash_Start+1)+2*l, 1, 1, 1)      # fixed end to let soil fix

# ------------- Normal dashpot (node 127,128~ 143,144)-> for P wave ------------
    node(BotNDash_Start+2*l, Dw*l, 0.0)
    node((BotNDash_Start+1)+2*l, Dw*l, 0.0)
# ---------- dashpot dir: Vp -> y dir---------------------     
    fix(BotNDash_Start+2*l, 1, 0, 1)      # y dir dashpot　
    fix((BotNDash_Start+1)+2*l, 1, 1, 1)      # fixed end to let soil fix
    
# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
for k in range(nx+1):
# --------------traction dashpot: for S wave------------------
    equalDOF(1+k,BotTDash_Start+2*k,1)
# --------------Normal dashpot: for P wave------------------
    equalDOF(1+k,BotNDash_Start+2*k,2)

print("Finished creating all Bottom dashpot boundary conditions and equalDOF...")
# ------------------- ZeroLength to Build dashpot: Material ----------------------------------
sizeX = Dw  # 0.125m ******
B_Smp = 0.5*rho*Vp*sizeX      # lower Left and Right corner node dashpot :N (newton)
B_Sms = 0.5*rho*Vs*sizeX      # lower Left and Right corner node dashpot :N (newton)

B_Cmp = 1.0*rho*Vp*sizeX      # Bottom Center node dashpot :N (newton)
B_Cms = 1.0*rho*Vs*sizeX      # Bottom Center node dashpot :N (newton)

uniaxialMaterial('Viscous',4000, B_Smp, 1)    # P wave: Side node
uniaxialMaterial('Viscous',4001, B_Sms, 1)    # S wave: Side node

uniaxialMaterial('Viscous',4002, B_Cmp, 1)    # P wave: Center node
uniaxialMaterial('Viscous',4003, B_Cms, 1)    # S wave: Center node

#----------- dashpot elements: Vs with x dir / Vp with y-dir------------------
xdir = 1
ydir = 2
# ------ Traction dashpot element: Vs with x dir
BotTEle_Start = BeamEle_Start + nx
BotTEle_End = BotTEle_Start + nx

element('zeroLength',BotTEle_Start,(BotTDash_Start+1),BotTDash_Start, '-mat',4001,'-dir',xdir)  # node 1: Left side
element('zeroLength',BotTEle_End,(BotTDash_Start+1)+2*nx,BotTDash_Start+2*nx, '-mat',4001,'-dir',xdir)  # node 8: Right side
for m in range(1,nx): # nx+1
    element('zeroLength',BotTEle_Start+m,(BotTDash_Start+1)+2*m,BotTDash_Start+2*m, '-mat',4003,'-dir',xdir)  # node 1: Left side
    # print(BotTEle_Start+m,(BotTDash_Start+1)+2*m,BotTDash_Start+2*m)
# ------ Normal dashpot element: Vp with y dir (98~106)
BotNEle_Start = BotTEle_End+1
BotNEle_End = BotNEle_Start+nx

element('zeroLength',BotNEle_Start,(BotNDash_Start+1),BotNDash_Start, '-mat',4000,'-dir',ydir)
element('zeroLength',BotNEle_End,(BotNDash_Start+1)+2*nx,BotNDash_Start+2*nx, '-mat',4000,'-dir',ydir)
for m in range(1,nx): # nx+1
    element('zeroLength',BotNEle_Start+m,(BotNDash_Start+1)+2*m,BotNDash_Start+2*m, '-mat',4002,'-dir',ydir)  # node 1: Left side
    # print(BotNEle_Start+m,(BotNDash_Start+1)+2*m,BotNDash_Start+2*m)
print("Finished creating Bottom dashpot material and element...")

# # ============== Soil Left and Right "Side" Dashpot =====================================
# LSideNDash_Start =  BotNDash_Start + 2*(nx+1)
# LSideTDash_Start =  LSideNDash_Start + 2*(ny+1)
# # print(LSideNDash_Start,LSideTDash_Start)
# RSideNDash_Start =  LSideTDash_Start + 2*(ny+1)
# RSideTDash_Start =  RSideNDash_Start + 2*(ny+1)
# # print(RSideNDash_Start,RSideTDash_Start)
# for l in range(ny+1):
# # ========= Left Side =============
# # --------- Normal dashpot (node 145,146~ 165,166)-> for S wave------------
#     node(LSideNDash_Start+2*l, 0.0, yMesh*l)
#     node((LSideNDash_Start+1)+2*l, 0.0, yMesh*l)
# # ---------- dashpot dir: Vs -> x dir ---------------------     
#     fix(LSideNDash_Start+2*l, 0, 1, 1)      # x dir dashpot　
#     fix((LSideNDash_Start+1)+2*l, 1, 1, 1)      # fixed end to let soil fix

# # --------- Traction dashpot (node 167,168~ 187,188)-> for P wave------------
#     node(LSideTDash_Start+2*l, 0.0, yMesh*l)
#     node((LSideTDash_Start+1)+2*l, 0.0, yMesh*l)
# # ---------- dashpot dir: Vp -> y dir ---------------------     
#     fix(LSideTDash_Start+2*l, 1, 0, 1)      # y dir dashpot　
#     fix((LSideTDash_Start+1)+2*l, 1, 1, 1)      # fixed end to let soil fix

# # ========= Right Side =============
# # --------- Normal dashpot (node 189,190~ 209,210)-> for S wave------------
#     node(RSideNDash_Start+2*l, soilwidth, yMesh*l)
#     node((RSideNDash_Start+1)+2*l, soilwidth, yMesh*l)
# # ---------- dashpot dir: Vs -> x dir ---------------------     
#     fix(RSideNDash_Start+2*l, 0, 1, 1)      # x dir dashpot　
#     fix((RSideNDash_Start+1)+2*l, 1, 1, 1)      # fixed end to let soil fix

# # --------- Traction dashpot (node 211,212~ 231,232)-> for P wave------------
#     node(RSideTDash_Start+2*l, soilwidth, yMesh*l)
#     node((RSideTDash_Start+1)+2*l, soilwidth, yMesh*l)
# # ---------- dashpot dir: Vp -> y dir ---------------------     
#     fix(RSideTDash_Start+2*l, 1, 0, 1)      # y dir dashpot　
#     fix((RSideTDash_Start+1)+2*l, 1, 1, 1)      # fixed end to let soil fix

# # ------ connect dashpot with Soil side layer :Vs with x dir / Vp with y-dir --------------
# for l in range(ny+1):
# # ========= Left Side =============
# # --------------Normal dashpot: for S wave------------------
#     equalDOF(1+(nx+1)*l, LSideNDash_Start+2*l, 1)  # x dir
# # --------------Traction dashpot: for P wave------------------
#     equalDOF(1+(nx+1)*l, LSideTDash_Start+2*l, 2)  # y dir

# # ========= Right Side =============
# # --------------Normal dashpot: for S wave------------------
#     equalDOF((nx+1)+(nx+1)*l, RSideNDash_Start+2*l, 1)  # x dir
# # --------------Traction dashpot: for P wave------------------
#     equalDOF((nx+1)+(nx+1)*l, RSideTDash_Start+2*l, 2)  # y dir

# print("Finished creating all Side dashpot boundary conditions and equalDOF...")
# # ------------- Side dashpot material -----------------------
# sizeX1 = yMesh
# S_Smp = 0.5*rho*Vp*sizeX1    # side Normal dashpot for S wave   ; lower/Upper  Left and Right corner node
# S_Sms = 0.5*rho*Vs*sizeX1    # side Traction dashpot for P wave ; lower/Upper Left and Right corner node

# S_Cmp = 1.0*rho*Vp*sizeX1    # side Normal dashpot for S wave: Netwon
# S_Cms = 1.0*rho*Vs*sizeX1    # side Traction dashpot for P wave: Netwon

# uniaxialMaterial('Viscous',4004, S_Smp, 1)    # "S" wave: Side node
# uniaxialMaterial('Viscous',4005, S_Sms, 1)    # "P" wave: Side node

# uniaxialMaterial('Viscous',4006, S_Cmp, 1)    # "S" wave: Center node
# uniaxialMaterial('Viscous',4007, S_Cms, 1)    # "P" wave: Center node

# # # =============== Right and Left NODE :different dashpot element==================
# LsideNEle_Start = BotNEle_End + 1
# LsideNEle_End = LsideNEle_Start + ny
# # print(LsideNEle_Start, LsideNEle_End)
# #  ----------- Left side Normal: S wave ----------
# element('zeroLength',LsideNEle_Start, (LSideNDash_Start+1), LSideNDash_Start, '-mat',4004,'-dir',xdir)  # lower Left node: -> Smp
# element('zeroLength',LsideNEle_End, (LSideNDash_Start+1)+2*ny, LSideNDash_Start+2*ny, '-mat',4004,'-dir',xdir)  # Upper left node: -> Smp

# LsideTEle_Start = LsideNEle_End + 1
# LsideTEle_End = LsideTEle_Start + ny
# # print(LsideTEle_Start, LsideTEle_End)
# #  ----------- Left side Traction: P wave ----------
# element('zeroLength',LsideTEle_Start, (LSideTDash_Start+1), LSideTDash_Start, '-mat',4005,'-dir',ydir)  # lower Left node: -> Sms
# element('zeroLength',LsideTEle_End, (LSideTDash_Start+1)+2*ny, LSideTDash_Start+2*ny, '-mat',4005,'-dir',ydir)  # Upper left node -> Sms

# RsideNEle_Start = LsideTEle_End + 1
# RsideNEle_End = RsideNEle_Start + ny
# # print(RsideNEle_Start, RsideNEle_End)
# #  ----------- Right side Normal: S wave ----------
# element('zeroLength',RsideNEle_Start, (RSideNDash_Start+1), RSideNDash_Start, '-mat',4004,'-dir',xdir)  # lower Right node: -> Smp
# element('zeroLength',RsideNEle_End, (RSideNDash_Start+1)+2*ny, RSideNDash_Start+2*ny, '-mat',4004,'-dir',xdir)   # Upper Right node: -> Smp

# RsideTEle_Start = RsideNEle_End + 1
# RsideTEle_End = RsideTEle_Start + ny
# # print(RsideTEle_Start, RsideTEle_End)
# #  ----------- Right side Traction: P wave ----------
# element('zeroLength',RsideTEle_Start, (RSideTDash_Start+1), RSideTDash_Start, '-mat',4005,'-dir',ydir)  # lower Right node: -> Sms
# element('zeroLength',RsideTEle_End, (RSideTDash_Start+1)+2*ny, RSideTDash_Start+2*ny, '-mat',4005,'-dir',ydir)  # Upper Right node: -> Sms

# for w in range(1,ny): #1,ny
# #----------- Left side Normal Dashpot: (ele 107~117)---------- -> Smp
#     element('zeroLength',LsideNEle_Start+w, (LSideNDash_Start+1)+2*w, LSideNDash_Start+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
# #----------- Left side Traction Dashpot: (ele 118~128) ---------- -> Sms
#     element('zeroLength',LsideTEle_Start+w, (LSideTDash_Start+1)+2*w, LSideTDash_Start+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave
#     # print(LsideTEle_Start+w, (LSideTDash_Start+1)+2*w, LSideTDash_Start+2*w)
# #----------- Right side Normal Dashpot:(ele 129 ~ 139) ---------- -> Smp
#     element('zeroLength',RsideNEle_Start+w, (RSideNDash_Start+1)+2*w, RSideNDash_Start+2*w, '-mat',4006,'-dir',xdir)  # center node : S wave
# #----------- Right side Traction Dashpot: (ele 140 ~ 150) ----------  -> Sms
#     element('zeroLength',RsideTEle_Start+w, (RSideTDash_Start+1)+2*w, RSideTDash_Start+2*w, '-mat',4007,'-dir',ydir)  # center node：P wave
#     # print(RsideTEle_Start+w, (RSideTDash_Start+1)+2*w, RSideTDash_Start+2*w)
# # print("Finished creating Side dashpot material and element...")

# # ==================== Surface Middle Beam (W = 1m) ===============================
# TopLeft_Node = UpperN_Center - int(0.5/Dw)
# TopMid_Node = UpperN_Center
# TopRight_Node = UpperN_Center + int(0.5/Dw)
# print(f"TopLeft_Node = {TopLeft_Node}, TopMid_Node = {TopMid_Node},  TopRight_Node = {TopRight_Node}")
# # printModel('-node', TopLeft_Node, TopMid_Node, TopRight_Node)

# # --------- Fide Foundation Middle and Left/ Right Node ---------------------
# # # -======= Tie Condition =======
# # Found_Left = BotNDash_Start + 2*(nx+1)
# # Found_Mid = Found_Left + 1
# # Found_Right = Found_Mid + 1

# # FoundLeft_Ele = BotNEle_End + 1
# # FoundRight_Ele = FoundLeft_Ele + 1

# # ======= LK Dashpot Condition and BeamType Condition =======
# Found_Left = RSideTDash_Start + 2*(ny+1)
# Found_Mid = Found_Left + 1
# Found_Right = Found_Mid + 1

# FoundLeft_Ele = RsideTEle_End + 1 
# FoundRight_Ele = FoundLeft_Ele + 1

# node(Found_Left, (soilwidth/2)-0.5, soilLength)
# node(Found_Mid, (soilwidth/2), soilLength)
# node(Found_Right, (soilwidth/2)+0.5, soilLength)
# print(f'Found_Left = {Found_Left}, Found_Mid = {Found_Mid}, Found_Right = {Found_Right}')
# # printModel('-node', Found_Left, Found_Mid, Found_Right)

# fix(Found_Left,0,0,1)
# fix(Found_Mid,0,0,1)
# fix(Found_Right,0,0,1)
# # ---------- Top Foundation Beam Element ----------------------
# element('elasticBeamColumn', FoundLeft_Ele, Found_Left, Found_Mid, A,E1,Iz, 1, '-release', 3)
# element('elasticBeamColumn', FoundRight_Ele, Found_Mid, Found_Right, A,E1,Iz, 1, '-release', 3)

# # --------- Top Beam and Soil BC -----------------
# equalDOF(TopLeft_Node, Found_Left, 1,2)
# equalDOF(TopMid_Node, Found_Mid, 1,2)
# equalDOF(TopRight_Node, Found_Right, 1,2)

# # ================ NewBC: for Case A/B============================
# # ==================== Side Beam node (233~243 / 244~254) ====================
# LsideNode = Found_Right +1 # RSideTDash_Start + 2*(ny+1)
# RsideNode = LsideNode + (ny+1)
# LsideEle =  FoundRight_Ele +1 # RsideTEle_End + 1 
# RsideEle = LsideEle + ny

# for i in range(ny+1):
# # ----- Left Side: 233~243 -----------------
#     node(LsideNode+i, 0.0, yMesh*i)
#     fix(LsideNode+i,0,0,1)
# # ----- Right Side: 244~254 -----------------
#     node(RsideNode+i, soilwidth ,yMesh*i)
#     fix(RsideNode+i,0,0,1)

# # ------------  Beam Element: 151 ~ 160 / 161 ~ 170 ------------------
# for j in range(ny):
# # ----- Left Side Beam:151 ~ 160 -----------------
#     element('elasticBeamColumn', LsideEle+j, LsideNode+j, (LsideNode+1)+j, A,E1,Iz, 1, '-release', 3)
# # ----- Right Side Beam:161 ~ 170 -----------------
#     element('elasticBeamColumn', RsideEle+j, RsideNode+j, (RsideNode+1)+j, A,E1,Iz, 1, '-release', 3)

# # --------- Side Beam and Soil BC -----------------
# for j in range(ny+1):
#     equalDOF(1+(nx+1)*j,LsideNode+j,1,2)
#     equalDOF((nx+1)+(nx+1)*j,RsideNode+j,1,2)

# ============================== S wave ======================================
# ========================= "CaseA": SideLoad Pattern ===================================
# ------------ Side Load Pattern ------------------------------
# xTimeSeriesID = 800
# xPatternID = 804
# for g in range(ny):
# # ------- timeSeries ID: 800~809 / Pattern ID: 804~813----------------------
#     timeSeries('Path',xTimeSeriesID+g, '-filePath',f'SSideforce_{ny}rowx/ele{1+g}.txt','-dt', dt)
#     pattern('Plain',xPatternID+g, xTimeSeriesID+g)
# # ---------- x direction : Sideforce ---------------------
# # ---------- Distributed at Left Side Beam ----------------------
#     eleLoad('-ele',LsideEle+g, '-type', '-beamUniform',-20,0)  # for local axes Wy -
# # ---------- Distributed at Right Side Beam ----------------------
#     eleLoad('-ele',RsideEle+g, '-type', '-beamUniform',-20,0)   # for local axes Wy +

# yTimeSeriesID = xTimeSeriesID + ny
# yPatternID  = xPatternID + ny

# for g in range(ny):
# # ------- timeSeries ID: 810~819 / Pattern ID:814~823 ----------------------
# # ---------- y direction : Sideforce --------------------
#     timeSeries('Path',yTimeSeriesID+g, '-filePath',f'SSideforce_{ny}rowy/ele{1+g}.txt','-dt', dt)
#     pattern('Plain',yPatternID+g, yTimeSeriesID+g)
# # ---------- For P wave : y direction ---------------------
# # ---------- Distributed at Left Side Beam ----------------------
#     eleLoad('-ele',LsideEle+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# # ---------- Distributed at Right Side Beam ----------------------
#     eleLoad('-ele',RsideEle+g, '-type', '-beamUniform',0,-20,0)   # for local axes Wx -

# # ========================= "Case B": Side Node Dashpot ===================================
# # ------------ Side Nodal Load Pattern ------------------------------
# xTimeSeriesID = 800
# xPatternID = 804

# LsideNode = 1
# RsideNode = 1 + nx #1+(nx+1)*ny


# timeSeries('Path',xTimeSeriesID, '-filePath',f'S_Nodeforce_{ny}rowx/node{1}.txt','-dt',dt)
# pattern('Plain',xPatternID, xTimeSeriesID)
# # ---- NodeForce at Left Side Corner -----
# load(LsideNode, 20*yMesh*0.5,0) # 10,0,0
# # ---- NodeForce at Right Side Corner -----
# load(RsideNode, 20*yMesh*0.5,0)
# # print(LsideNode,RsideNode, f'S_Nodeforce_{ny}rowx/node{1}.txt')

# timeSeries('Path',xTimeSeriesID+ny, '-filePath',f'S_Nodeforce_{ny}rowx/node{ny+1}.txt','-dt',dt)
# pattern('Plain',xPatternID+ny, xTimeSeriesID+ny)
# # ---- NodeForce at Left Side Corner -----
# load(LsideNode+(nx+1)*ny, 20*yMesh*0.5,0)
# # ---- NodeForce at Right Side Corner -----
# load(RsideNode+(nx+1)* ny, 20*yMesh*0.5,0)
# # print(LsideNode+(nx+1)*ny, RsideNode+(nx+1)* ny,f'S_Nodeforce_{ny}rowx/node{ny+1}.txt')

# for g in range(1,ny):
# # ------- timeSeries ID: 800~810 / Pattern ID: 804~814----------------------
#     timeSeries('Path',xTimeSeriesID+g, '-filePath',f'S_Nodeforce_{ny}rowx/node{1+g}.txt','-dt', dt)
#     pattern('Plain',xPatternID+g, xTimeSeriesID+g)
# # # ---------- x direction : Sideforce ---------------------
# # ---------- NodeForce at Left Side Beam ----------------------
#     load(LsideNode+(nx+1)*g, 20*yMesh*1,0)
# # ---------- NodeForce at Right Side Beam ----------------------
#     load(RsideNode+(nx+1)*g, 20*yMesh*1,0)
#     # print(LsideNode+(nx+1)*g, RsideNode+(nx+1)*g,f'S_Nodeforce_{ny}rowx/node{1+g}')
# # print("Nodalforce= ", 20*yMesh*0.5, 20*yMesh*1 )

# # ------------------ SideForce Nodal Load: Py ---------------------------------
# yTimeSeriesID = xTimeSeriesID + (ny+1)
# yPatternID  = xPatternID + (ny+1)

# timeSeries('Path',yTimeSeriesID, '-filePath',f'S_Nodeforce_{ny}rowy/node{1}.txt','-dt',dt)
# pattern('Plain',yPatternID, yTimeSeriesID)
# # ---- NodeForce at Left Side Corner -----
# load(LsideNode, 0, +20*yMesh*0.5) # 10,0,0
# # ---- NodeForce at Right Side Corner -----
# load(RsideNode, 0, -20*yMesh*0.5)
# # print(LsideNode,RsideNode, f'S_Nodeforce_{ny}rowy/node{1}.txt')

# timeSeries('Path',yTimeSeriesID+ny, '-filePath',f'S_Nodeforce_{ny}rowy/node{ny+1}.txt','-dt',dt)
# pattern('Plain',yPatternID+ny, yTimeSeriesID+ny)
# # ---- NodeForce at Left Side Corner -----
# load(LsideNode+(nx+1)*ny, 0, +20*yMesh*0.5)
# # ---- NodeForce at Right Side Corner -----
# load(RsideNode+(nx+1)*ny, 0, -20*yMesh*0.5)
# # print(LsideNode+ny,RsideNode+ny,f'S_Nodeforce_{ny}rowy/node{ny+1}.txt')

# for g in range(1,ny):
# # ------- timeSeries ID: 800~810 / Pattern ID: 804~814----------------------
#     timeSeries('Path',yTimeSeriesID+g, '-filePath',f'S_Nodeforce_{ny}rowy/node{1+g}.txt','-dt', dt)
#     pattern('Plain',yPatternID+g, yTimeSeriesID+g)
# # # ---------- x direction : Sideforce ---------------------
# # ---------- NodeForce at Left Side Beam ----------------------
#     load(LsideNode+(nx+1)*g, 0, +20*yMesh*0.5)
# # ---------- NodeForce at Right Side Beam ----------------------
#     load(RsideNode+(nx+1)*g, 0, +20*yMesh*0.5)
#     # print(LsideNode+g, RsideNode+g,f'S_Nodeforce_{ny}rowy/node{1+g}')

# # # ------------------ SideForce Distributed Load: Wy ---------------------------------
# # yTimeSeriesID = xTimeSeriesID + (ny+1)
# # yPatternID  = xPatternID + (ny+1)
# # for g in range(ny):
# # # ------- timeSeries ID: 810~819 / Pattern ID:814~823 ----------------------
# # # ---------- y direction : Sideforce --------------------
# #     timeSeries('Path',yTimeSeriesID+g, '-filePath',f'SSideforce_{ny}rowy/ele{1+g}.txt','-dt', dt)
# #     pattern('Plain',yPatternID+g, yTimeSeriesID+g)
# # # ---------- For P wave : y direction ---------------------
# # # ---------- Distributed at Left Side Beam ----------------------
# #     eleLoad('-ele',LsideEle+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# # # ---------- Distributed at Right Side Beam ----------------------
# #     eleLoad('-ele',RsideEle+g, '-type', '-beamUniform',0,-20,0)   # for local axes Wx -

# #     print(LsideEle+g, RsideEle+g,"finish SideBeam Force InputFile Apply")

# # ============== SideBeam and Dashpot for "Case C" =========================================
# # ==================== Side Beam node (145~165 / 146~164) ====================
# yMesh = soilLength/ny # Y row MeshSize
# LSideBeamNode_Start =  BotNDash_Start + 2*(nx+1)
# RSideBeamNode_Start =  LSideBeamNode_Start + 2*ny +1
# # print(LSideBeamNode_Start)
# for i in range(ny+1):
# # ----- Left Side: 145~165 -----------------
#     node(LSideBeamNode_Start+2*i, 0.0, yMesh*i)
#     mass(LSideBeamNode_Start+2*i,1,1,1)
#     fix(LSideBeamNode_Start+2*i,0,0,1)
    
#     if i < ny: #146,148...,164
#         node((LSideBeamNode_Start+1)+2*i, 0.0, (0.5*yMesh)+ yMesh*i)
#         mass((LSideBeamNode_Start+1)+2*i,1,1,1)
#         fix((LSideBeamNode_Start+1)+2*i,0,1,1)

# # ----- Right Side: 166~186 / 167~185 -----------------
#     node(RSideBeamNode_Start+2*i, soilwidth, yMesh*i)
#     mass(RSideBeamNode_Start+2*i,1,1,1)
#     fix(RSideBeamNode_Start+2*i,0,0,1)

#     if i < ny: #146,148...,164
#         node((RSideBeamNode_Start+1)+2*i, soilwidth, (0.5*yMesh)+ yMesh*i)
#         mass((RSideBeamNode_Start+1)+2*i,1,1,1)
#         fix((RSideBeamNode_Start+1)+2*i,0,1,1)

# # ============================ Apply Rayleigh Wave Absorption Dahpot ===================================================
# # ---------- Left Side Rayleigh Dashpot ---------------------
# # ----------------------------- For "LK Dashpot" -----------------------------------
# LNDash_Raly = (BotNDash_Start+1)+2*nx+ 1 #For LK Dashpot
# LTDash_Raly = LNDash_Raly + 2*(ny+1)

# RNDash_Raly = LTDash_Raly + 2*(ny+1)
# RTDash_Raly = RNDash_Raly + 2*(ny+1)
# # print(LNDash_Raly, LTDash_Raly, RNDash_Raly,RTDash_Raly )

# for Ray in range(ny+1):
#     # ------- Normal Dashpot ------------
#     node(LNDash_Raly+2*Ray, 0.0, yMesh*Ray)
#     node((LNDash_Raly+1)+2*Ray, 0.0, yMesh*Ray)
#     # ---------- dashpot dir: Vs -> x dir ---------------------     
#     fix(LNDash_Raly+2*Ray, 0, 1, 1)      # x dir dashpot　
#     fix((LNDash_Raly+1)+2*Ray, 1, 1, 1)      # fixed end to let soil fix

#     # ------- Traction Dashpot ------------
#     node(LTDash_Raly+2*Ray, 0.0, yMesh*Ray)
#     node((LTDash_Raly+1)+2*Ray , 0.0, yMesh*Ray)
#     # ---------- dashpot dir: Vs -> Y dir ---------------------     
#     fix(LTDash_Raly+2*Ray, 1, 0, 1)      # x dir dashpot　
#     fix((LTDash_Raly+1)+2*Ray, 1, 1, 1)      # fixed end to let soil fi

# # ---------- Right Side Rayleigh Dashpot ---------------------
#     # ------- Normal Dashpot ------------
#     node(RNDash_Raly+2*Ray, soilwidth, yMesh*Ray)
#     node((RNDash_Raly+1)+2*Ray, soilwidth, yMesh*Ray)
#     # ---------- dashpot dir: Vs -> x dir ---------------------     
#     fix(RNDash_Raly+2*Ray, 0, 1, 1)      # x dir dashpot　
#     fix((RNDash_Raly+1)+2*Ray, 1, 1, 1)      # fixed end to let soil fix

#     # ------- Traction Dashpot ------------
#     node(RTDash_Raly+2*Ray, soilwidth, yMesh*Ray)
#     node((RTDash_Raly+1)+2*Ray , soilwidth, yMesh*Ray)
#     # ---------- dashpot dir: Vs -> Y dir ---------------------     
#     fix(RTDash_Raly+2*Ray, 1, 0, 1)      # x dir dashpot　
#     fix((RTDash_Raly+1)+2*Ray, 1, 1, 1)      # fixed end to let soil fix

# # ------ connect dashpot with Soil side layer :Vs with x dir / Vp with y-dir --------------      
# for i in range(ny+1):
#     # ========= Left Side =============
#     # --------------Normal dashpot: for S wave------------------
#     equalDOF(1+(nx+1)*i, LNDash_Raly+2*i, 1)  # x dir
#     # --------------Traction dashpot: for P wave------------------
#     equalDOF(1+(nx+1)*i, LTDash_Raly+2*i, 2)  # y dir

#     # ========= Right Side =============
#     # --------------Normal dashpot: for S wave------------------
#     equalDOF((nx+1)+(nx+1)*i, RNDash_Raly+2*i, 1)  # x dir
#     # --------------Traction dashpot: for P wave------------------
#     equalDOF((nx+1)+(nx+1)*i, RTDash_Raly+2*i, 2)  # y dir

# # printModel('-node', 774,LNDash_Raly )
# # # ------------------------ For "Tie Boundary" -----------------------------------
# # LNDash_Raly = (BotNDash_Start+1)+2*nx+ 1
# # LTDash_Raly = LNDash_Raly + 2*(int(Apply_node))

# # RNDash_Raly = LTDash_Raly + 2*(int(Apply_node))
# # RTDash_Raly = RNDash_Raly + 2*(int(Apply_node))

# # for Ray in range(int(Apply_node)):
# #     # ------- Normal Dashpot ------------
# #     node(LNDash_Raly+2*Ray, 0.0, soilLength-(yMesh*Ray))
# #     node((LNDash_Raly+1)+2*Ray, 0.0, soilLength-(yMesh*Ray))
# #     # ---------- dashpot dir: Vs -> x dir ---------------------     
# #     fix(LNDash_Raly+2*Ray, 0, 1, 1)      # x dir dashpot　
# #     fix((LNDash_Raly+1)+2*Ray, 1, 1, 1)      # fixed end to let soil fix

# #     # ------- Traction Dashpot ------------
# #     node(LTDash_Raly+2*Ray, 0.0, soilLength-(yMesh*Ray))
# #     node((LTDash_Raly+1)+2*Ray , 0.0, soilLength-(yMesh*Ray))
# #     # ---------- dashpot dir: Vs -> Y dir ---------------------     
# #     fix(LTDash_Raly+2*Ray, 1, 0, 1)      # x dir dashpot　
# #     fix((LTDash_Raly+1)+2*Ray, 1, 1, 1)      # fixed end to let soil fix

# # # ---------- Right Side Rayleigh Dashpot ---------------------
# #     # ------- Normal Dashpot ------------
# #     node(RNDash_Raly+2*Ray, soilwidth, soilLength-(yMesh*Ray))
# #     node((RNDash_Raly+1)+2*Ray, soilwidth, soilLength-(yMesh*Ray))
# #     # ---------- dashpot dir: Vs -> x dir ---------------------     
# #     fix(RNDash_Raly+2*Ray, 0, 1, 1)      # x dir dashpot　
# #     fix((RNDash_Raly+1)+2*Ray, 1, 1, 1)      # fixed end to let soil fix

# #     # ------- Traction Dashpot ------------
# #     node(RTDash_Raly+2*Ray, soilwidth, soilLength-(yMesh*Ray))
# #     node((RTDash_Raly+1)+2*Ray , soilwidth, soilLength-(yMesh*Ray))
# #     # ---------- dashpot dir: Vs -> Y dir ---------------------     
# #     fix(RTDash_Raly+2*Ray, 1, 0, 1)      # x dir dashpot　
# #     fix((RTDash_Raly+1)+2*Ray, 1, 1, 1)      # fixed end to let soil fix

# # # ------ connect dashpot with Soil side layer :Vs with x dir / Vp with y-dir --------------      
# # for i in range(int(Apply_node)):
# #     # ========= Left Side =============
# #     # --------------Normal dashpot: for S wave------------------
# #     equalDOF(1+(nx+1)*(ny-i), LNDash_Raly+2*i, 1)  # x dir
# #     # --------------Traction dashpot: for P wave------------------
# #     equalDOF(1+(nx+1)*(ny-i), LTDash_Raly+2*i, 2)  # y dir

# #     # ========= Right Side =============
# #     # --------------Normal dashpot: for S wave------------------
# #     equalDOF((nx+1)+(nx+1)*(ny-i), RNDash_Raly+2*i, 1)  # x dir
# #     # --------------Traction dashpot: for P wave------------------
# #     equalDOF((nx+1)+(nx+1)*(ny-i), RTDash_Raly+2*i, 2)  # y dir

# # # ------------------- ZeroLength to Build Rayleigh dashpot: Material ----------------------------------
# Dwidth = 0.125 # m
# DMeshSize = yMesh

# N_Smp = 0.5*rho*Vp*Dwidth 
# T_Sms = 0.5*rho*Vs*DMeshSize     
# N_Cmp = 1.0*rho*Vp*Dwidth
# N_Cms = 1.0*rho*Vs*DMeshSize

# uniaxialMaterial('Viscous',4005, N_Smp, 1)    # P wave: Side node
# uniaxialMaterial('Viscous',4006, T_Sms, 1)    # S wave: Side node

# uniaxialMaterial('Viscous',4007, N_Cmp, 1)    # P wave: Side node
# uniaxialMaterial('Viscous',4008, N_Cms, 1)    # S wave: Side node

# # Ray_Smp = 0.5*akz*rho*Vp*Dwidth         # upper Left and Right corner node dashpot :N (newton) 
# # Ray_Sms = 0.5*bkz*rho*Vs*DMeshSize      # upper Left and Right corner node dashpot :N (newton) 
# Ray_Cmp = 1.0*akz*rho*Vp*Dwidth         # upper Left and Right corner node dashpot :N (newton) 
# Ray_Cms = 1.0*bkz*rho*Vs*DMeshSize      # upper Left and Right corner node dashpot :N (newton) 

# # uniaxialMaterial('Viscous',4010, Ray_Smp, 1)    # P wave: Side node
# # uniaxialMaterial('Viscous',4011, Ray_Sms, 1)    # S wave: Side node

# uniaxialMaterial('Viscous',4012, Ray_Cmp, 1)    # P wave: Side node
# uniaxialMaterial('Viscous',4013, Ray_Cms, 1)    # S wave: Side node
# #----------- dashpot elements: Vs with x dir / Vp with y-dir------------------
# xdir = 1
# ydir = 2
# # --------- For LK Dashpot -------------------------
# LN_Rayele = BotNEle_End + 1
# LT_Rayele = LN_Rayele + ny + 1

# RN_Rayele = LT_Rayele + ny + 1
# RT_Rayele = RN_Rayele + ny + 1
# # print(LN_Rayele, LT_Rayele, RN_Rayele, RT_Rayele)

# # ------------- Left Side Dashpot -----------------------------
# element('zeroLength',LN_Rayele, (LNDash_Raly+1), LNDash_Raly, '-mat',4005,'-dir',xdir) # Left corner LK Dashpot (Noprmal) 
# element('zeroLength',LT_Rayele, (LTDash_Raly+1), LTDash_Raly, '-mat',4006,'-dir',ydir) # Left corner LK Dashpot (Traction)
# # ------------- Right Side Dashpot -----------------------------
# element('zeroLength',RN_Rayele, (RNDash_Raly+1), RNDash_Raly, '-mat',4005,'-dir',xdir) # Right corner LK Dashpot (Noprmal)
# element('zeroLength',RT_Rayele, (RTDash_Raly+1), RTDash_Raly, '-mat',4006,'-dir',ydir) # Right corner LK Dashpot (Traction)

# for i in range(1,ny+1):
#     Soil_Deep = yMesh*i
#     if Soil_Deep < (soilLength-Applt_D): # when Apply LK Dashpot smaller than Rayleigh Dashpot Depth, focus on Body wave
#         element('zeroLength',LN_Rayele +i, (LNDash_Raly+1)+(2*i), LNDash_Raly+(2*i), '-mat',4007,'-dir',xdir)
#         element('zeroLength',LT_Rayele +i, (LTDash_Raly+1)+(2*i), LTDash_Raly+(2*i), '-mat',4008,'-dir',ydir)

#         element('zeroLength',RN_Rayele +i, (RNDash_Raly+1)+(2*i), RNDash_Raly+(2*i), '-mat',4007,'-dir',xdir)
#         element('zeroLength',RT_Rayele +i, (RTDash_Raly+1)+(2*i), RTDash_Raly+(2*i), '-mat',4008,'-dir',ydir)

#     if Soil_Deep >= (soilLength-Applt_D):
#         element('zeroLength',LN_Rayele +i, (LNDash_Raly+1)+(2*i), LNDash_Raly+(2*i), '-mat',4012,'-dir',xdir)
#         element('zeroLength',LT_Rayele +i, (LTDash_Raly+1)+(2*i), LTDash_Raly+(2*i), '-mat',4013,'-dir',ydir)

#         element('zeroLength',RN_Rayele +i, (RNDash_Raly+1)+(2*i), RNDash_Raly+(2*i), '-mat',4012,'-dir',xdir)
#         element('zeroLength',RT_Rayele +i, (RTDash_Raly+1)+(2*i), RTDash_Raly+(2*i), '-mat',4013,'-dir',ydir)

# # --------- For Tie Boundary -------------------------
# LN_Rayele = BotNEle_End + 1
# LT_Rayele = LN_Rayele + int(Apply_node)
# # print(LN_Rayele, LT_Rayele)
# RN_Rayele = LT_Rayele + int(Apply_node)
# RT_Rayele = RN_Rayele + int(Apply_node)

# # ------------------------- Left Side Corner Dashpot -----------------------------------
# element('zeroLength',LN_Rayele, (LNDash_Raly+1), LNDash_Raly, '-mat',4010,'-dir',xdir)
# element('zeroLength',LT_Rayele, (LTDash_Raly+1), LTDash_Raly, '-mat',4011,'-dir',ydir)
# # ------------------------- Right Sid1)+2*i, RNDash_Raly+2*i, '-mat',4012,'-dir',xdir)  # node 1: Left side
#     # ------ Traction dashpot element: Vp with y dire Corner Dashpot -----------------------------------
# element('zeroLength',RN_Rayele, (RNDash_Raly+1), RNDash_Raly, '-mat',4010,'-dir',xdir)
# element('zeroLength',RT_Rayele, (RTDash_Raly+1), RTDash_Raly, '-mat',4011,'-dir',ydir)
# # print(LT_Rayele, (LTDash_Raly+1), LTDash_Raly)
# for i in range(1,int(Apply_node)):
#     # ------ Normal dashpot element: Vs with x dir
#     element('zeroLength',LN_Rayele+ i, (LNDash_Raly+1)+2*i, LNDash_Raly+2*i, '-mat',4012,'-dir',xdir)  # node 1: Left side
#     # ------ Traction dashpot element: Vp with y dir
#     element('zeroLength',LT_Rayele+ i, (LTDash_Raly+1)+2*i, LTDash_Raly+2*i, '-mat',4013,'-dir',ydir)  # node 8: Right side
#     # print(LT_Rayele+ i, (LTDash_Raly+1)+2*i, LTDash_Raly+2*i)

#     # ------ Normal dashpot element: Vs with x dir
#     element('zeroLength',RN_Rayele+ i, (RNDash_Raly+
#     element('zeroLength',RT_Rayele+ i, (RTDash_Raly+1)+2*i, RTDash_Raly+2*i, '-mat',4013,'-dir',ydir)  # node 8: Right side
#     # print(RT_Rayele+ i, (RTDash_Raly+1)+2*i, RTDash_Raly+2*i)
# ======================================== Rayleigh Dashpot END ===============================================

#=========================== Load Pattern 1: Shear wave / P wave ============================
TimeSeries_Path = f"D:/shiang/opensees/20220330/OpenSeesPy/TimeSeries"
#------------- Original TimeSeries dt => Pwave = 3.125e-05 ; Swave = 6.25e-05 ---------------------------------------
#------------- New TimeSeries dt (Dy = 40 row) => Pwave = 6.25e-05 ; Swave = 1.25e-04 ------------------------------------
Pwave_dt = 6.25e-05
Swave_dt = 1.25e-04

timeSeries('Path',702, '-filePath', f'{TimeSeries_Path}/Pwave_Time/New_Time/fp_Dt0.1_HZ10.txt','-dt', Pwave_dt) # HZ = 10
timeSeries('Path',704, '-filePath', f'{TimeSeries_Path}/Pwave_Time/New_Time/fp_Dt0.1_HZ20.txt','-dt', Pwave_dt) # HZ = 20
timeSeries('Path',705, '-filePath', f'{TimeSeries_Path}/Pwave_Time/New_Time/fp_Dt0.1_HZ40.txt','-dt', Pwave_dt) # HZ = 40
timeSeries('Path',706, '-filePath', f'{TimeSeries_Path}/Pwave_Time/New_Time/fp_Dt0.1_HZ80.txt','-dt', Pwave_dt) # HZ = 80

timeSeries('Path',707, '-filePath', f'{TimeSeries_Path}/Swave_Time/New_Time/fs_Dt0.1_HZ10.txt','-dt', Swave_dt) # HZ = 10
timeSeries('Path',708, '-filePath', f'{TimeSeries_Path}/Swave_Time/New_Time/fs_Dt0.1_HZ20.txt','-dt', Swave_dt) # HZ = 20
timeSeries('Path',709, '-filePath', f'{TimeSeries_Path}/Swave_Time/New_Time/fs_Dt0.1_HZ40.txt','-dt', Swave_dt) # HZ = 40
timeSeries('Path',710, '-filePath', f'{TimeSeries_Path}/Swave_Time/New_Time/fs_Dt0.1_HZ80.txt','-dt', Swave_dt) # HZ = 80

# pattern('Plain',703, 705) # TimeSeries_Num
# # ------------- P wave -----------------------------.
# for o in range(nx):
#     eleLoad('-ele', BeamEle_Start+o, '-type','-beamUniform',20*1e4,0) # *1e4

# # # ------------- S wave -----------------------------
# # for o in range(nx):
# #     eleLoad('-ele', BeamEle_Start+o, '-type','-beamUniform',0,20*1e4,0)

# ===================== Load Pattern 2: TopForce on the top Middle Foundation (Foundation width = 1m, r = 0.5m)======================
# # --------- Fide Foundation Middle and Left/ Right Node ---------------------
# TopLeft_Node = UpperN_Center - int(0.5/Dw)
# TopMid_Node = UpperN_Center
# TopRight_Node = UpperN_Center + int(0.5/Dw)
# print(f"TopLeft_Node = {TopLeft_Node}, TopMid_Node = {TopMid_Node},  TopRight_Node = {TopRight_Node}")
# # printModel('-node', TopLeft_Node, TopMid_Node, TopRight_Node)

Total_Force = 20*1e4 # Vertical/ Horizon= 20*1e4 ; Rocking= 20*1e4*3.35
Distribute_Force = Total_Force/(4*Dw)
print(f'Distributed Load = {Distribute_Force}; Py = {Distribute_Force*(2*Dw)/2}')

pattern('Plain',703, 706) # TimeSeries_Num
# # ------------- Case 1 => Vertical Apply: P wave TimeSeries -----------------------------
# # load(Found_Left, 0,-0.5*1e5)
# # load(Found_Mid, 0,-1*1e5)
# # load(Found_Right, 0,-0.5*1e5)

# load(UpperN_Center-2, 0,-0.5*1e5) # TopLeft 2  x=0.50
# load(UpperN_Center-1, 0,-1.0*1e5) # TopLeft 1  x=0.25
# load(UpperN_Center,   0,-1.0*1e5) 
# load(UpperN_Center+1, 0,-1.0*1e5) # TopRight 1  x=0.25
# load(UpperN_Center+2, 0,-0.5*1e5) # TopRight 2  x=0.50

# # eleLoad('-ele', FoundLeft_Ele, '-type','-beamUniform', -Distribute_Force,0) # *1e4
# # eleLoad('-ele', FoundRight_Ele, '-type','-beamUniform', -Distribute_Force,0) # *1e4

# #  ------------- Case 2 => Horizon Apply: S wave TimeSeries -----------------------------
# # load(Found_Left, 0.5*1e5, 0)
# # load(CenterN_Center, 1*1e5, 0)
# # load(Found_Right, 0.5*1e5, 0)

# load(UpperN_Center-2, 0.5*1e5, 0) # TopLeft 2  x=0.50
# load(UpperN_Center-1, 1.0*1e5, 0) # TopLeft 1  x=0.25
# load(UpperN_Center,   1.0*1e5, 0) 
# load(UpperN_Center+1, 1.0*1e5, 0) # TopRight 1  x=0.25
# load(UpperN_Center+2, 0.5*1e5, 0) # TopRight 2  x=0.50

# # eleLoad('-ele', FoundLeft_Ele, '-type','-beamUniform',0, Distribute_Force,0)
# # eleLoad('-ele', FoundRight_Ele, '-type','-beamUniform',0, Distribute_Force,0)

#  ------------- Case 3 => Rocking Apply: P wave TimeSeries -----------------------------
# -------------- Rocking point Load ------------------
Total_ApplyNode = int(0.5/Dw)
# print(Total_ApplyNode)
Py = 1e5*3.35*2 # 1e5*3.35 / 1e6 
# for o in range(1, Total_ApplyNode+1):
#     # --------- Left Side ----------------
#     load(UpperN_Center-o, 0, Py*((Dw*o)/0.5))
#     # --------- Right Side ----------------
#     load(UpperN_Center+o, 0, -Py*((Dw*o)/0.5))
#     print(Py*((Dw*o)/0.5))

load(UpperN_Center-2, 0, -(3/32)*Py) # TopLeft 2  x=0.50
load(UpperN_Center-1, 0, -(1/8)*Py) # TopLeft 1  x=0.25
# load(UpperN_Center,   (1/32)*1e5, 0) 
load(UpperN_Center+1, 0, (1/8)*Py) # TopRight 1  x=0.25
load(UpperN_Center+2, 0, (3/32)*Py) # TopRight 2  x=0.50

# # -------------- Rocking Distributed Beam Load ------------------
# aOverL_Left = 0/(2*Dw)
# bOverL_Left = (2*Dw)/(2*Dw)
# print(f'Left Beam: aOverL_Left ={aOverL_Left}; bOverL_Left = {bOverL_Left}')

# aOverL_Right = 0/(2*Dw)
# bOverL_Right = (2*Dw)/(2*Dw)
# print(f'Left Beam: aOverL_Right ={aOverL_Right}; bOverL_Right = {bOverL_Right}')

# eleLoad('-ele', FoundLeft_Ele, '-type','-beamUniform', -Distribute_Force, 0, aOverL_Left, bOverL_Left, 0, 0) # i to j end
# eleLoad('-ele', FoundRight_Ele, '-type','-beamUniform',0, 0, aOverL_Right, bOverL_Right, +Distribute_Force, 0) # i to j end

print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# -------------- Recorder --------------------------------
# # recorder('Element', '-file', 'Stressele500.out', '-time', '-ele',500, 'globalForce')
# # recorder('Element', '-file', 'ele501.out', '-time', '-ele',501, 'globalForce')
# ------------- left column -------------
recorder('Element', '-file', f'{path2}/ele{LowerE_Left}.out', '-time', '-ele',LowerE_Left, 'material ',1,'stresses')
recorder('Element', '-file', f'{path2}/ele{CenterE_Left}.out', '-time', '-ele',CenterE_Left, 'material ',1,'stresses')
recorder('Element', '-file', f'{path2}/ele{UpperE_Left}.out', '-time', '-ele',UpperE_Left, 'material ',1,'stresses')

recorder('Node', '-file', f'{path1}/node{LowerN_Left}.out', '-time', '-node',LowerN_Left,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'{path1}/node{CenterN_Left}.out', '-time', '-node',CenterN_Left,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'{path1}/node{UpperN_Left}.out', '-time', '-node',UpperN_Left,'-dof',1,2,3,'vel')
# ------------- Center column -------------
recorder('Element', '-file', f'{path2}/ele{LowerE_Center}.out', '-time', '-ele',LowerE_Center, 'material ',1,'stresses')
recorder('Element', '-file', f'{path2}/ele{CenterE_Center}.out', '-time', '-ele',CenterE_Center, 'material ',1,'stresses')
recorder('Element', '-file', f'{path2}/ele{UpperE_Center}.out', '-time', '-ele',UpperE_Center, 'material ',1,'stresses')

recorder('Node', '-file', f'{path1}/node{LowerN_Center}.out', '-time', '-node',LowerN_Center,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'{path1}/node{CenterN_Center}.out', '-time', '-node',CenterN_Center,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'{path1}/node{UpperN_Center}.out', '-time', '-node',UpperN_Center,'-dof',1,2,3,'vel')
# ------------- Right column -------------
recorder('Element', '-file', f'{path2}/ele{LowerE_Right}.out', '-time', '-ele',LowerE_Right, 'material ',1,'stresses')
recorder('Element', '-file', f'{path2}/ele{CenterE_Right}.out', '-time', '-ele',CenterE_Right, 'material ',1,'stresses')
recorder('Element', '-file', f'{path2}/ele{UpperE_Right}.out', '-time', '-ele',UpperE_Right, 'material ',1,'stresses')

recorder('Node', '-file', f'{path1}/node{LowerN_Right}.out', '-time', '-node',LowerN_Right,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'{path1}/node{CenterN_Right}.out', '-time', '-node',CenterN_Right,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'{path1}/node{UpperN_Right}.out', '-time', '-node',UpperN_Right,'-dof',1,2,3,'vel')

# # ==== Left 1/4 node ======================================
# recorder('Element', '-file', f'{path2}/ele{UpperrE_LQuarter}.out', '-time', '-ele',UpperrE_LQuarter, 'material ',1,'stresses')
# recorder('Node', '-file', f'{path1}/node{UpperrN_LQuarter}.out', '-time', '-node',UpperrN_LQuarter,'-dof',1,2,3,'vel')

# # ==== Right 1/4 node ======================================
# recorder('Element', '-file', f'{path2}/ele{UpperrE_RQuarter}.out', '-time', '-ele',UpperrE_RQuarter, 'material ',1,'stresses')
# recorder('Node', '-file', f'{path1}/node{UpperrN_RQuarter}.out', '-time', '-node',UpperrN_RQuarter,'-dof',1,2,3,'vel')

# ============= For Surface Load Output ===========================
Top_CenterLeft = UpperN_Center - int(1.0/Dw)
Top_CenterRight = UpperN_Center + int(1.0/Dw)
print(f'Top_CenterLeft Node = {Top_CenterLeft}; Top_CenterRight Node = {Top_CenterRight}')
# printModel('-node', Top_CenterLeft, Top_CenterRight)
recorder('Node', '-file', f'{path1}/node{Top_CenterLeft}.out', '-time', '-node',Top_CenterLeft,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'{path1}/node{Top_CenterRight}.out', '-time', '-node',Top_CenterRight,'-dof',1,2,3,'vel')
# printModel('-node', Top_CenterLeft, Top_CenterRight)

# # # # -------- Left Side Beam Node Vel/Stress --------------------------
# # # recorder('Node', '-file', f'Velocity/node{LSideBeamNode_Start}.out', '-time', '-node',LSideBeamNode_Start,'-dof',1,2,3,'vel')
# # # recorder('Node', '-file', f'Velocity/node{LSideBeamNode_Center}.out', '-time', '-node',LSideBeamNode_Center,'-dof',1,2,3,'vel')
# # # recorder('Node', '-file', f'Velocity/node{LSideBeamNode_End}.out', '-time', '-node',LSideBeamNode_End,'-dof',1,2,3,'vel')

# # # recorder('Element', '-file', f'Stress/ele{LSideBeam_Start}.out', '-time', '-ele',LSideBeam_Start, 'globalForce')
# # # recorder('Element', '-file', f'Stress/ele{LSideBeam_Center}.out', '-time', '-ele',LSideBeam_Center, 'globalForce')
# # # recorder('Element', '-file', f'Stress/ele{LSideBeam_End}.out', '-time', '-ele',LSideBeam_End, 'globalForce')
# # # # -------- Left Side Beam Center Node Vel/Stress --------------------------
# # # recorder('Node', '-file', f'Velocity/node{LSideBeam_CenterNodeStart}.out', '-time', '-node',LSideBeam_CenterNodeStart,'-dof',1,2,3,'vel')
# # # recorder('Node', '-file', f'Velocity/node{LSideBeam_CenterNode}.out', '-time', '-node',LSideBeam_CenterNode,'-dof',1,2,3,'vel')
# # # recorder('Node', '-file', f'Velocity/node{LSideBeamNode_CenterNodeEnd}.out', '-time', '-node',LSideBeamNode_CenterNodeEnd,'-dof',1,2,3,'vel')
# # # recorder('Node', '-file', f'Velocity/node{LSideBeam_CenterNodeStartplus}.out', '-time', '-node',LSideBeam_CenterNodeStartplus,'-dof',1,2,3,'vel')

# # # recorder('Node', '-file', f'Velocity/node{LSideNDash_Start}.out', '-time', '-node',LSideNDash_Start,'-dof',1,2,3,'vel')
# # # recorder('Node', '-file', f'Velocity/node{LSideNDash_CenterFree}.out', '-time', '-node',LSideNDash_CenterFree,'-dof',1,2,3,'vel')
# # # recorder('Node', '-file', f'Velocity/node{LSideNDash_EndFree}.out', '-time', '-node',LSideNDash_EndFree,'-dof',1,2,3,'vel')
# # # # --------Left Side dash free/fix Velocity ----------------
# # # recorder('Node', '-file', f'Velocity/node{LSideNDash_StartFix}.out', '-time', '-node',LSideNDash_StartFix,'-dof',1,2,3,'vel')
# # # recorder('Node', '-file', f'Velocity/node{LSideNDash_CenterFix}.out', '-time', '-node',LSideNDash_CenterFix,'-dof',1,2,3,'vel')
# # # recorder('Node', '-file', f'Velocity/node{LSideNDash_EndFix}.out', '-time', '-node',LSideNDash_EndFix,'-dof',1,2,3,'vel')

# # # # -------- Right Beam Node Velocity / Stress----------------
# # # recorder('Node', '-file', f'Velocity/node{RSideBeamNode_Start}.out', '-time', '-node',RSideBeamNode_Start,'-dof',1,2,3,'vel')
# # # recorder('Node', '-file', f'Velocity/node{RSideBeamNode_Center}.out', '-time', '-node',RSideBeamNode_Center,'-dof',1,2,3,'vel')
# # # recorder('Node', '-file', f'Velocity/node{RSideBeamNode_End}.out', '-time', '-node',RSideBeamNode_End,'-dof',1,2,3,'vel')

# # # recorder('Element', '-file', f'Stress/ele{RSideBeam_Start}.out', '-time', '-ele',RSideBeam_Start, 'globalForce')
# # # recorder('Element', '-file', f'Stress/ele{RSideBeam_Center}.out', '-time', '-ele',RSideBeam_Center, 'globalForce')
# # # recorder('Element', '-file', f'Stress/ele{RSideBeam_End}.out', '-time', '-ele',RSideBeam_End, 'globalForce')

# # # recorder('Node', '-file', f'Velocity/node{RSideBeamNode_Startplus}.out', '-time', '-node',RSideBeamNode_Startplus,'-dof',1,2,3,'vel')
# # # recorder('Node', '-file', f'Velocity/node{RSideBeamNode_Startplus2}.out', '-time', '-node',RSideBeamNode_Startplus2,'-dof',1,2,3,'vel')
# # # # -------- Right Beam Center Node Velocity----------------
# # # recorder('Node', '-file', f'Velocity/node{RSideNDash_Start}.out', '-time', '-node',RSideNDash_Start,'-dof',1,2,3,'vel')
# # # recorder('Node', '-file', f'Velocity/node{RSideNDash_CenterFree}.out', '-time', '-node',RSideNDash_CenterFree,'-dof',1,2,3,'vel')
# # # recorder('Node', '-file', f'Velocity/node{RSideNDash_EndFree}.out', '-time', '-node',RSideNDash_EndFree,'-dof',1,2,3,'vel')
# # # # --------Right Side dash free/fix Velocity ----------------
# # # recorder('Node', '-file', f'Velocity/node{RSideNDash_StartFix}.out', '-time', '-node',RSideNDash_StartFix,'-dof',1,2,3,'vel')
# # # recorder('Node', '-file', f'Velocity/node{RSideNDash_CenterFix}.out', '-time', '-node',RSideNDash_CenterFix,'-dof',1,2,3,'vel')
# # # recorder('Node', '-file', f'Velocity/node{RSideNDash_EndFix}.out', '-time', '-node',RSideNDash_EndFix,'-dof',1,2,3,'vel')
# #     # ============ recorder Mesh size Each Depth Node ===============================
# # for o in range(ny+1):
# # # ---------------- Left Side ------------
# #     Depth = yMesh*o 
# #     LeftNode = int(1 + (nx+1)*o)
# #     CenterNode = int((1 + (nx/2)) + (nx+1)*o)
# #     RightNode = int((1+nx)+ (nx+1)*o)
# #     # print(RightNode)

# #     recorder('Node', '-file', f'E:/unAnalysisFile/RayleighDashpot/{Boundary}/DepthTest/H{Applt_D}/Ca{akz}_Cb{bkz}/Velocity/D{Depth}_Lnode{LeftNode}.out', '-time', '-node',LeftNode,'-dof',1,2,3,'vel')
# #     recorder('Node', '-file', f'E:/unAnalysisFile/RayleighDashpot/{Boundary}/DepthTest/H{Applt_D}/Ca{akz}_Cb{bkz}/Velocity/D{Depth}_Cnode{CenterNode}.out', '-time', '-node',CenterNode,'-dof',1,2,3,'vel')
# #     recorder('Node', '-file', f'E:/unAnalysisFile/RayleighDashpot/{Boundary}/DepthTest/H{Applt_D}/Ca{akz}_Cb{bkz}/Velocity/D{Depth}_Rnode{RightNode}.out', '-time', '-node',RightNode,'-dof',1,2,3,'vel')
# # # --------------- Top X(m) Each Dw  -----------------------
# # topLeftNode = 1 + (nx+1)* (ny)
# # for width in range(nx+1):
# #     topNode = topLeftNode + width
# #     MeshWidth = 0.125*width

# #     recorder('Node', '-file', f'E:/unAnalysisFile/RayleighDashpot/{Boundary}/DepthTest/H{Applt_D}/Ca{akz}_Cb{bkz}/SurfaceVelocity/W{MeshWidth}node{topNode}.out', '-time', '-node',topNode,'-dof',1,2,3,'vel')
# #     # print(topNode)

system("UmfPack") 
numberer("RCM")
constraints("Transformation")

integrator("Newmark", 0.5, (1/6)) # NewMark, (Constant), 0.5, 0.25 / (Linear),  0.5, (1/6)
# integrator("HHT", (2/3)) # unconditionally stable when 2/3 <= alpha <= 1.0(NewMark),
# integrator("CentralDifference")

algorithm("Linear") # Newton For Intrgeator = "NewMark"/ "HHT"; Linear For Integrator = "CentralDifference"
test('EnergyIncr',1e-8, 200)
analysis("Transient")
analyze(int(analystep),dt)
# analyze(int(analystep),cpdt)
print("finish analyze:0 ~ 0.8s")

#  ================ Make Find Stiffnes and Mass Matrix (VFO_Version) =============================
# Path = f'D:/shiang/opensees/20220330/OpenSeesPy/2D_Absorb/{Choose_Wave}/W_{int(soilwidth)}m/HZ_{HZ}/LKDash_Surface_{ny}row'  #/{Scale}{Compare_For}
# Path = f'D:/shiang/opensees/20220330/OpenSeesPy/2D_Absorb/Newmark_Linear/Vertical/W_{int(soilwidth)}m/HZ_80/LKDash_Surface_40row'
# Nmodes = 20 
# lam = eigen(Nmodes) 

# mode = 1
# Scale = 10
# vfo.plot_modeshape(modenumber=mode, scale=Scale, filename=f'{Path}/ModeShape_{mode}_scale{Scale}3', line_width= 10)

# #  ================ Make Find Stiffnes and Mass Matrix (Opstool_Version) ============================= rainbow_r / tealgrn
# opsvis.set_plot_props(point_size=0, theme='gridon', line_width=5, cmap="rainbow_r",  mesh_edge_width=5) # plasma setting element enviroment
# fig = opsvis.plot_eigen(mode_tags=[12, 12], subplots=True, show_outline=False, style='surface', show_bc =False, show_origin=False) # mode_tags=[7, 7]
# fig.show()

# --------- end to calculate time -------------
end = time.time()
print(end - start)
