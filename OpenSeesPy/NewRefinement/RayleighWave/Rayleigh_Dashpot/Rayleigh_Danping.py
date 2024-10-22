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
pi = np.pi

Extend_Scale = 1# 100
# size = [1e-0, 1e-1, 1e-2, 1e-3, 1e-4] #1e-0, 1e-1, 1e-2, 1e-3, 1e-4
# # # time_Scale = 1e-4

Compare = f"Pwave/Beam_Side_Column/Beam_SideRayleigh" # 0.0001Scale
# Compare_For = f"_rho"
# for Scale in size:
#     print(f"scale = {Scale}")
wipe()
# -------- Start calculaate time -----------------
start = time.time()
print("The time used to execute this is given below")

model('basic', '-ndm', 2, '-ndf' , 2)
# ============= Real Element Elastic Modules =====================
cs = 200     ;# m/s 

nu = 0.3 #0.3
rho = 2000    # kg/m3 
G = rho*cs*cs
E = 2*(1+nu)*G# 208000000 # (N/m^2)= (kg*m/s2)*(1/m2) = kg/(s2*m) 

cp = (E*(1-nu)/(rho*(1+nu)*(1-2*nu)))**0.5
M = rho*cp*cp

print(f"Pwave Velocity = {cp}; E = {E}; M = {M}")

nDMaterial('ElasticIsotropic', 2000, E, nu, rho)

soilLength = 10 #m 10*Extend_Scale
soilwidth = 0.125   #1.0/ 0.125

nx = int(soilwidth/(0.125*Extend_Scale))# 
ny = 80 # 80
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
#     equalDOF((nx+1)*i+1,(nx+1)*i+(nx+1),1,2) # Normal
#     # print((nx+1)*i+1,(nx+1)*i+(nx+1),1,2)

endNode = (1+nx) + (nx+1)*ny
endEle = nx*ny
# print(f"endNode= {endNode}, endEle= {endEle}")

Dy = soilLength/ny # = yMesh Y row MeshSize
dcell = Dy / cp 
dt = 2e-5
print(f"yMesh = {Dy}; dcell = {dcell}; dt = {dt}")

widthMesh = soilwidth/nx
print(f"widthMesh = {widthMesh}")

# ================= Build Boundary File =====================H{Applt_D}t/Ca{akz}_Cb{bkz}/Stress
path1 = f'D:/shiang/opensees/20220330/OpenSeesPy/Column_Quad/{Compare}/Velocity' # /Velocity   {Scale}{Compare_For}
path2 = f'D:/shiang/opensees/20220330/OpenSeesPy/Column_Quad/{Compare}/Stress' # /Stress   /{Scale}{Compare_For}

if not os.path.isdir(path1):
    os.makedirs(path1)
if not os.path.isdir(path2):
    os.makedirs(path2)
# # if not os.path.isdir(path3):
# #     os.makedirs(path3)

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
# print(f"LowerN_LQuarter = {LowerN_LQuarter} ,UpperrN_LQuarter = {UpperrN_LQuarter}")
LowerE_LQuarter = int((nx/4)+1)
UpperrE_LQuarter = int(LowerE_LQuarter + (ny-1)* nx)
# print(f"LowerE_LQuarter = {LowerE_LQuarter} ,UpperrE_LQuarter = {UpperrE_LQuarter}")

# -------- Quarter(3/4) Node ------------------------
LowerN_RQuarter = int((3*nx/4)+1)
UpperrN_RQuarter = int(LowerN_RQuarter + (nx+1)* ny)
# print(f"LowerN_RQuarter = {LowerN_RQuarter} ,UpperrN_RQuarter = {UpperrN_RQuarter}")
LowerE_RQuarter = int((3*nx/4)+1)
UpperrE_RQuarter = int(LowerE_RQuarter + (ny-1)* nx)
# print(f"LowerE_RQuarter = {LowerE_RQuarter} ,UpperrE_RQuarter = {UpperrE_RQuarter}")

# ============= Virtual Element Elastic Modules (E' control by M or G) =====================
nu2 = 0.0
Scale = 1e-4 # Control Size  (1/10000) 
E_G = Scale*E
M_G = Scale* E # = E_G young's Module Control by G (S wave Velocity) # (N/m^2)= (kg*m/s2)*(1/m2) = kg/(s2*m) 
G_ = M_G/2

rho2 =  Scale*rho   # kg/m3 Scale
nDMaterial('ElasticIsotropic', 2006, E_G, nu2, rho2)

Vp_Ghost = (E_G/(rho2))**0.5
Dy_Ghost = 0.125 # Vp_Ghost* (Dy/cp) # Ghost_yMesh 0.125
print(f"Vp_Ghost = {Vp_Ghost} ; Ghost_yMesh = {Dy_Ghost}")

# ============== Apply Bottom virtual Quad element to apply Rayleigh Dashpot =======================
BotNode = endNode+ 1 
BotEle = endEle + 1
print(f"BotNode = {BotNode}; BotEle = {BotEle}")
for i in range(nx+1):
    node(BotNode+i, widthMesh*i, -Dy_Ghost*Extend_Scale)
    fix(BotNode+i, 1 ,1) # like LK Dashpot have the fix end to get reaction Rayleigh Force
    # print(BotNode+i, widthMesh*i, -Dy_Ghost*Extend_Scale)

# --------------- Apply Bot Virtual Quad element ----------------------------------------------
for k in range(nx):
    element('quad', BotEle+k, BotNode+k, (BotNode+1)+k, (n1+1)+k,  n1+k, 1, 'PlaneStrain', 2006) # PlaneStrain
    # print(BotEle+k, BotNode+k, (BotNode+1)+k, (n1+1)+k,  n1+k, 1, 'PlaneStrain', 2006)

# =============Apply Left and Right virtual Quad element to apply Rayleigh Dashpot =======================
LeftNode =  BotNode+ nx + 1  #BotNode+ nx + 1
RightNode = LeftNode + ny + 1

LeftEle = BotEle + nx # BotEle + nx
RightEle = LeftEle + ny
print(f"LeftNode = {LeftNode}; LeftEle = {LeftEle}; RightNode = {RightNode}; RightEle = {RightEle}")

for i in range(ny+1):
    node(LeftNode+i, -Dy_Ghost, Dy*i)
    node(RightNode+i, soilwidth+Dy_Ghost, Dy*i)
    
    fix(LeftNode+i, 1, 1)
    fix(RightNode+i, 1, 1)
    # print(RightNode+i, soilwidth+Dy_Ghost, Dy*i)

for k in range(ny):
# # --------- no Change quad direction ----------
#     element('quad', LeftEle+k, LeftNode+k, n1+(n1+nx)*k, (n1+(n1+nx))+(n1+nx)*k,  (LeftNode+1)+k, 1, 'PlaneStrain', 2006)
#     element('quad', RightEle+k, (n1+nx)+ (n1+nx)*k, RightNode+k, (RightNode+1)+k, (n1+nx)*2+ (n1+nx)*k, 1, 'PlaneStrain', 2006)
    # print(RightEle+k, (n1+nx)+ (n1+nx)*k, RightNode+k, (RightNode+1)+k, (n1+nx)*2+ (n1+nx)*k)
# ---------  Change quad direction ----------
    element('quad', LeftEle+k, (LeftNode+1)+k, LeftNode+k, n1+(n1+nx)*k, (n1+(n1+nx))+(n1+nx)*k, 1, 'PlaneStrain', 2006)
    element('quad', RightEle+k, RightNode+k, (RightNode+1)+k, (n1+nx)*2+ (n1+nx)*k, (n1+nx)+ (n1+nx)*k, 1, 'PlaneStrain', 2006)
    # print(RightEle+k, RightNode+k, (RightNode+1)+k, (n1+nx)*2+ (n1+nx)*k, (n1+nx)+ (n1+nx)*k)

# #  ================ Make Find Stiffnes and Mass Matrix =============================
# Path = f"Column_Quad/{Compare}" #/{Scale}{Compare_For}
# wipeAnalysis()
# system('FullGeneral')
# analysis('Transient')

# # Mass
# integrator('GimmeMCK',1.0,0.0,0.0) 
# analyze(1,0.0)

# # Number of equations in the model
# N = systemSize() # Has to be done after analyze

# MASS = printA('-file', f'{Path}/M.out') #, '-ret' / Or use ops.printA('-file','M.out')

# # Stiffness
# integrator('GimmeMCK',0.0,0.0,1.0)
# analyze(1,0.0)
# K_Stiffness = printA('-file',f'{Path}/K.out') # ,'-ret'
# # K = np.array(K)
# # K.shape = (N,N)
# # print(K)

# # Nmodes = 162-1
# # # lam = eigen('-standard','-symmBandLapack',Nmodes) # With no considered Mass matrix
# # lam = eigen(Nmodes) # Full Generalize Eigen 
# # print('Computed eigenvalues:',lam)
# # omega = np.zeros(len(lam))
# # for i in range(len(lam)):
# #     omega[i] =(lam[i]**0.5)

