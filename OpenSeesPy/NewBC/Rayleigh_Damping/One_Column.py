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

Extend_Scale = 100

wipe()
# -------- Start calculaate time -----------------
start = time.time()
print("The time used to execute this is given below")

model('basic', '-ndm', 2, '-ndf' , 2)

# ============= Real Element Elastic Modules =====================
E = 208000000 # (N/m^2)= (kg*m/s2)*(1/m2) = kg/(s2*m) 
nu = 0.3 #0.3
rho = 2000    # kg/m3 
nDMaterial('ElasticIsotropic', 2000, E, nu, rho)

soilLength = 10*Extend_Scale #m
soilwidth = 0.125*Extend_Scale   #1.0/ 0.125

nx = int(soilwidth/(0.125*Extend_Scale))
ny = 80 #80
e1 = 1
n1 = 1
eleArgs = [1, 'PlaneStrain', 2000]
points = [1, 0.0,   0.0, 
        2, soilwidth,  0.0, 
        3, soilwidth,  soilLength, 
        4, 0.0,   soilLength]
block2D(nx, ny, e1, n1,'quad', *eleArgs, *points)

# -------- Soil B.C (Tie BC) ---------------
for i in range(ny+1):
    equalDOF((nx+1)*i+1,(nx+1)*i+(nx+1),1,2)

endNode = (1+nx) + (nx+1)*ny
endEle = nx*ny
# print(f"endNode= {endNode}, endEle= {endEle}")

Vp = 374.166    # m/s 
Vs = 200     ;# m/s 

yMesh = soilLength/ny # Y row MeshSize
dcell = yMesh / Vs 
dt = dcell/10.0  #6.25e-5
print(f"yMesh = {yMesh}; dcell = {dcell}")
# ======= Totla Analysis Time ============================
analysisTime = (soilLength/Vs)*8
analystep = analysisTime/dt # int(800*(ny/10))
print(f"dt = {dt}; Analysis Total Time = {analysisTime} ;Analysis_step = {analystep}")
                  
widthMesh = soilwidth/nx
print(f"widthMesh = {widthMesh}")
# ------ Recorde Node/Element ID -----------------------------------------------
LowerN_Left =  1
CenterN_Left = int(LowerN_Left + (nx+1)*(ny/2))
UpperN_Left = int(LowerN_Left + (nx+1)* ny)
# print(f"LowerN_Left = {LowerN_Left},CenterN_Left = {CenterN_Left}, UpperN_Left = {UpperN_Left}")
LowerE_Left =  1
CenterE_Left = int(LowerE_Left + nx*(ny/2))
UpperE_Left = int(LowerE_Left + nx* (ny-1))
# print(f"LowerE_Left = {LowerE_Left},CenterE_Left = {CenterE_Left}, UpperE_Left = {UpperE_Left}")

LowerN_Center =  int(1 + (nx/2))
CenterN_Center = int(LowerN_Center + (nx+1)*(ny/2))
UpperN_Center = int(LowerN_Center + (nx+1)* ny)
print(f"LowerN_Center = {LowerN_Center},CenterN_Center = {CenterN_Center}, UpperN_Center = {UpperN_Center}")

LowerE_Center =  int((nx/2)+1)
CenterE_Center = int(LowerE_Center + nx*(ny/2))
UpperE_Center = int(LowerE_Center + nx* (ny-1))
# print(f"LowerE_Center = {LowerE_Center} ,CenterE_Center = {CenterE_Center}, UpperE_Center = {UpperE_Center}")

LowerN_Right =  int(nx+1)
CenterN_Right = int(LowerN_Right + (nx+1)*(ny/2))
UpperN_Right = int(LowerN_Right + (nx+1)* ny)
# print(f"LowerN_Right = {LowerN_Right},CenterN_Right = {CenterN_Right}, UpperN_Right = {UpperN_Right}")
LowerE_Right =  int(nx)
CenterE_Right = int(LowerE_Right + nx*(ny/2))
UpperE_Right = int(LowerE_Right + nx* (ny-1))
# print(f"LowerE_Right = {LowerE_Right} ,CenterE_Right = {CenterE_Right}, UpperE_Right = {UpperE_Right}")

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

# ============== Apply Bottom virtual Quad element to apply Rayleigh Dashpot =======================
BotNode = endNode+ 1 
BotEle = endEle + 1

for i in range(nx+1):
    node(BotNode+i, widthMesh*i, -0.125*Extend_Scale)
    fix(BotNode+i, 1 ,1) # like LK Dashpot have the fix end to get reaction Rayleigh Force
    # print(BotNode+i, widthMesh*i, -0.125*Extend_Scale)

