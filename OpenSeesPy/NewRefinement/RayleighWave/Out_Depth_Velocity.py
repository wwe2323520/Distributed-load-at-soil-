# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 22:03:39 2023

@author: User
"""
import numpy as np
import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
from matplotlib.ticker import ScalarFormatter
from matplotlib import pyplot as plt, ticker as mticker
import scipy.signal
from scipy.signal import find_peaks

start = time.time()

pi = np.pi
plt.rc('font', family= 'Times New Roman')

# a_cofficient = np.arange(0.0, 2.0+0.2, 0.2)
# b_cofficient = np.arange(0.0, 2.0+0.2, 0.2)

soilWidth = 10.0
SoilDepth = 10.0 
DW = 0.125
nx = int(soilWidth/DW)
ny = 80

yMesh = SoilDepth/ny
#------------- Read file ---------------------
def rdnumpy(textname):
    f = open(textname)
    line = f.readlines()
    lines = len(line)
    for l in line:
        le = l.strip('\n').split(' ')
        columns = len(le)
    
    A = np.zeros((lines, columns), dtype = float)
    A_row = 0
    
    for lin in line:
        list = lin.strip('\n').split(' ')
        A[A_row:] = list[0:columns]
        A_row += 1
    return A

# --------- Tie Boundary Condition ----------------
fileNumber = 0
# for a in range(len(a_cofficient)):
#     akz = a_cofficient[a]
#     for b in range(len(b_cofficient)):
#         fileNumber = fileNumber + 1
#         bkz = b_cofficient[b]

        # file[fileNumber] = 
a_cofficient = np.arange(0.0, 0.2+0.2, 0.2)
b_cofficient = np.arange(0.0, 0.2+0.2, 0.2)

for akz in a_cofficient:
    for bkz in b_cofficient:
        a = round(akz, 2)
        b = round(bkz, 2)
        print(f'a_Cofficient = {a} ; b_Cofficient = {b} ')
        file_paths = []
        file = []
        for o in range(ny+1):
        # ---------------- Left Side ------------
            Depth = yMesh*o 
            LeftNode = int(1 + (nx+1)*o)
            file_paths.append(f"E:/unAnalysisFile/RayleighDashpot/Tie/Ca{a}_Cb{b}/Velocity/D{Depth}_Lnode{LeftNode}.out")
           
            name =  f'D{Depth}_Lnode{LeftNode}'
            file.append(name)
        # ---------------- Center Side ------------
        for o in range(ny+1):
            Depth = yMesh*o 
            CenterNode = int((1 + (nx/2)) + (nx+1)*o)
            file_paths.append(f"E:/unAnalysisFile/RayleighDashpot/Tie/Ca{a}_Cb{b}/Velocity/D{Depth}_Cnode{CenterNode}.out")
            name =  f'D{Depth}_Cnode{CenterNode}'
            file.append(name)
        
        # ---------------- Right Side ------------
        for o in range(ny+1):
            Depth = yMesh*o 
            RightNode = int((1+nx)+ (nx+1)*o)
            file_paths.append(f"E:/unAnalysisFile/RayleighDashpot/Tie/Ca{a}_Cb{b}/Velocity/D{Depth}_Rnode{RightNode}.out")
            name =  f'D{Depth}_Rnode{RightNode}'
            file.append(name)
            
        for size in range(len(file)): #
            file[size] = rdnumpy(file_paths[size]) # Convert File into array
        
        
        #===================== Make x - Vx Matrix (each depth) =====================
        # ----------------- Depth amd Time Matrix -------------------------
        surfaceID = ny
        Depth_Array = np.arange(0.0, SoilDepth+yMesh, yMesh)
        
        Total_Time = []
        Dstep = 10 # Contol TimeStep*******
        TotalStep = int(len(file[0][:,0])/Dstep)
        
        for i in range(TotalStep+1):
            t = i
            if i > 0:    
                t = 10*i-1    
            Total_Time.append(file[0][t,0])
           
        # ----------------- Grab each Depth and Velocity Data -------------------------
        LDep_Vel = np.zeros((ny+1,len(Total_Time)+1))
        CDep_Vel = np.zeros((ny+1,len(Total_Time)+1))
        RDep_Vel = np.zeros((ny+1,len(Total_Time)+1))
        
        LDep_Vel[:,0] = Depth_Array[:]
        CDep_Vel[:,0] = Depth_Array[:]
        RDep_Vel[:,0] = Depth_Array[:]
        
        CDepId = ny+1 
        RDepId = 2*(ny+1) 
        
        # ------------- Left / Center / Column Differ Depth vs Velocity y Store
        Vdir = 2 ## Velocity Direction
        for i in range(TotalStep+1):     #TotalStep+1
            if i == 0:    
                t = i
                for Dep in range(len(Depth_Array)):
                    LDep_Vel[Dep, 1] = file[Dep][t][Vdir] 
                    CDep_Vel[Dep, 1] = file[CDepId+Dep][t][Vdir] 
                    RDep_Vel[Dep, 1] = file[RDepId+Dep][t][Vdir]
        
            if i > 0:
                t = (10*i) - 1
                for Dep in range(len(Depth_Array)):
                    LDep_Vel[Dep, i+1] = file[Dep][t][Vdir] 
                    CDep_Vel[Dep, i+1] = file[CDepId+Dep][t][Vdir] 
                    RDep_Vel[Dep, i+1] = file[RDepId+Dep][t][Vdir]
                    
        # plt.plot(Dep_Vel[:,0], Dep_Vel[:,135])
        # plt.grid(True)
        # ----------------- Build File to Store Image ---------------------------
        output_folder1 = f'E:/unAnalysisFile/RayleighDashpot/W10Tie_Output/a{a}b{b}/LeftColumn'
        os.makedirs(output_folder1, exist_ok=True)
        
        output_folder2 = f'E:/unAnalysisFile/RayleighDashpot/W10Tie_Output/a{a}b{b}/CenterColumn'
        os.makedirs(output_folder2, exist_ok=True)
        
        output_folder3 = f'E:/unAnalysisFile/RayleighDashpot/W10Tie_Output/a{a}b{b}/RightColumn'
        os.makedirs(output_folder3, exist_ok=True)
        
        x_axis = 1
        def draw_Depthh_Velocity(ColumnName, LDep_Vel, output_folder1):
            for pt in range(TotalStep+1):     #TotalStep+1
                plt.figure(figsize= (8,6))
                plt.title(f"{ColumnName} Velocity: t = {Total_Time[pt]}s", fontsize = 20)
                
                plt.xlabel('Depth (m)', fontsize = 20)
                plt.ylabel(r"$\mathrm {Velocity}$  $v_y$  $\mathrm {(m/s)}$", fontsize = 20)
                    
                plt.plot(LDep_Vel[:,0], LDep_Vel[:, 1+pt])
                plt.xlim(0.0, 10.0)
                
                plt.xticks(fontsize = 16)
                plt.yticks(fontsize = 16)
                plt.grid(True)
                
                ax1 = plt.gca()
                ax1.xaxis.set_major_locator(ticker.MultipleLocator(x_axis))
                ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
                ax1.yaxis.get_offset_text().set(size=18)
                
                image_path = os.path.join(output_folder1, f'fig{pt+1}.png')
                plt.savefig(image_path, bbox_inches='tight')
                plt.close()
            print("Images saved to", output_folder1) 
        
        draw_Depthh_Velocity('Left Column', LDep_Vel, output_folder1)
        draw_Depthh_Velocity('Center Column', CDep_Vel, output_folder2)
        draw_Depthh_Velocity('Right Column', RDep_Vel, output_folder3)  
        
            
            
        end = time.time()
        print('Total Time =', end - start)
print('Finish All Cofficient Image Output')
        
        
        
        