# # Tperiod = np.zeros(len(omega))
# # for j in range(len(omega)):
# #     Tperiod[j] = (2*pi)/omega[j]

# # np.savetxt(r'Tperiod.txt',Tperiod, delimiter = " ")
# # print(f"Tperiod = {Tperiod}")

# # print('Eigenvector 1')
# # print(nodeEigenvector(1,1), nodeEigenvector(2,1))

# # print('Eigenvector 2')
# # print(nodeEigenvector(1,2), nodeEigenvector(2,2))

# modalProperties('-print', '-file', f'{Path}/ModalReport.txt', '-unorm')

# =========== Bottom Beam element ===================
# # --------- Bot Virtual quad -----------
# BeamNode_Start = BotNode + (nx+1) 
# BeamEle_Start = BotEle + nx
# ---------- With Side Virtual quad --------------
BeamNode_Start = RightNode + ny +1
BeamEle_Start = RightEle + ny
# # ----------- LK Dashpot ------------------------
# BeamNode_Start = endNode +1
# BeamEle_Start = endEle + 1
# print(f"BeamNode_Start = {BeamNode_Start}; BeamEle_Start = {BeamEle_Start}")

model('basic', '-ndm', 2, '-ndf' , 3)
for j in range(nx+1):
    node(BeamNode_Start+j, widthMesh*j,0.0)
    mass(BeamNode_Start+j,1,1,1)
# -------- fix rotate dof ------------
    fix(BeamNode_Start+j,0,0,1)
    # print(BeamNode_Start+j, widthMesh*j,0.0)

# ------------- Beam parameter -----------------
A =  0.1*1 # 0.1*0.1
E1 = 1e-06 ;#1e-06
Iz = (0.1*0.1*0.1)/12 # (0.125*0.1*0.1)/12
geomTransf('Linear', 1)

for k in range(nx):
    element('elasticBeamColumn', BeamEle_Start+k, BeamNode_Start+k, BeamNode_Start+1+k, A,E1,Iz, 1, '-release', 3)
    # print(BeamEle_Start+k, BeamNode_Start+k, BeamNode_Start+1+k)
# =========== connect bot beam and soil element =========================
for k in range(nx+1):
    equalDOF(n1+k,BeamNode_Start+k,1,2)

# # ============= Bottom LK Dashpot element Dashpot ==========================
# BotTDash_Start = BeamNode_Start + (nx+1) # BeamNode_Start + (nx+1) / endNode + 1
# BotNDash_Start = BotTDash_Start + 2*(nx+1)
# print(f'BotTDash_Start= {BotTDash_Start}; BotNDash_Start={BotNDash_Start}')

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
# B_Smp = 0.5*rho*cp*sizeX      # lower Left and Right corner node dashpot :N (newton)
# B_Sms = 0.5*rho*cs*sizeX      # lower Left and Right corner node dashpot :N (newton)

# B_Cmp = 1.0*rho*cp*sizeX      # Bottom Center node dashpot :N (newton)
# B_Cms = 1.0*rho*cs*sizeX      # Bottom Center node dashpot :N (newton)

# uniaxialMaterial('Viscous',4000, B_Smp, 1)    # P wave: Side node
# uniaxialMaterial('Viscous',4001, B_Sms, 1)    # S wave: Side node

# uniaxialMaterial('Viscous',4002, B_Cmp, 1)    # P wave: Center node
# uniaxialMaterial('Viscous',4003, B_Cms, 1)    # S wave: Center node

# #----------- dashpot elements: Vs with x dir / Vp with y-dir------------------
# xdir = 1
# ydir = 2
# # ------ Traction dashpot element: Vs with x dir
# BotTEle_Start = BeamEle_Start + nx # BeamEle_Start + nx / endEle + 1
# BotTEle_End = BotTEle_Start + nx
# # print(BotTEle_Start, BotTEle_End)
# element('zeroLength',BotTEle_Start,(BotTDash_Start+1), BotTDash_Start, '-mat',4001,'-dir',xdir)  # node 1: Left side 4003 / 4001
# element('zeroLength',BotTEle_End,(BotTDash_Start+1)+2*nx, BotTDash_Start+2*nx, '-mat',4001,'-dir',xdir)  # node 1: Left side

# # for m in range(1,nx): # nx+1
# #     element('zeroLength',BotTEle_Start+m,(BotTDash_Start+1)+2*m,BotTDash_Start+2*m, '-mat',4003,'-dir',xdir)  # node 1: Left side
# #     # print(BotTEle_Start+m,(BotTDash_Start+1)+2*m,BotTDash_Start+2*m)
# # ------ Normal dashpot element: Vp with y dir (98~106)
# BotNEle_Start = BotTEle_End+1
# BotNEle_End = BotNEle_Start+nx
# # print(BotNEle_Start, BotNEle_End)
# element('zeroLength',BotNEle_Start,(BotNDash_Start+1), BotNDash_Start, '-mat',4000,'-dir',ydir) # 4002 / 4000
# element('zeroLength',BotNEle_End,(BotNDash_Start+1)+2*nx, BotNDash_Start+2*nx, '-mat',4000,'-dir',ydir)

# # for m in range(1,nx): # nx+1
# #     element('zeroLength',BotNEle_Start+m,(BotNDash_Start+1)+2*m,BotNDash_Start+2*m, '-mat',4002,'-dir',ydir)  # node 1: Left side

# # ============== Soil Left and Right "Side" Dashpot =====================================
# LSideNDash_Start =  BotNDash_Start + 2*(nx+1)
# LSideTDash_Start =  LSideNDash_Start + 2*(ny+1)
# print(f"LSideNDash_Start = {LSideNDash_Start}, LSideTDash_Start = {LSideTDash_Start}")
# RSideNDash_Start =  LSideTDash_Start + 2*(ny+1)
# RSideTDash_Start =  RSideNDash_Start + 2*(ny+1)
# print(f"RSideNDash_Start = {RSideNDash_Start}, RSideTDash_Start = {RSideTDash_Start}")
# for l in range(ny+1):
# # ========= Left Side =============
# # --------- Normal dashpot (node 145,146~ 165,166)-> for S wave------------
#     node(LSideNDash_Start+2*l, 0.0, Dy*l)
#     node((LSideNDash_Start+1)+2*l, 0.0, Dy*l)
# # ---------- dashpot dir: Vs -> x dir ---------------------     
#     fix(LSideNDash_Start+2*l, 0, 1, 1)      # x dir dashpot　
#     fix((LSideNDash_Start+1)+2*l, 1, 1, 1)      # fixed end to let soil fix

# # --------- Traction dashpot (node 167,168~ 187,188)-> for P wave------------
#     node(LSideTDash_Start+2*l, 0.0, Dy*l)
#     node((LSideTDash_Start+1)+2*l, 0.0, Dy*l)
# # ---------- dashpot dir: Vp -> y dir ---------------------     
#     fix(LSideTDash_Start+2*l, 1, 0, 1)      # y dir dashpot　
#     fix((LSideTDash_Start+1)+2*l, 1, 1, 1)      # fixed end to let soil fix

# # ========= Right Side =============
# # --------- Normal dashpot (node 189,190~ 209,210)-> for S wave------------
#     node(RSideNDash_Start+2*l, soilwidth, Dy*l)
#     node((RSideNDash_Start+1)+2*l, soilwidth, Dy*l)
# # ---------- dashpot dir: Vs -> x dir ---------------------     
#     fix(RSideNDash_Start+2*l, 0, 1, 1)      # x dir dashpot　
#     fix((RSideNDash_Start+1)+2*l, 1, 1, 1)      # fixed end to let soil fix

# # --------- Traction dashpot (node 211,212~ 231,232)-> for P wave------------
#     node(RSideTDash_Start+2*l, soilwidth, Dy*l)
#     node((RSideTDash_Start+1)+2*l, soilwidth, Dy*l)
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
# # print("Finished creating all Side dashpot boundary conditions and equalDOF...")
    
# # ------------- Side dashpot material -----------------------
# sizeX1 = Dy
# S_Smp = 0.5*rho*cp*sizeX1    # side Normal dashpot for S wave   ; lower/Upper  Left and Right corner node
# S_Sms = 0.5*rho*cs*sizeX1    # side Traction dashpot for P wave ; lower/Upper Left and Right corner node

# S_Cmp = 1.0*rho*cp*sizeX1    # side Normal dashpot for S wave: Netwon
# S_Cms = 1.0*rho*cs*sizeX1    # side Traction dashpot for P wave: Netwon

# uniaxialMaterial('Viscous',4004, S_Smp, 1)    # "S" wave: Side node
# uniaxialMaterial('Viscous',4005, S_Sms, 1)    # "P" wave: Side node

# uniaxialMaterial('Viscous',4006, S_Cmp, 1)    # "S" wave: Center node
# uniaxialMaterial('Viscous',4007, S_Cms, 1)    # "P" wave: Center node