# ============= Virtual Element Elastic Modules (E' control by M or G) =====================
M = rho*Vp*Vp
G = rho*Vs*Vs

nu2 = 0.0
Scale = 1e-2 # Control Size  (1/10000) 
E_M = Scale* M*((1+nu2)*(1-2*nu2)/(1-nu2)) # young's Module Control by M (P wave Velocity) # (N/m^2)= (kg*m/s2)*(1/m2) = kg/(s2*m) 
E_G = Scale* 2*G*(1+nu2) # young's Module Control by G (S wave Velocity) # (N/m^2)= (kg*m/s2)*(1/m2) = kg/(s2*m) 

rho2 =  Scale*rho   # kg/m3 
nDMaterial('ElasticIsotropic', 2006, E_G, nu2, rho2)

# --------------- Apply Bot Virtual Quad element ----------------------------------------------
for k in range(nx):
    element('quad', BotEle+k, BotNode+k, (BotNode+1)+k, (n1+1)+k,  n1+k, 1, 'PlaneStrain', 2006)
    # print( BotEle+k, BotNode+k, (BotNode+1)+k, (n1+1)+k,  n1+k, 1, 'PlaneStrain', 2006)

# # =============Apply Left and Right virtual Quad element to apply Rayleigh Dashpot =======================
# LeftNode = BotNode+ nx + 1
# RightNode = LeftNode + ny + 1

# LeftEle = BotEle + nx
# RightEle = LeftEle + ny

# for i in range(ny+1):
#     node(LeftNode+i, -widthMesh, yMesh*i)
#     node(RightNode+i, soilwidth+widthMesh, yMesh*i)

# for k in range(ny):
#     element('quad', LeftEle+k, LeftNode+k, n1+(n1+nx)*k, (n1+(n1+nx))+(n1+nx)*k,  (LeftNode+1)+k, *eleArgs)
#     element('quad', RightEle+k, (n1+nx)+ (n1+nx)*k, RightNode+k, (RightNode+1)+k, (n1+nx)*2+ (n1+nx)*k, *eleArgs)
#     # print(RightEle+k, (n1+nx)+ (n1+nx)*k, RightNode+k, (RightNode+1)+k, (n1+nx)*2+ (n1+nx)*k)

# # =========== Bottom Beam element ===================
# # --------- Bot Virtual quad -----------
# BeamNode_Start = BotNode + 2
# BeamEle_Start = BotEle + 1
# # ---------- With Side Virtual quad --------------
# # BeamNode_Start = RightNode + ny +1
# # BeamEle_Start = RightEle + ny
# # ----------- LK Dashpot ------------------------
# BeamNode_Start = endNode +1
# BeamEle_Start = endEle + 1

# model('basic', '-ndm', 2, '-ndf' , 3)
# for j in range(nx+1):
#     node(BeamNode_Start+j, widthMesh*j,0.0)
#     mass(BeamNode_Start+j,1,1,1)
# # -------- fix rotate dof ------------
#     fix(BeamNode_Start+j,0,0,1)

# # ------------- Beam parameter -----------------
# A = 0.1*1
# E1 = 1e-06 ;#1e-06
# Iz = (0.1*0.1*0.1)/12
# geomTransf('Linear', 1)

# for k in range(nx):
#     element('elasticBeamColumn', BeamEle_Start+k, BeamNode_Start+k, BeamNode_Start+1+k, A,E1,Iz, 1, '-release', 3)

# # =========== connect bot beam and soil element =========================
# for k in range(nx+1):
#     equalDOF(n1+k,BeamNode_Start+k,1,2)

# # ============= Bottom LK Dashpot element Dashpot ==========================
# BotTDash_Start =  endNode + 1# BeamNode_Start + (nx+1)
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
# BotTEle_Start = endEle + 1# BeamEle_Start + nx
# BotTEle_End = BotTEle_Start + nx

# element('zeroLength',BotTEle_Start,(BotTDash_Start+1),BotTDash_Start, '-mat',4001,'-dir',xdir)  # node 1: Left side 4003 / 4001
# element('zeroLength',BotTEle_End,(BotTDash_Start+1)+2*1,BotTDash_Start+2*1, '-mat',4001,'-dir',xdir)  # node 1: Left side
# # for m in range(1,nx): # nx+1
# #     element('zeroLength',BotTEle_Start+m,(BotTDash_Start+1)+2*m,BotTDash_Start+2*m, '-mat',4003,'-dir',xdir)  # node 1: Left side

# # ------ Normal dashpot element: Vp with y dir (98~106)
# BotNEle_Start = BotTEle_End+1
# BotNEle_End = BotNEle_Start+nx

