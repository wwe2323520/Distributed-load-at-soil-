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

pi = np.pi
# Choose_Wave = f"Test_Integrator/NewMark_Linear/Test" # Central / NewMark_Constant / NewMark_Linear

# ----------- Rayleigh Dashpot Cofficient ------------------
# Integrator = "Central"
     
PtimeNum = np.array([702, 704, 705, 706]) # For P wave TimeSeries 702, 704, 705, 706
StimeNum = np.array([707, 708, 709, 710]) # For S wave TimeSeries 707, 708, 709, 710]

Force_HZ = np.array([10, 20, 40, 80]) # 10, 20, 40, 80
Width = np.array([2.0, 10.0, 20.0]) # 2.0, 10.0, 20.0
Y_MeshNumber= np.array([40]) # 80, 40, 20, 10

Choose_Wave = f"Newmark_Linear/Pwave" # Pwave / Swave (use to build file name)

for i in range(len(Width)):
    soilwidth = Width[i]
    print(f"================ Now SoilWidth = {soilwidth} ================")

    for j in range(len(Force_HZ)):
        TimeSeries_Num = int(PtimeNum[j]) # PtimeNum / StimeNum
        HZ = int(Force_HZ[j])
        print(f"--------------------- Force td = 1/f = {HZ} -------------------")

        for h in range(len(Y_MeshNumber)):
            ny = int(Y_MeshNumber[h])
            # print(soilwidth, TimeSeries_Num, HZ, ny)
    
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
            # soilwidth =  2.0 # 2.0 / 0.125
            # ny = 40 # 80, 40, 20, 10

            yMesh = soilLength/ny # Y row MeshSize
            dcell = (yMesh / Vp)

            Dw = soilLength/80 # soilLength/80 , soilLength/ny
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

            dt_Mesh = (soilLength/ny) # (soilLength/ny)
            dt = (dt_Mesh/Vp)*Dt_Size # dcell*Dt_Size
            print(f'dt_Mesh = {dt_Mesh}')

            print(f"Pwave travel yMesh= {yMesh}; each ele = {dcell} ;dt_Size = {Dt_Size}; dt = {dt}")
            # ======= Totla Analysis Time ============================
            analysisTime = (soilLength/Vp)*8
            analystep = analysisTime/dt # int(800*(ny/10))
            print(f"Analysis Total Time = {analysisTime} ;Analysis_step = {analystep}")

            # ================= Build Boundary File =====================
            Boundary = f"{Choose_Wave}/W_{int(soilwidth)}m/HZ_{HZ}/TieBC_{ny}row" 
            path1 = f'D:/shiang/OpenSeesPy/1D_Transport/{Boundary}/Velocity'
            path2 = f'D:/shiang/OpenSeesPy/1D_Transport/{Boundary}/Stress'

            if not os.path.isdir(path1):
                os.makedirs(path1)
            if not os.path.isdir(path2):
                os.makedirs(path2)

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

            # -------- Soil B.C (Tie BC) ---------------
            for i in range(ny+1):
                equalDOF((nx+1)*i+1,(nx+1)*i+(nx+1),1,2)
       
            # ============== Build Beam element =========================
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
            E1 = 1e-06
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
            sizeX = Dw  # m ******
            B_Smp = 0.5*rho*Vp*sizeX      # lower Left and Right corner node dashpot :N (newton)
            B_Sms = 0.5*rho*Vs*sizeX      # lower Left and Right corner node dashpot :N (newton)

            B_Cmp = 1.0*rho*Vp*sizeX      # Bottom Center node dashpot :N (newton)
            B_Cms = 1.0*rho*Vs*sizeX      # Bottom Center node dashpot :N (newton)

            uniaxialMaterial('Viscous',4000, B_Smp, 1)    # P wave: Side node
            uniaxialMaterial('Viscous',4001, B_Sms, 1)    # S wave: Side node

            uniaxialMaterial('Viscous',4002, B_Cmp, 1)    # P wave: Center node
            uniaxialMaterial('Viscous',4003, B_Cms, 1)    # S wave: Center node

            #----------- dashpot elements ------------------
            xdir = 1
            ydir = 2
            # ------ Traction dashpot element: 
            BotTEle_Start = BeamEle_Start + nx
            BotTEle_End = BotTEle_Start + nx

            element('zeroLength',BotTEle_Start,(BotTDash_Start+1),BotTDash_Start, '-mat',4001,'-dir',xdir)  #Left corner node
            element('zeroLength',BotTEle_End,(BotTDash_Start+1)+2*nx,BotTDash_Start+2*nx, '-mat',4001,'-dir',xdir)  #Right corner node
            for m in range(1,nx): # nx+1
                element('zeroLength',BotTEle_Start+m,(BotTDash_Start+1)+2*m,BotTDash_Start+2*m, '-mat',4003,'-dir',xdir)  # bottom side
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

            #=========================== Load Pattern 1: Shear wave / P wave ============================
            #------------- Input TimeSeries ------------------------------------
            TimeSeries_Path = f"D:/shiang/OpenSeesPy/TimeSeries" 

            Pwave_dt = 6.25e-05
            Swave_dt = 1.25e-04
            timeSeries('Path',702, '-filePath', f'{TimeSeries_Path}/Pwave_Time/New_Time/fp_HZ10.txt','-dt', Pwave_dt) # HZ = 10
            timeSeries('Path',704, '-filePath', f'{TimeSeries_Path}/Pwave_Time/New_Time/fp_HZ20.txt','-dt', Pwave_dt) # HZ = 20
            timeSeries('Path',705, '-filePath', f'{TimeSeries_Path}/Pwave_Time/New_Time/fp_HZ40.txt','-dt', Pwave_dt) # HZ = 40
            timeSeries('Path',706, '-filePath', f'{TimeSeries_Path}/Pwave_Time/New_Time/fp_HZ80.txt','-dt', Pwave_dt) # HZ = 80

            timeSeries('Path',707, '-filePath', f'{TimeSeries_Path}/Swave_Time/New_Time/fs_HZ10.txt','-dt', Swave_dt) # HZ = 10
            timeSeries('Path',708, '-filePath', f'{TimeSeries_Path}/Swave_Time/New_Time/fs_HZ20.txt','-dt', Swave_dt) # HZ = 20
            timeSeries('Path',709, '-filePath', f'{TimeSeries_Path}/Swave_Time/New_Time/fs_HZ40.txt','-dt', Swave_dt) # HZ = 40
            timeSeries('Path',710, '-filePath', f'{TimeSeries_Path}/Swave_Time/New_Time/fs_HZ80.txt','-dt', Swave_dt) # HZ = 80


            pattern('Plain',703, TimeSeries_Num) # TimeSeries_Num
            # ------------- P wave -----------------------------
            for o in range(nx):
                eleLoad('-ele', BeamEle_Start+o, '-type','-beamUniform',20*1e4,0) 

            # # ------------- S wave -----------------------------
            # for o in range(nx):
            #     eleLoad('-ele', BeamEle_Start+o, '-type','-beamUniform',0,20*1e4,0)


            # -------------- Recorder --------------------------------
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

            # # ====surface Left 1/4 node ======================================
            # recorder('Element', '-file', f'{path2}/ele{UpperrE_LQuarter}.out', '-time', '-ele',UpperrE_LQuarter, 'material ',1,'stresses')
            # recorder('Node', '-file', f'{path1}/node{UpperrN_LQuarter}.out', '-time', '-node',UpperrN_LQuarter,'-dof',1,2,3,'vel')

            # # ====surface Right 1/4 node ======================================
            # recorder('Element', '-file', f'{path2}/ele{UpperrE_RQuarter}.out', '-time', '-ele',UpperrE_RQuarter, 'material ',1,'stresses')
            # recorder('Node', '-file', f'{path1}/node{UpperrN_RQuarter}.out', '-time', '-node',UpperrN_RQuarter,'-dof',1,2,3,'vel')

            system("UmfPack") 
            numberer("RCM")
            constraints("Transformation")

            integrator("Newmark", 0.5, (1/6)) # NewMark, (Constant), 0.5, 0.25 / (Linear),  0.5, (1/6)

            algorithm("Newton") # Newton For Intrgeator = "NewMark"
            test('EnergyIncr',1e-8, 200)
            analysis("Transient")
            analyze(int(analystep),dt)
            print("finish analyze:0 ~ 0.8s")

            # --------- end to calculate time -------------
            end = time.time()
            print(end - start)