# # # =============== Right and Left NODE :different dashpot element==================
# LsideNEle_Start = BotNEle_End + 1
# LsideNEle_End = LsideNEle_Start + ny
# print(f"LsideNEle_Start = {LsideNEle_Start}, LsideNEle_End = {LsideNEle_End}")
# #  ----------- Left side Normal: S wave ----------
# element('zeroLength',LsideNEle_Start, (LSideNDash_Start+1), LSideNDash_Start, '-mat',4004,'-dir',xdir)  # lower Left node: -> Smp
# element('zeroLength',LsideNEle_End, (LSideNDash_Start+1)+2*ny, LSideNDash_Start+2*ny, '-mat',4004,'-dir',xdir)  # Upper left node: -> Smp

# LsideTEle_Start = LsideNEle_End + 1
# LsideTEle_End = LsideTEle_Start + ny
# print(f"LsideTEle_Start = {LsideTEle_Start}, LsideTEle_End = {LsideTEle_End}")

# #  ----------- Left side Traction: P wave ----------
# element('zeroLength',LsideTEle_Start, (LSideTDash_Start+1), LSideTDash_Start, '-mat',4005,'-dir',ydir)  # lower Left node: -> Sms
# element('zeroLength',LsideTEle_End, (LSideTDash_Start+1)+2*ny, LSideTDash_Start+2*ny, '-mat',4005,'-dir',ydir)  # Upper left node -> Sms

# RsideNEle_Start = LsideTEle_End + 1
# RsideNEle_End = RsideNEle_Start + ny
# print(f"RsideNEle_Start = {RsideNEle_Start}, RsideNEle_End = {RsideNEle_End}")
# #  ----------- Right side Normal: S wave ----------
# element('zeroLength',RsideNEle_Start, (RSideNDash_Start+1), RSideNDash_Start, '-mat',4004,'-dir',xdir)  # lower Right node: -> Smp
# element('zeroLength',RsideNEle_End, (RSideNDash_Start+1)+2*ny, RSideNDash_Start+2*ny, '-mat',4004,'-dir',xdir)   # Upper Right node: -> Smp

# RsideTEle_Start = RsideNEle_End + 1
# RsideTEle_End = RsideTEle_Start + ny
# print(f"RsideTEle_Start = {RsideTEle_Start}, RsideTEle_End = {RsideTEle_End}")
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
    
# ================== Apply Rayleigh Dashpot ============================= 
# ------------Bottom Rayleigh Damping： Only Account for Ghost ELement to Calculate a0, a1 ---------------------------------
alphaM1 = (2/Dy_Ghost)*(rho/rho2)*(-cp + 2*cs) 
betaK1 =  (2*Dy_Ghost)*(1/E_G)*rho*(cp-cs)
betaKinit = 0.0
betaKcomm = 0.0
print(f"alphaM = {alphaM1}; betaK = {betaK1}")

Ray_Scale = 1.0
# --------------------- one Quad element Bot Rayleigh Damping --------------------------------------------
# region(10000, '-ele ', BotEle ,'-rayleigh',alphaM, betaK, betaKinit,betaKcomm)

Bot_StartEle = BotEle
Bot_EndEle = BotEle + nx-1
print(f"Bot_StartEle = {Bot_StartEle}; Bot_EndEle = {Bot_EndEle}")
# # ---------------Bot Corner Element  (Use in Harmonic TimeSeries)------------------
# region(10000, '-ele ', Bot_StartEle, Bot_EndEle,'-rayleigh',alphaM1*Ray_Scale, betaK1*Ray_Scale, betaKinit,betaKcomm) 
# region(10001, '-eleRange ', Bot_StartEle+1, Bot_EndEle-1,'-rayleigh',alphaM1, betaK1, betaKinit,betaKcomm) 

# --------------- Bot Element Total (Use in Constant TimeSeries)------------------
region(10000, '-eleRange ', BotEle, BotEle+nx-1,'-rayleigh',alphaM1, betaK1, betaKinit,betaKcomm) 

# ----------- Left Side Rayleigh Damping ----------------------------
alphaM_LR = (2/(rho2*Dy_Ghost))* (-(rho*cs) + 2*(rho*cp))  # (2/Dy_Ghost)*(rho/rho2)*(-cp + 2*cs) / (2/(rho2*Dy_Ghost))* (-(rho*cs) + 2*(rho*cp))
betaK_LR =  (Dy_Ghost/(G_ - M_G))*((rho*cp) - (rho*cs))  #(2*Dy_Ghost)*(1/E_G)*rho*(cp-cs)  / (Dy_Ghost/(G_ - M_G))*((rho*cp) - (rho*cs))
print(f"alphaM_L = {alphaM_LR}; betaK_L = {betaK_LR}")

# --------------- Left / Right Rayleigh Damping C = alphaM * M + betaK * K ---------------------------
# # --------- Center and Corner element seperete (Use in Harmonic TimeSeries) ------------
# Left_StartEle = LeftEle
# Left_EndEle = LeftEle + ny-1
# print(f"Left_StartEle = {Left_StartEle}; Left_EndEle = {Left_EndEle}")

# Right_StartEle = RightEle
# Right_EndEle = RightEle + ny-1
# print(f"Right_StartEle = {Right_StartEle}; Right_EndEle = {Right_EndEle}")

# region(10002, '-ele', Left_StartEle, Left_EndEle,'-rayleigh', alphaM1*Ray_Scale, betaK1*Ray_Scale, betaKinit,betaKcomm) 
# region(10003, '-eleRange ', Left_StartEle+1, Left_EndEle-1,'-rayleigh', alphaM1, betaK1, betaKinit,betaKcomm) 

# region(10004, '-ele', Right_StartEle, Right_EndEle,'-rayleigh',alphaM1*Ray_Scale, betaK1*Ray_Scale, betaKinit,betaKcomm) 
# region(10005, '-eleRange ', Right_StartEle+1, Right_EndEle-1,'-rayleigh',alphaM1, betaK1, betaKinit,betaKcomm) 

# --------- Total element seperete (Use in Constant TimeSeries)------------
region(10001, '-eleRange ', LeftEle, LeftEle+ny-1,'-rayleigh', alphaM1, betaK1, betaKinit,betaKcomm) 
region(10002, '-eleRange ', RightEle, RightEle+ny-1,'-rayleigh', alphaM1, betaK1, betaKinit,betaKcomm) 

# ================ NewBC: for Case A/B============================
# ====================Bulild Side Beam node (233~243 / 244~254) ====================
# ----------Rayleigh Dashpot -----------------
LsideNode = BeamNode_Start + nx+1
RsideNode = LsideNode + (ny+1)
LsideEle = BeamEle_Start + nx 
RsideEle = LsideEle + ny
# # ----LK Dashpot ------------
# LsideNode = RSideTDash_Start + 2*(ny+1)
# RsideNode = LsideNode + (ny+1)
# LsideEle = RsideTEle_End + 1
# RsideEle = LsideEle + ny
print(f"Lside_BeamNode = {LsideNode}, Lside_BeamEle= {LsideEle}")
print(f"Rside_BeamNode = {RsideNode}, Rside_BeamEle= {RsideEle}")

for i in range(ny+1):
# ----- Left Side: 233~243 -----------------
    node(LsideNode+i, 0.0, Dy*i)
    fix(LsideNode+i,0,0,1)
# ----- Right Side: 244~254 -----------------
    node(RsideNode+i, soilwidth ,Dy*i)
    fix(RsideNode+i,0,0,1)
    # print(RsideNode+i, soilwidth ,Dy*i)

# ------------  Beam Element: 151 ~ 160 / 161 ~ 170 ------------------
for j in range(ny):
# ----- Left Side Beam:151 ~ 160 -----------------
    element('elasticBeamColumn', LsideEle+j, LsideNode+j, (LsideNode+1)+j, A,E1,Iz, 1, '-release', 3)
# ----- Right Side Beam:161 ~ 170 -----------------
    element('elasticBeamColumn', RsideEle+j, RsideNode+j, (RsideNode+1)+j, A,E1,Iz, 1, '-release', 3)
    # print(RsideEle+j, RsideNode+j, (RsideNode+1)+j)
# --------- Side Beam and Soil BC -----------------
for j in range(ny+1):
    equalDOF(1+(nx+1)*j,LsideNode+j,1,2)
    equalDOF((nx+1)+(nx+1)*j,RsideNode+j,1,2)
    # print((nx+1)+(nx+1)*j,RsideNode+j)

# #  ============================== S wave ======================================
# # ========================= "CaseA": SideLoad Pattern ===================================
# # ------------ Side Load Pattern ------------------------------
# xTimeSeriesID = 800
# xPatternID = 804

# coff = 1 # (Vs/Vp) (origin) / (Vp/Vs) (later) / 1 (new)