# element('zeroLength',BotNEle_Start,(BotNDash_Start+1),BotNDash_Start, '-mat',4000,'-dir',ydir) # 4002 / 4000
# element('zeroLength',BotNEle_End,(BotNDash_Start+1)+2*1,BotNDash_Start+2*1, '-mat',4000,'-dir',ydir)
# # for m in range(1,nx): # nx+1
# #     element('zeroLength',BotNEle_Start+m,(BotNDash_Start+1)+2*m,BotNDash_Start+2*m, '-mat',4002,'-dir',ydir)  # node 1: Left side

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
    
# ================== Apply Rayleigh Dashpot ============================= 
# alphaM = -(6/yMesh)*(rho/rho2)*(Vp*(1-2*nu) + Vs*(2*nu-2)) # Vs = *1.5 ; Vp = *2.0 (special coff)
# betaK = -(-4*yMesh)*((1+nu)*(1-2*nu)/E)*rho*(Vp-Vs) 
# betaKinit = 0.0
# betaKcomm = 0.0
# # ----------- Consistnet Mass ----------------------------
# alphaM = (6/yMesh)*(rho/rho2)*(-Vp + 2*Vs)
# betaK = (4*yMesh)*(1/E_G)*rho*(Vp-Vs)
# betaKinit = 0.0
# betaKcomm = 0.0
# ----------- Lumped Mass ----------------------------
alphaM = (2/yMesh)*(rho/rho2)*(-Vp + 2*Vs) 
betaK = (2*yMesh)*(1/E_G)*rho*(Vp-Vs)
betaKinit = 0.0
betaKcomm = 0.0

print(f"alphaM = {alphaM}; betaK = {betaK}")
region(10000, '-ele ', BotEle ,'-rayleigh',alphaM, betaK, betaKinit,betaKcomm)

# # --------------- Bot Rayleigh Damping---------------------------
# region(10000, '-eleRange ', BotEle, BotEle+nx-1,'-rayleigh',alphaM, betaK, betaKinit,betaKcomm) 

# # --------------- Left / Right Rayleigh Damping---------------------------
# region(10001, '-eleRange ', LeftEle, LeftEle+ny-1,'-rayleigh',alphaM, betaK, betaKinit,betaKcomm) 
# region(10002, '-eleRange ', RightEle, RightEle+ny-1,'-rayleigh',alphaM, betaK, betaKinit,betaKcomm) 

# # ================ NewBC: for Case A/B============================
# # ====================Bulild Side Beam node (233~243 / 244~254) ====================
# # ----------Rayleigh Dashpot -----------------
# LsideNode = BeamNode_Start + nx+1
# RsideNode = LsideNode + (ny+1)
# LsideEle = BeamEle_Start + nx 
# RsideEle = LsideEle + ny

# # # ----LK Dashpot ------------
# # LsideNode = RSideTDash_Start + 2*(ny+1)
# # RsideNode = LsideNode + (ny+1)
# # LsideEle = RsideTEle_End + 1
# # RsideEle = LsideEle + ny

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

# #  ============================== S wave ======================================
# # ========================= "CaseA": SideLoad Pattern ===================================
# # ------------ Side Load Pattern ------------------------------
# xTimeSeriesID = 800
# xPatternID = 804

# coff = (Vs/Vp)
# for g in range(ny):
# # ------- timeSeries ID: 800~809 / Pattern ID: 804~813----------------------
#     timeSeries('Path',xTimeSeriesID+g, '-filePath',f'SSideforce_{ny}rowx/ele{1+g}.txt','-dt', dt)
#     pattern('Plain',xPatternID+g, xTimeSeriesID+g)
# # ---------- x direction : Sideforce ---------------------
# # ---------- Distributed at Left Side Beam ----------------------
#     eleLoad('-ele',LsideEle+g, '-type', '-beamUniform',-20*coff,0)  # for local axes Wy -
# # ---------- Distributed at Right Side Beam ----------------------
#     eleLoad('-ele',RsideEle+g, '-type', '-beamUniform',-20*coff,0)   # for local axes Wy +

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
    
#=========================== Load Pattern 1: Shear wave / P wave ============================
tnscp = soilLength/Vp # wave transport time
dcellcp = tnscp/ny #each cell time
cpdt = round(dcellcp/10, 7) #eace cell have 10 steps
print(f"tnscp = {tnscp}; dcellcp= {dcellcp}, cp_dt = {cpdt}")