# for g in range(ny):
# # ------- timeSeries ID: 800~809 / Pattern ID: 804~813----------------------Ray_S_Sideforce_80rowx_Const / PSideforce_80rowx
#     timeSeries('Path',xTimeSeriesID+g, '-filePath',f'Ray_P_Sideforce_80rowx_Const/ele{1+g}.txt','-dt', 3.34e-05)#cs_dt = 6.25e-05 /cp_dt = 3.34e-05 # f'SSideforce_{ny}rowx/ele{1+g}.txt'
#     pattern('Plain',xPatternID+g, xTimeSeriesID+g)
# # ---------- x direction : Sideforce ---------------------
# # ---------- Distributed at Left Side Beam ----------------------
#     eleLoad('-ele',LsideEle+g, '-type', '-beamUniform', -20*coff,0)  # for local axes Wy -    -20*coff
# # ---------- Distributed at Right Side Beam ----------------------
#     eleLoad('-ele',RsideEle+g, '-type', '-beamUniform', +20*coff,0)   # for local axes Wy +

# yTimeSeriesID = xTimeSeriesID + ny
# yPatternID  = xPatternID + ny

# for g in range(ny):
# # ------- timeSeries ID: 810~819 / Pattern ID:814~823 ----------------------Ray_S_Sideforce_80rowy_Const / PSideforce_80rowy
# # ---------- y direction : Sideforce --------------------
#     timeSeries('Path',yTimeSeriesID+g, '-filePath',f'Ray_P_Sideforce_80rowy_Const/ele{1+g}.txt','-dt', 3.34e-05) # f'SSideforce_{ny}rowy/ele{1+g}.txt'
#     pattern('Plain',yPatternID+g, yTimeSeriesID+g)
# # ---------- For P wave : y direction ---------------------
# # ---------- Distributed at Left Side Beam ----------------------
#     eleLoad('-ele',LsideEle+g, '-type', '-beamUniform',0,+20,0)  # for local axes Wx +
# # ---------- Distributed at Right Side Beam ----------------------
#     eleLoad('-ele',RsideEle+g, '-type', '-beamUniform',0,+20,0)   # for local axes Wx -

# # ========================= "Case B": Side Node Dashpot (Only Nodal Force at Left and Right side) ===================================
# # ------------ Side Nodal Load Pattern ------------------------------
# xTimeSeriesID = 800
# xPatternID = 804
# P0 = 20
# timeSeries('Path',xTimeSeriesID, '-filePath',f'Ray_P_Nodeforce_80rowx_Const/node{1}.txt','-dt',3.34e-05) #cs_dt = 6.25e-05 /cp_dt = 3.34e-05
# pattern('Plain',xPatternID, xTimeSeriesID)
# # ---- NodeForce at Left Side Corner -----
# load(LsideNode, P0*Dy*0.5 ,0 ,0) # LsideNode
# # ---- NodeForce at Right Side Corner -----
# load(RsideNode, -P0*Dy*0.5 ,0 ,0) # RsideNode

# # # ---- NodeForce at Left Side Corner -----
# # load(LsideNode, P0*Dy*0.5,0 ) # 10,0,0
# # # ---- NodeForce at Right Side Corner -----
# # load(RsideNode, P0*Dy*0.5,0 )
# # print(LsideNode,RsideNode, f'S_Nodeforce_{ny}rowx/node{1}.txt')

# timeSeries('Path',xTimeSeriesID+ny, '-filePath',f'Ray_P_Nodeforce_80rowx_Const/node{ny+1}.txt','-dt',3.34e-05) #cs_dt = 6.25e-05 /cp_dt = 3.34e-05
# pattern('Plain',xPatternID+ny, xTimeSeriesID+ny)
# # ---- NodeForce at Left Side Corner -----
# load(LsideNode+ny, P0*Dy*0.5 ,0 ,0) # LsideNode+ny
# # ---- NodeForce at Right Side Corner -----
# load(RsideNode+ny, -P0*Dy*0.5 ,0 ,0) # RsideNode+ny

# # # ---- NodeForce at Left Side Corner -----
# # load(LsideNode+2*ny, P0*yMesh*0.5,0) # LsideNode+ny
# # # ---- NodeForce at Right Side Corner -----
# # load(RsideNode+2*ny, P0*yMesh*0.5,0) # RsideNode+ny
# # # print(LsideNode+ny,RsideNode+ny,f'S_Nodeforce_{ny}rowx/node{ny+1}.txt')

# for g in range(1,ny):
# # ------- timeSeries ID: 800~810 / Pattern ID: 804~814----------------------
#     timeSeries('Path',xTimeSeriesID+g, '-filePath',f'Ray_P_Nodeforce_80rowx_Const/node{1+g}.txt','-dt', 3.34e-05)
#     pattern('Plain',xPatternID+g, xTimeSeriesID+g)
# # ---------- x direction : Sideforce ---------------------
# # ---------- NodeForce at Left Side Beam ----------------------
#     load(LsideNode+g, P0*Dy*0.5*2.0 ,0 ,0) # LsideNode+g
# # ---------- NodeForce at Right Side Beam ----------------------
#     load(RsideNode+g, -P0*Dy*0.5*2.0 ,0 ,0) # RsideNode+g

# #     # ---------- x direction : Sideforce ---------------------
# # # ---------- NodeForce at Left Side Beam ----------------------
# #     load(LsideNode+2*g, P0*yMesh*0.5*2.0,0) # LsideNode+g
# # # ---------- NodeForce at Right Side Beam ----------------------
# #     load(RsideNode+2*g, P0*yMesh*0.5*2.0,0) # RsideNode+g
#     # print(LsideNode+g, RsideNode+g,f'S_Nodeforce_{ny}rowx/node{1+g}')
# print("Nodalforce= ", 20*Dy*0.5, 20*Dy*0.5*2 )

# # ------------------ SideForce Nodal Load: Py ---------------------------------
# yTimeSeriesID = xTimeSeriesID + (ny+1)
# yPatternID  = xPatternID + (ny+1)

# timeSeries('Path',yTimeSeriesID, '-filePath',f'Ray_P_Nodeforce_80rowy_Const/node{1}.txt','-dt',3.34e-05) #cs_dt = 6.25e-05 /cp_dt = 3.34e-05
# pattern('Plain',yPatternID, yTimeSeriesID)
# # ---- NodeForce at Left Side Corner -----
# load(LsideNode, 0, +P0*Dy*0.5 ,0) # LsideNode
# # ---- NodeForce at Right Side Corner -----
# load(RsideNode, 0, +P0*Dy*0.5 ,0) # RsideNode

# # # ---- NodeForce at Left Side Corner -----
# # load(LsideNode, 0, +P0*yMesh*0.5) # 10,0,0
# # # ---- NodeForce at Right Side Corner -----
# # load(RsideNode, 0, -P0*yMesh*0.5)
# # print(LsideNode,RsideNode, f'S_Nodeforce_{ny}rowy/node{1}.txt')

# timeSeries('Path',yTimeSeriesID+ny, '-filePath',f'Ray_P_Nodeforce_80rowy_Const/node{ny+1}.txt','-dt',3.34e-05) #cs_dt = 6.25e-05 /cp_dt = 3.34e-05
# pattern('Plain',yPatternID+ny, yTimeSeriesID+ny)
# # ---- NodeForce at Left Side Corner -----
# load(LsideNode+ny, 0, +P0*Dy*0.5 ,0) # LsideNode+ny
# # ---- NodeForce at Right Side Corner -----
# load(RsideNode+ny, 0, +P0*Dy*0.5 ,0) # RsideNode+ny

# # # ---- NodeForce at Left Side Corner -----
# # load(LsideNode+2*ny, 0, +P0*yMesh*0.5) # LsideNode+ny
# # # ---- NodeForce at Right Side Corner -----
# # load(RsideNode+2*ny, 0, -P0*yMesh*0.5) # RsideNode+ny
# # print(LsideNode+ny,RsideNode+ny,f'S_Nodeforce_{ny}rowy/node{ny+1}.txt')

# for g in range(1,ny):
# # ------- timeSeries ID: 800~810 / Pattern ID: 804~814----------------------
#     timeSeries('Path',yTimeSeriesID+g, '-filePath',f'Ray_P_Nodeforce_80rowy_Const/node{1+g}.txt','-dt', 3.34e-05) #cs_dt = 6.25e-05 /cp_dt = 3.34e-05
#     pattern('Plain',yPatternID+g, yTimeSeriesID+g)
# # ---------- x direction : Sideforce ---------------------
# # ---------- NodeForce at Left Side Beam ----------------------
#     load(LsideNode+g, 0, +P0*Dy*0.5*2.0 ,0) # LsideNode+g
# # ---------- NodeForce at Right Side Beam ----------------------
#     load(RsideNode+g, 0, +P0*Dy*0.5*2.0 ,0) # RsideNode+g