# Extend_Scale = 10
Length = 10*Extend_Scale #m
Extend_tns = Length/Vs # wave transport time
Extend_dcell = Extend_tns/80 #each cell time
Extend_dt = Extend_dcell/10 #eace cell have 10 steps
print(f"Extend time:  time = {Extend_tns}; Extend_dt = {Extend_dt}")

# timeSeries('Path',702, '-filePath', f'TimeSeries/fp_80row.txt','-dt',cpdt) #1e-4
# timeSeries('Path',702, '-filePath', f'TimeSeries/fs200_{ny}row.txt','-dt', dt) # 2*sinwst
# timeSeries('Path',704, '-filePath','TopForce10row.txt','-dt',2.67e-4)
# ------------------ Extend Apply timeSeries --------------------------
timeSeries('Path',702, '-filePath', f'Extend_TimeSeries/{Extend_Scale}_fs.txt','-dt', dt) # 1*sinwst
# #------------------- Harmonic Force ---------------------------------------------
# Pulse_dt = 1e-2
# timeSeries('Path', 710, '-filePath', f'TimeSeries/Pulse/Pulse_Series.txt','-dt',Pulse_dt)

pattern('Plain',703, 702)
load(1, 1, 0)
load(2, 1, 0)
# # ------------- P wave -----------------------------
# for o in range(nx):
#     eleLoad('-ele', BeamEle_Start+o, '-type','-beamUniform',20,0)

# # ------------- S wave -----------------------------
# for o in range(nx):
#     eleLoad('-ele', BeamEle_Start+o, '-type','-beamUniform',0,20,0)

# # # ===================== Load Pattern 2: TopForce on the top Middle Point ======================
# tnscp = soilLength/Vp # wave transport time
# dcellcp = tnscp/ny #each cell time
# cpdt = round(dcellcp/10, 7) #eace cell have 10 steps
# print(f"tnscp = {tnscp}; dcellcp= {dcellcp}, cp_dt = {cpdt}")

# timeSeries('Path',704, '-filePath',f'TimeSeries/TopForce{ny}row.txt','-dt', cpdt)
# pattern('Plain',703, 704)
# load(UpperN_Center,0,-1)

# print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# # ---------------- One Column -----------------------
# UpperN_Center = 1 + (1+nx)*ny
# timeSeries('Path',704, '-filePath',f'TimeSeries/TopForce{ny}row.txt','-dt', cpdt)
# pattern('Plain',703, 704)
# load(UpperN_Center,0,-0.5)
# load(UpperN_Center+1,0,-0.5)
# print("finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)")

# ##----------Use velocity timeseries to make wave transport and Input velocity boundary(node 1,2)------------
# IDloadTag = 400   # load tag
# IDgmSeries = 500  # for multipleSupport Excitation

# # iSupportNode = [1, 2] # BotTDash_Start, BotTDash_Start+2*1
# # iGMdirection = [1,1]

# # timeSeries('Path',706, '-filePath', f'TimeSeries/Accel_fs.txt','-dt', dt) # Acceleration_TimeSeries
# # timeSeries('Path',708, '-filePath', f'TimeSeries/Vel_fs.txt','-dt', dt) # Velocity_TimeSeries
# # timeSeries('Path',710, '-filePath', f'TimeSeries/Disp_fs.txt','-dt', dt) # Displacement_TimeSeries

# # ============ Input Extend TimeSeries ===============================
# # Extend_Scale = 10
# Length = 10*Extend_Scale #m
# Extend_tns = Length/Vs # wave transport time
# Extend_dcell = Extend_tns/80 #each cell time
# Extend_dt = Extend_dcell/10 #eace cell have 10 steps
# print(f"Extend time:  time = {Extend_tns}; Extend_dt = {Extend_dt}")

# timeSeries('Path',706, '-filePath', f'Extend_TimeSeries/{Extend_Scale}Accel_fs.txt','-dt', Extend_dt) # Acceleration_TimeSeries
# timeSeries('Path',708, '-filePath', f'Extend_TimeSeries/{Extend_Scale}Vel_fs.txt','-dt', Extend_dt) # Velocity_TimeSeries
# timeSeries('Path',710, '-filePath', f'Extend_TimeSeries/{Extend_Scale}Disp_fs.txt','-dt', Extend_dt) # Displacement_TimeSeries


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

# # -------------- Recorder --------------------------------
# ------------- left column -------------
recorder('Element', '-file', f'Stress/ele{LowerE_Left}.out', '-time', '-ele',LowerE_Left, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{CenterE_Left}.out', '-time', '-ele',CenterE_Left, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{UpperE_Left}.out', '-time', '-ele',UpperE_Left, 'material ',1,'stresses')