# #     # ---------- x direction : Sideforce ---------------------
# # # ---------- NodeForce at Left Side Beam ----------------------
# #     load(LsideNode+2*g, 0, +P0*yMesh*0.5*2.0)
# # # ---------- NodeForce at Right Side Beam ----------------------
# #     load(RsideNode+2*g, 0, -P0*yMesh*0.5*2.0)
#     # print(LsideNode+g, RsideNode+g,f'S_Nodeforce_{ny}rowy/node{1+g}')

# # # =========== "Case C": Side Beam + Node Dashpot (Beam Distributed + Nodal Force at Left and Right side) ===================================
# # # ------------ Side Load Pattern-X direction ------------------------------
# # xTimeSeriesID = 800
# # xPatternID = 804
# # coff = 1 # (Vs/Vp) (origin) / (Vp/Vs) (later) / 1 (new)

# # for g in range(ny):
# # # ------- timeSeries ID: 800~809 / Pattern ID: 804~813----------------------
# #     timeSeries('Path',xTimeSeriesID+g, '-filePath',f'Ray_P_Sideforce_80rowx_Const/ele{1+g}.txt','-dt', 3.34e-05)#cs_dt = 6.25e-05 /cp_dt = 3.34e-05 # f'SSideforce_{ny}rowx/ele{1+g}.txt'
# #     pattern('Plain',xPatternID+g, xTimeSeriesID+g)
# # # ---------- x direction : Sideforce ---------------------
# # # ---------- Distributed at Left Side Beam ----------------------
# #     eleLoad('-ele',LsideEle+g, '-type', '-beamUniform', -20*coff,0)  # for local axes Wy -    -20*coff
# # # ---------- Distributed at Right Side Beam ----------------------
# #     eleLoad('-ele',RsideEle+g, '-type', '-beamUniform', +20*coff,0)   # for local axes Wy +

# # # # ------------------ SideForce Nodal Load: Py ---------------------------------
# # yTimeSeriesID = xTimeSeriesID + ny
# # yPatternID  = xPatternID + ny
# # P0 = 20

# # timeSeries('Path',yTimeSeriesID, '-filePath',f'Ray_P_Nodeforce_80rowy_Const/node{1}.txt','-dt',3.34e-05) #cs_dt = 6.25e-05 /cp_dt = 3.34e-05
# # pattern('Plain',yPatternID, yTimeSeriesID)
# # # ---- NodeForce at Left Side Corner -----
# # load(LsideNode, 0, +P0*Dy*0.5 ,0) # 10,0,0
# # # ---- NodeForce at Right Side Corner -----
# # load(RsideNode, 0, +P0*Dy*0.5 ,0)
# # # print(LsideNode,RsideNode, f'S_Nodeforce_{ny}rowy/node{1}.txt')

# # timeSeries('Path',yTimeSeriesID+ny, '-filePath',f'Ray_P_Nodeforce_80rowy_Const/node{ny+1}.txt','-dt',3.34e-05) #cs_dt = 6.25e-05 /cp_dt = 3.34e-05
# # pattern('Plain',yPatternID+ny, yTimeSeriesID+ny)
# # # ---- NodeForce at Left Side Corner -----
# # load(LsideNode+ny, 0, +P0*Dy*0.5 ,0) # LsideNode+ny
# # # ---- NodeForce at Right Side Corner -----
# # load(RsideNode+ny, 0, +P0*Dy*0.5 ,0) # RsideNode+ny
# # # print(LsideNode+ny,RsideNode+ny,f'S_Nodeforce_{ny}rowy/node{ny+1}.txt')

# # for g in range(1,ny):
# # # ------- timeSeries ID: 800~810 / Pattern ID: 804~814----------------------
# #     timeSeries('Path',yTimeSeriesID+g, '-filePath',f'Ray_P_Nodeforce_80rowy_Const/node{1+g}.txt','-dt', 3.34e-05) #cs_dt = 6.25e-05 /cp_dt = 3.34e-05
# #     pattern('Plain',yPatternID+g, yTimeSeriesID+g)
# # # ---------- x direction : Sideforce ---------------------
# # # ---------- NodeForce at Left Side Beam ----------------------
# #     load(LsideNode+g, 0, +P0*Dy*0.5*2.0,0) # LsideNode+g
# # # ---------- NodeForce at Right Side Beam ----------------------
# #     load(RsideNode+g, 0, +P0*Dy*0.5*2.0,0) # RsideNode+g
# #     # print(LsideNode+g, RsideNode+g,f'S_Nodeforce_{ny}rowy/node{1+g}')

#=========================== Load Pattern 1: Shear wave / P wave ============================
tnscp = soilLength/cp # wave transport time
dcellcp = tnscp/ny #each cell time
cpdt = round(dcellcp/10, 7) #eace cell have 10 steps
print(f"tnscp = {tnscp}; dcellcp= {dcellcp}, cp_dt = {cpdt}")
# # # # ============ Calculate Extend TimeSeries dt ===============================
# # # Extend_Scale = 10
# # # Length = 10*Extend_Scale #m
# # # Extend_tns = Length/Vs # wave transport time
# # # Extend_dcell = Extend_tns/80 #each cell time
# # # Extend_dt = Extend_dcell/10 #eace cell have 10 steps
# # # print(f"Extend time:  time = {Extend_tns}; Extend_dt = {Extend_dt}")

# timeSeries('Path',702, '-filePath', f'TimeSeries/fp_80row.txt','-dt',cpdt) #1e-4 

# timeSeries('Path',702, '-filePath', f'TimeSeries/fs200_{ny}row.txt','-dt', 6.25e-5) # 2*sinwst

Constant_dt = 1e-5
timeSeries('Path',702, '-filePath', f'TimeSeries/Pulse/Pwave_Force_Column.txt','-dt', Constant_dt) # Pwave

# timeSeries('Path',704, '-filePath','TopForce10row.txt','-dt',2.67e-4)
# # ------------------ Extend Apply timeSeries --------------------------
# timeSeries('Path',702, '-filePath', f'Extend_TimeSeries/{Extend_Scale}_fs.txt','-dt', dt) # 1*sinwst
# #------------------- Harmonic Force ---------------------------------------------
# Pulse_dt = 1e-2
# timeSeries('Path', 710, '-filePath', f'TimeSeries/Pulse/Pulse_Series.txt','-dt',Pulse_dt)

pattern('Plain',703, 702)
# ------ Convert Beam Distributed force to nodal load --------------------------------
# load(1, 1.25, 0) # 20*Dx*(1/2)
# load(2, 1.25, 0)

# load(1, 0, 1.25) # 20*Dx*(1/2)
# load(2, 0, 1.25)

# ------------- P wave -----------------------------
for o in range(nx):
    eleLoad('-ele', BeamEle_Start+o, '-type','-beamUniform',40,0) # 20 for Harmonic / 40 for Const

# # ------------- S wave -----------------------------
# for o in range(nx):
#     eleLoad('-ele', BeamEle_Start+o, '-type','-beamUniform',0,40,0) # 20 for Harmonic / 40 for Const

# # # ===================== Load Pattern 2: TopForce on the top Middle Point ======================
# tnscp = soilLength/cp # wave transport time
# dcellcp = tnscp/ny #each cell time
# cpdt = round(dcellcp/10, 7) #eace cell have 10 steps
# # print(f"tnscp = {tnscp}; dcellcp= {dcellcp}, cp_dt = {cpdt}")

# # timeSeries('Path',704, '-filePath',f'TimeSeries/TopForce{ny}row.txt','-dt', cpdt)
# timeSeries('Path',704, '-filePath', f'TimeSeries/Pulse/TopForce_Constant.txt','-dt', Constant_dt) # TopForce _Constant TimeSeries

# pattern('Plain',703, 704)
# load(UpperN_Center-1, 0, -1)
# load(UpperN_Center,0,-1)
# load(UpperN_Center+1, 0, -1)

# print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# # # ---------------- One Column -----------------------
# # UpperN_Center = 1 + (1+nx)*ny
# # timeSeries('Path',704, '-filePath',f'TimeSeries/TopForce{ny}row.txt','-dt', cpdt)
# # pattern('Plain',703, 704)
# # load(UpperN_Center,0,-0.5)
# # load(UpperN_Center+1,0,-0.5)
# # print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# # ##----------Use velocity timeseries to make wave transport and Input velocity boundary(node 1,2)------------
# IDloadTag = 400   # load tag
# IDgmSeries = 500  # for multipleSupport Excitation

# # # iSupportNode = [1, 2] # BotTDash_Start, BotTDash_Start+2*1
# # # iGMdirection = [1,1]

# # # timeSeries('Path',706, '-filePath', f'TimeSeries/Accel_fs.txt','-dt', dt) # Acceleration_TimeSeries
# # # timeSeries('Path',708, '-filePath', f'TimeSeries/Vel_fs.txt','-dt', dt) # Velocity_TimeSeries
# # # timeSeries('Path',710, '-filePath', f'TimeSeries/Disp_fs.txt','-dt', dt) # Displacement_TimeSeries

# # # ===================== Load Pattern 3: Direct Apply Initial Conditions ======================
# u0 = 1
# v0 = 5
# # setNodeDisp(1,2,u0,'-commit')
# # setNodeDisp(2,2,u0,'-commit')

# setNodeVel(1,2,v0,'-commit')
# setNodeVel(2,2,v0,'-commit')

# # ============ Load Pattern 4: apply Disp / Vel TimeSeries ===============================
# Constant_dt = 1e-5
# # timeSeries('Path',706, '-filePath', f'Extend_TimeSeries/{Extend_Scale}Accel_fs.txt','-dt', Extend_dt) # Acceleration_TimeSeries
# timeSeries('Path',708, '-filePath', f'TimeSeries/Pulse/Velocity_Const.txt','-dt', Constant_dt) # Velocity_TimeSeries
# timeSeries('Path',710, '-filePath', f'TimeSeries/Pulse/Displacement_Const.txt','-dt', Constant_dt) # Displacement_TimeSeries

# IDloadTag = 400   # load tag
# IDgmSeries = 500  # for multipleSupport Excitation

# iSupportNode = [1, 2] # BotTDash_Start, BotTDash_Start+2*1
# iGMdirection = [2, 2]

# pattern('MultipleSupport', IDloadTag)
# groundMotion(IDgmSeries, 'Plain', '-vel', 708, 'int', 'Trapezoidal')
# imposedMotion(1, 2,IDgmSeries) # Bot Node 1
# imposedMotion(2, 2,IDgmSeries) # Bot Node 2
# # print(BotTDash_Start, BotTDash_Start+2*1)

# # pattern('MultipleSupport', IDloadTag)
# # for i in range(len(iSupportNode)):
# #     groundMotion(IDgmSeries+i, 'Plain', '-vel', 708,'int', 'Trapezoidal') # 'Trapezoidal'/'Simpson'
# #     imposedMotion(iSupportNode[i], iGMdirection[i], IDgmSeries+i)
# #     # print(iSupportNode[i], iGMdirection[i], IDgmSeries+i)

# # ============ Input Extend TimeSeries ===============================
# # Extend_Scale = 10
# Length = 10*Extend_Scale #m
# Extend_tns = Length/Vs # wave transport time
# Extend_dcell = Extend_tns/80 #each cell time
# Extend_dt = Extend_dcell/10 #eace cell have 10 steps
# print(f"Extend time:  time = {Extend_tns}; Extend_dt = {Extend_dt}")

# # timeSeries('Path',706, '-filePath', f'Extend_TimeSeries/{Extend_Scale}Accel_fs.txt','-dt', Extend_dt) # Acceleration_TimeSeries
# # timeSeries('Path',708, '-filePath', f'Extend_TimeSeries/{Extend_Scale}Vel_fs.txt','-dt', Extend_dt) # Velocity_TimeSeries
# # timeSeries('Path',710, '-filePath', f'Extend_TimeSeries/{Extend_Scale}Disp_fs.txt','-dt', Extend_dt) # Displacement_TimeSeries


# pattern('MultipleSupport', IDloadTag)
# groundMotion(IDgmSeries, 'Plain', '-vel', 708, 'int', 'Trapezoidal')
# imposedMotion(1, 1,IDgmSeries) #BotTDash_Start
# imposedMotion(2, 1,IDgmSeries) # BotTDash_Start+2*1
# # print(BotTDash_Start, BotTDash_Start+2*1)

# # pattern('MultipleSupport', IDloadTag)
# # for i in range(len(iSupportNode)):
# #     groundMotion(IDgmSeries+i, 'Plain', '-accel',706 ,'int', 'Trapezoidal') # 'Trapezoidal'/'Simpson'
# #     imposedMotion(iSupportNode[i], iGMdirection[i], IDgmSeries+i)
# #     # print(iSupportNode[i], iGMdirection[i], IDgmSeries+i)
    
# # path1 = f"Velocity"
# # path2 = f"Stress"
# # -------------- Recorder --------------------------------
# # ------------- left column -------------Stress /Velocity {path2}/{path1}
# recorder('Element', '-file', f'{path2}/ele{LowerE_Left}.out', '-time', '-ele',LowerE_Left, 'material ',1,'stresses')
# recorder('Element', '-file', f'{path2}/ele{CenterE_Left}.out', '-time', '-ele',CenterE_Left, 'material ',1,'stresses')

# recorder('Element', '-file', f'{path2}/ele{UpperE_Left}_1.out', '-time', '-ele',UpperE_Left, 'material ',1,'stresses')
# recorder('Element', '-file', f'{path2}/ele{UpperE_Left}_2.out', '-time', '-ele',UpperE_Left, 'material ',2,'stresses')
# recorder('Element', '-file', f'{path2}/ele{UpperE_Left}_3.out', '-time', '-ele',UpperE_Left, 'material ',3,'stresses')
# recorder('Element', '-file', f'{path2}/ele{UpperE_Left}_4.out', '-time', '-ele',UpperE_Left, 'material ',4,'stresses')

# recorder('Node', '-file', f'{path1}/node{LowerN_Left}.out', '-time', '-node',LowerN_Left,'-dof',1,2,3,'vel') 
# recorder('Node', '-file', f'{path1}/node{CenterN_Left}.out', '-time', '-node',CenterN_Left,'-dof',1,2,3,'vel')
# recorder('Node', '-file', f'{path1}/node{UpperN_Left}.out', '-time', '-node',UpperN_Left,'-dof',1,2,3,'vel')

# # recorder('Node', '-file', f'{path1}/Disp{LowerN_Left}.out', '-time', '-node',LowerN_Left,'-dof',1,2,3,'disp')
# # recorder('Node', '-file', f'{path1}/Disp{CenterN_Left}.out', '-time', '-node',CenterN_Left,'-dof',1,2,3,'disp')
# # recorder('Node', '-file', f'{path1}/Disp{UpperN_Left}.out', '-time', '-node',UpperN_Left,'-dof',1,2,3,'disp')

# # recorder('Node', '-file', f'{path1}/acc{LowerN_Left}.out', '-time', '-node',LowerN_Left,'-dof',1,2,3,'accel')
# # recorder('Node', '-file', f'{path1}/acc{CenterN_Left}.out', '-time', '-node',CenterN_Left,'-dof',1,2,3,'accel')
# # recorder('Node', '-file', f'{path1}/acc{UpperN_Left}.out', '-time', '-node',UpperN_Left,'-dof',1,2,3,'accel')
# # ------------- Center column ------------- Stress /Velocity
# recorder('Element', '-file', f'{path2}/ele{LowerE_Center}.out', '-time', '-ele',LowerE_Center, 'material ',1,'stresses')
# recorder('Element', '-file', f'{path2}/ele{CenterE_Center}.out', '-time', '-ele',CenterE_Center, 'material ',1,'stresses')

# recorder('Element', '-file', f'{path2}/ele{UpperE_Center}_1.out', '-time', '-ele',UpperE_Center, 'material ',1,'stresses')
# recorder('Element', '-file', f'{path2}/ele{UpperE_Center}_2.out', '-time', '-ele',UpperE_Center, 'material ',2,'stresses')
# recorder('Element', '-file', f'{path2}/ele{UpperE_Center}_3.out', '-time', '-ele',UpperE_Center, 'material ',3,'stresses')
# recorder('Element', '-file', f'{path2}/ele{UpperE_Center}_4.out', '-time', '-ele',UpperE_Center, 'material ',4,'stresses')

# recorder('Node', '-file', f'{path1}/node{LowerN_Center}.out', '-time', '-node',LowerN_Center,'-dof',1,2,3,'vel')
# recorder('Node', '-file', f'{path1}/node{CenterN_Center}.out', '-time', '-node',CenterN_Center,'-dof',1,2,3,'vel')
# recorder('Node', '-file', f'{path1}/node{UpperN_Center}.out', '-time', '-node',UpperN_Center,'-dof',1,2,3,'vel')

# recorder('Node', '-file', f'{path1}/Disp{LowerN_Center}.out', '-time', '-node',LowerN_Center,'-dof',1,2,3,'disp')
# recorder('Node', '-file', f'{path1}/Disp{CenterN_Center}.out', '-time', '-node',CenterN_Center,'-dof',1,2,3,'disp')
# recorder('Node', '-file', f'{path1}/Disp{UpperN_Center}.out', '-time', '-node',UpperN_Center,'-dof',1,2,3,'disp')

# recorder('Node', '-file', f'{path1}/acc{LowerN_Center}.out', '-time', '-node',LowerN_Center,'-dof',1,2,3,'accel')
# recorder('Node', '-file', f'{path1}/acc{CenterN_Center}.out', '-time', '-node',CenterN_Center,'-dof',1,2,3,'accel')
# recorder('Node', '-file', f'{path1}/acc{UpperN_Center}.out', '-time', '-node',UpperN_Center,'-dof',1,2,3,'accel')
# # ------------- Right column -------------
# recorder('Element', '-file', f'{path2}/ele{LowerE_Right}.out', '-time', '-ele',LowerE_Right, 'material ',1,'stresses')
# recorder('Element', '-file', f'{path2}/ele{CenterE_Right}.out', '-time', '-ele',CenterE_Right, 'material ',1,'stresses')