recorder('Node', '-file', f'Velocity/node{LowerN_Left}.out', '-time', '-node',LowerN_Left,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'Velocity/node{CenterN_Left}.out', '-time', '-node',CenterN_Left,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'Velocity/node{UpperN_Left}.out', '-time', '-node',UpperN_Left,'-dof',1,2,3,'vel')

recorder('Node', '-file', f'Velocity/Disp{LowerN_Left}.out', '-time', '-node',LowerN_Left,'-dof',1,2,3,'disp')
recorder('Node', '-file', f'Velocity/Disp{CenterN_Left}.out', '-time', '-node',CenterN_Left,'-dof',1,2,3,'disp')
recorder('Node', '-file', f'Velocity/Disp{UpperN_Left}.out', '-time', '-node',UpperN_Left,'-dof',1,2,3,'disp')
# ------------- Center column -------------
recorder('Element', '-file', f'Stress/ele{LowerE_Center}.out', '-time', '-ele',LowerE_Center, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{CenterE_Center}.out', '-time', '-ele',CenterE_Center, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{UpperE_Center}.out', '-time', '-ele',UpperE_Center, 'material ',1,'stresses')

recorder('Node', '-file', f'Velocity/node{LowerN_Center}.out', '-time', '-node',LowerN_Center,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'Velocity/node{CenterN_Center}.out', '-time', '-node',CenterN_Center,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'Velocity/node{UpperN_Center}.out', '-time', '-node',UpperN_Center,'-dof',1,2,3,'vel')

recorder('Node', '-file', f'Velocity/Disp{LowerN_Center}.out', '-time', '-node',LowerN_Center,'-dof',1,2,3,'disp')
recorder('Node', '-file', f'Velocity/Disp{CenterN_Center}.out', '-time', '-node',CenterN_Center,'-dof',1,2,3,'disp')
recorder('Node', '-file', f'Velocity/Disp{UpperN_Center}.out', '-time', '-node',UpperN_Center,'-dof',1,2,3,'disp')
# ------------- Right column -------------
recorder('Element', '-file', f'Stress/ele{LowerE_Right}.out', '-time', '-ele',LowerE_Right, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{CenterE_Right}.out', '-time', '-ele',CenterE_Right, 'material ',1,'stresses')
recorder('Element', '-file', f'Stress/ele{UpperE_Right}.out', '-time', '-ele',UpperE_Right, 'material ',1,'stresses')

recorder('Node', '-file', f'Velocity/node{LowerN_Right}.out', '-time', '-node',LowerN_Right,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'Velocity/node{CenterN_Right}.out', '-time', '-node',CenterN_Right,'-dof',1,2,3,'vel')
recorder('Node', '-file', f'Velocity/node{UpperN_Right}.out', '-time', '-node',UpperN_Right,'-dof',1,2,3,'vel')

recorder('Node', '-file', f'Velocity/Disp{LowerN_Right}.out', '-time', '-node',LowerN_Right,'-dof',1,2,3,'disp')
recorder('Node', '-file', f'Velocity/Disp{CenterN_Right}.out', '-time', '-node',CenterN_Right,'-dof',1,2,3,'disp')
recorder('Node', '-file', f'Velocity/Disp{UpperN_Right}.out', '-time', '-node',UpperN_Right,'-dof',1,2,3,'disp')
# # ==== Left 1/4 node ======================================
# recorder('Element', '-file', f'Stress/ele{UpperrE_LQuarter}.out', '-time', '-ele',UpperrE_LQuarter, 'material ',1,'stresses')
# recorder('Node', '-file', f'Velocity/node{UpperrN_LQuarter}.out', '-time', '-node',UpperrN_LQuarter,'-dof',1,2,3,'vel')

# # ==== Right 1/4 node ======================================
# recorder('Element', '-file', f'Stress/ele{UpperrE_RQuarter}.out', '-time', '-ele',UpperrE_RQuarter, 'material ',1,'stresses')
# recorder('Node', '-file', f'Velocity/node{UpperrN_RQuarter}.out', '-time', '-node',UpperrN_RQuarter,'-dof',1,2,3,'vel')

system("UmfPack")
numberer("RCM")
constraints("Transformation")
integrator("Newmark", 0.5, 0.25)
algorithm("Newton")
test('EnergyIncr',1e-8, 200)
analysis("Transient")
# analyze(int(analystep),dt)

# ---- Extend TimeSeries Dt -----------
analyze(int(analystep),Extend_dt)
# analyze(int(analystep),cpdt)

# # ---------Pulse TimeSeries Dt -----------
# analyze(3000,Pulse_dt)

print("finish analyze:0 ~ 0.8s")

end = time.time()
print(end - start)