# recorder('Element', '-file', f'{path2}/ele{UpperE_Right}_1.out', '-time', '-ele',UpperE_Right, 'material ',1,'stresses')
# recorder('Element', '-file', f'{path2}/ele{UpperE_Right}_2.out', '-time', '-ele',UpperE_Right, 'material ',2,'stresses')
# recorder('Element', '-file', f'{path2}/ele{UpperE_Right}_3.out', '-time', '-ele',UpperE_Right, 'material ',3,'stresses')
# recorder('Element', '-file', f'{path2}/ele{UpperE_Right}_4.out', '-time', '-ele',UpperE_Right, 'material ',4,'stresses')

# recorder('Node', '-file', f'{path1}/node{LowerN_Right}.out', '-time', '-node',LowerN_Right,'-dof',1,2,3,'vel')
# recorder('Node', '-file', f'{path1}/node{CenterN_Right}.out', '-time', '-node',CenterN_Right,'-dof',1,2,3,'vel')
# recorder('Node', '-file', f'{path1}/node{UpperN_Right}.out', '-time', '-node',UpperN_Right,'-dof',1,2,3,'vel')

# recorder('Node', '-file', f'{path1}/Disp{LowerN_Right}.out', '-time', '-node',LowerN_Right,'-dof',1,2,3,'disp')
# recorder('Node', '-file', f'{path1}/Disp{CenterN_Right}.out', '-time', '-node',CenterN_Right,'-dof',1,2,3,'disp')
# recorder('Node', '-file', f'{path1}/Disp{UpperN_Right}.out', '-time', '-node',UpperN_Right,'-dof',1,2,3,'disp')

# recorder('Node', '-file', f'{path1}/acc{LowerN_Right}.out', '-time', '-node',LowerN_Right,'-dof',1,2,3,'accel')
# recorder('Node', '-file', f'{path1}/acc{CenterN_Right}.out', '-time', '-node',CenterN_Right,'-dof',1,2,3,'accel')
# recorder('Node', '-file', f'{path1}/acc{UpperN_Right}.out', '-time', '-node',UpperN_Right,'-dof',1,2,3,'accel')

# # ==== Left 1/4 node ======================================
# recorder('Element', '-file', f'{path2}/ele{UpperrE_LQuarter}.out', '-time', '-ele',UpperrE_LQuarter, 'material ',1,'stresses')
# recorder('Node', '-file', f'{path1}/node{UpperrN_LQuarter}.out', '-time', '-node',UpperrN_LQuarter,'-dof',1,2,3,'vel')

# # ==== Right 1/4 node ======================================
# recorder('Element', '-file', f'{path2}/ele{UpperrE_RQuarter}_1.out', '-time', '-ele',UpperrE_RQuarter, 'material ',1,'stresses')
# recorder('Element', '-file', f'{path2}/ele{UpperrE_RQuarter}_2.out', '-time', '-ele',UpperrE_RQuarter, 'material ',2,'stresses')
# recorder('Element', '-file', f'{path2}/ele{UpperrE_RQuarter}_3.out', '-time', '-ele',UpperrE_RQuarter, 'material ',3,'stresses')
# recorder('Element', '-file', f'{path2}/ele{UpperrE_RQuarter}_4.out', '-time', '-ele',UpperrE_RQuarter, 'material ',4,'stresses')

# recorder('Node', '-file', f'{path1}/node{UpperrN_RQuarter}.out', '-time', '-node',UpperrN_RQuarter,'-dof',1,2,3,'vel')

# # ------ One Column ---------
# recorder('Node', '-file', f'{path1}/Disp3.out', '-time', '-node',3,'-dof',1,2,3,'disp')
# recorder('Node', '-file', f'{path1}/Disp4.out', '-time', '-node',4,'-dof',1,2,3,'disp')

# recorder('Node', '-file', f'{path1}/node3.out', '-time', '-node',3,'-dof',1,2,3,'vel')
# recorder('Node', '-file', f'{path1}/node4.out', '-time', '-node',4,'-dof',1,2,3,'vel')

# recorder('Node', '-file', f'{path1}/acc3.out', '-time', '-node',3,'-dof',1,2,3,'accel')
# recorder('Node', '-file', f'{path1}/acc4.out', '-time', '-node',4,'-dof',1,2,3,'accel')

# # ============== Node Reaction Force / Rayleigh Damping Force ======================== #rayleighForces (Rayle) / reaction (Reac)
# recorder('Node', '-file', f'{path1}/Reac163.out', '-time', '-node', 163,'-dof',1,2,3,'reaction')
# recorder('Node', '-file', f'{path1}/Reac164.out', '-time', '-node', 164,'-dof',1,2,3,'reaction')

# =================Comlumn OutPut to compare fix if the Bot and Top Element have error =============================
recorder('Node', '-file', f'{path1}/Disp1.out', '-time', '-node',1,'-dof',1,2,'disp')
recorder('Node', '-file', f'{path1}/Disp2.out', '-time', '-node',2,'-dof',1,2,'disp')
recorder('Node', '-file', f'{path1}/Disp3.out', '-time', '-node',3,'-dof',1,2,'disp')
recorder('Node', '-file', f'{path1}/Disp4.out', '-time', '-node',4,'-dof',1,2,'disp')

recorder('Node', '-file', f'{path1}/Vel1.out', '-time', '-node',1,'-dof',1,2,'vel')
recorder('Node', '-file', f'{path1}/Vel2.out', '-time', '-node',2,'-dof',1,2,'vel')
recorder('Node', '-file', f'{path1}/Vel3.out', '-time', '-node',3,'-dof',1,2,'vel')
recorder('Node', '-file', f'{path1}/Vel4.out', '-time', '-node',4,'-dof',1,2,'vel')

# recorder('Node', '-file', f'{path1}/accel1.out', '-time', '-node',1,'-dof',1,2,'accel')
# recorder('Node', '-file', f'{path1}/accel2.out', '-time', '-node',2,'-dof',1,2,'accel')
# recorder('Node', '-file', f'{path1}/accel3.out', '-time', '-node',3,'-dof',1,2,'accel')
# recorder('Node', '-file', f'{path1}/accel4.out', '-time', '-node',4,'-dof',1,2,'accel')

recorder('Element', '-file', f'{path2}/ele{1}_1.out', '-time', '-ele',1, 'material ',1,'stresses')
recorder('Element', '-file', f'{path2}/ele{1}_2.out', '-time', '-ele',1, 'material ',2,'stresses')
recorder('Element', '-file', f'{path2}/ele{1}_3.out', '-time', '-ele',1, 'material ',3,'stresses')
recorder('Element', '-file', f'{path2}/ele{1}_4.out', '-time', '-ele',1, 'material ',4,'stresses')
printModel('-ele', 1)
recorder('Element', '-file', f'{path2}/ele{1}_strain.out', '-time', '-ele',1, 'material ',1,'strain')

recorder('Element', '-file', f'{path2}/ele{UpperE_Left}_1.out', '-time', '-ele',UpperE_Left, 'material ',1,'stresses')
recorder('Element', '-file', f'{path2}/ele{UpperE_Left}_2.out', '-time', '-ele',UpperE_Left, 'material ',2,'stresses')
recorder('Element', '-file', f'{path2}/ele{UpperE_Left}_3.out', '-time', '-ele',UpperE_Left, 'material ',3,'stresses')
recorder('Element', '-file', f'{path2}/ele{UpperE_Left}_4.out', '-time', '-ele',UpperE_Left, 'material ',4,'stresses')

recorder('Node', '-file', f'{path2}/Reac1.out', '-time', '-node',1,'-dof',1,2,3,'reaction')
recorder('Node', '-file', f'{path2}/Reac2.out', '-time', '-node',2,'-dof',1,2,3,'reaction')

recorder('Node', '-file', f'{path2}/Reac3.out', '-time', '-node',3,'-dof',1,2,3,'reaction') #rayleighForces / reaction
recorder('Node', '-file', f'{path2}/Reac4.out', '-time', '-node',4,'-dof',1,2,3,'reaction')

# ------------ Rayleigh Damping Node -------------------------
recorder('Node', '-file', f'{path2}/Damp1.out', '-time', '-node',1,'-dof',1,2,3,'rayleighForces')
recorder('Node', '-file', f'{path2}/Damp2.out', '-time', '-node',2,'-dof',1,2,3,'rayleighForces')

recorder('Node', '-file', f'{path2}/Damp3.out', '-time', '-node',3,'-dof',1,2,3,'rayleighForces') #rayleighForces / reaction
recorder('Node', '-file', f'{path2}/Damp4.out', '-time', '-node',4,'-dof',1,2,3,'rayleighForces')

for i in range(nx+1):
    recorder('Node', '-file', f'{path2}/Damp{BotNode+i}.out', '-time', '-node',BotNode+i,'-dof',1,2,3,'rayleighForces')
    recorder('Node', '-file', f'{path2}/Reac{BotNode+i}.out', '-time', '-node',BotNode+i,'-dof',1,2,3,'reaction')
# ---------------- Disp / Vel ----------------------------
    recorder('Node', '-file', f'{path1}/Disp{BotNode+i}.out', '-time', '-node',BotNode+i,'-dof',1,2,3,'disp')
         
    print(f"BotNode_Rayleigh = {BotNode+i}")

# for j in range(2):
#     recorder('Node', '-file', f'{path2}/Damp{LeftNode+j}.out', '-time', '-node',LeftNode+j,'-dof',1,2,3,'rayleighForces')
#     recorder('Node', '-file', f'{path2}/Reac{LeftNode+j}.out', '-time', '-node',LeftNode+j,'-dof',1,2,3,'reaction')

#     recorder('Node', '-file', f'{path2}/Damp{RightNode+j}.out', '-time', '-node',RightNode+j,'-dof',1,2,3,'rayleighForces')
#     recorder('Node', '-file', f'{path2}/Reac{RightNode+j}.out', '-time', '-node',RightNode+j,'-dof',1,2,3,'reaction')
# # ---------------- Disp / Vel ----------------------------
#     recorder('Node', '-file', f'{path1}/Disp{LeftNode+j}.out', '-time', '-node',LeftNode+j,'-dof',1,2,3,'disp')
#     recorder('Node', '-file', f'{path1}/Disp{RightNode+j}.out', '-time', '-node',RightNode+j,'-dof',1,2,3,'disp')

#     print(f"LSideNode_Rayleigh = {LeftNode+j}; RSideNode_Rayleigh = {RightNode+j}")

# # ------------ LK Dashpot Node -------------------------
# for l in range(nx+1):
#     # ----------- Bot Dashpot Node -----------------------
#     recorder('Node', '-file', f'{path2}/Damp{BotTDash_Start+2*l}.out', '-time', '-node',BotTDash_Start+2*l,'-dof',1,2,3,'reaction')
#     recorder('Node', '-file', f'{path2}/Damp{(BotTDash_Start+1)+2*l}.out', '-time', '-node',(BotTDash_Start+1)+2*l,'-dof',1,2,3,'reaction')

#     recorder('Node', '-file', f'{path2}/Damp{BotNDash_Start+2*l}.out', '-time', '-node',BotNDash_Start+2*l,'-dof',1,2,3,'reaction')
#     recorder('Node', '-file', f'{path2}/Damp{(BotNDash_Start+1)+2*l}.out', '-time', '-node',(BotNDash_Start+1)+2*l,'-dof',1,2,3,'reaction')

# # -+----------- Disp /Vel ------------------
#     recorder('Node', '-file', f'{path1}/Disp{BotTDash_Start+2*l}.out', '-time', '-node',BotTDash_Start+2*l,'-dof',1,2,3,'disp')
#     recorder('Node', '-file', f'{path1}/Disp{(BotTDash_Start+1)+2*l}.out', '-time', '-node',(BotTDash_Start+1)+2*l,'-dof',1,2,3,'disp')

#     recorder('Node', '-file', f'{path1}/Disp{BotNDash_Start+2*l}.out', '-time', '-node',BotNDash_Start+2*l,'-dof',1,2,3,'disp')
#     recorder('Node', '-file', f'{path1}/Disp{(BotNDash_Start+1)+2*l}.out', '-time', '-node',(BotNDash_Start+1)+2*l,'-dof',1,2,3,'disp')
    
#     print(f"BotTDash_Start+2*l = {BotTDash_Start+2*l}; (BotTDash_Start+1)+2*l = {(BotTDash_Start+1)+2*l}; BotNDash_Start+2*l = {BotNDash_Start+2*l}; (BotNDash_Start+1)+2*l = {(BotNDash_Start+1)+2*l}")
# for l in range(nx):     
# # -----------Left + Right Side Dashpot Node -----------------------
#     recorder('Node', '-file', f'{path2}/Damp{LSideNDash_Start+2*l}.out', '-time', '-node',LSideNDash_Start+2*l,'-dof',1,2,3,'reaction')
#     recorder('Node', '-file', f'{path2}/Damp{(LSideNDash_Start+1)+2*l}.out', '-time', '-node',(LSideNDash_Start+1)+2*l,'-dof',1,2,3,'reaction')

#     recorder('Node', '-file', f'{path2}/Damp{LSideTDash_Start+2*l}.out', '-time', '-node',LSideTDash_Start+2*l,'-dof',1,2,3,'reaction')
#     recorder('Node', '-file', f'{path2}/Damp{(LSideTDash_Start+1)+2*l}.out', '-time', '-node',(LSideTDash_Start+1)+2*l,'-dof',1,2,3,'reaction')

#     recorder('Node', '-file', f'{path2}/Damp{RSideNDash_Start+2*l}.out', '-time', '-node',RSideNDash_Start+2*l,'-dof',1,2,3,'reaction')
#     recorder('Node', '-file', f'{path2}/Damp{(RSideNDash_Start+1)+2*l}.out', '-time', '-node',(RSideNDash_Start+1)+2*l,'-dof',1,2,3,'reaction')

#     recorder('Node', '-file', f'{path2}/Damp{RSideTDash_Start+2*l}.out', '-time', '-node',RSideTDash_Start+2*l,'-dof',1,2,3,'reaction')
#     recorder('Node', '-file', f'{path2}/Damp{(RSideTDash_Start+1)+2*l}.out', '-time', '-node',(RSideTDash_Start+1)+2*l,'-dof',1,2,3,'reaction')

# # -+----------- Disp /Vel ------------------
#     recorder('Node', '-file', f'{path1}/Disp{LSideNDash_Start+2*l}.out', '-time', '-node',LSideNDash_Start+2*l,'-dof',1,2,3,'disp')
#     recorder('Node', '-file', f'{path1}/Disp{(LSideNDash_Start+1)+2*l}.out', '-time', '-node',(LSideNDash_Start+1)+2*l,'-dof',1,2,3,'disp')

#     recorder('Node', '-file', f'{path1}/Disp{LSideTDash_Start+2*l}.out', '-time', '-node',LSideTDash_Start+2*l,'-dof',1,2,3,'disp')
#     recorder('Node', '-file', f'{path1}/Disp{(LSideTDash_Start+1)+2*l}.out', '-time', '-node',(LSideTDash_Start+1)+2*l,'-dof',1,2,3,'disp')

#     recorder('Node', '-file', f'{path1}/Disp{RSideNDash_Start+2*l}.out', '-time', '-node',RSideNDash_Start+2*l,'-dof',1,2,3,'disp')
#     recorder('Node', '-file', f'{path1}/Disp{(RSideNDash_Start+1)+2*l}.out', '-time', '-node',(RSideNDash_Start+1)+2*l,'-dof',1,2,3,'disp')

#     recorder('Node', '-file', f'{path1}/Disp{RSideTDash_Start+2*l}.out', '-time', '-node',RSideTDash_Start+2*l,'-dof',1,2,3,'disp')
#     recorder('Node', '-file', f'{path1}/Disp{(RSideTDash_Start+1)+2*l}.out', '-time', '-node',(RSideTDash_Start+1)+2*l,'-dof',1,2,3,'disp')

#     print(f"LSideNDash_Start+2*l = {LSideNDash_Start+2*l}; (LSideNDash_Start+1)+2*l = {(LSideNDash_Start+1)+2*l}; LSideTDash_Start+2*l = {LSideTDash_Start+2*l}; (LSideTDash_Start+1)+2*l = {(LSideTDash_Start+1)+2*l}")
#     print(f"RSideNDash_Start+2*l = {RSideNDash_Start+2*l}; (RSideNDash_Start+1)+2*l = {(RSideNDash_Start+1)+2*l}; RSideTDash_Start+2*l = {RSideTDash_Start+2*l}; (RSideTDash_Start+1)+2*l = {(RSideTDash_Start+1)+2*l}")

# # ---------- Conside H/4 and 3H/4 Deep Element Stress -------------------
# H1_id = int((soilLength*0.25)/Dy)
# H3_id = int((soilLength*0.75)/Dy)

# recorder('Element', '-file', f'{path2}/ele{H1_id+1}.out', '-time', '-ele',H1_id+1, 'material ',1,'stresses')
# recorder('Element', '-file', f'{path2}/ele{H3_id+1}.out', '-time', '-ele',H3_id+1, 'material ',1,'stresses')

system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
# =========== Input dt ============================
analyze(10000,dt) #int(analystep) 10000*2e-5 = 0.2

print("finish analyze:0 ~ 0.8s")

end = time.time()
print(end - start)
