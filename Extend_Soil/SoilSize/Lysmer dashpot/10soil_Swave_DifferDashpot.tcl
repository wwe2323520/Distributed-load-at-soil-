wipe
# ================== Build quad element with block2D ================================
model BasicBuilder -ndm 2 -ndf 2
set nx 100    ;# X-dri elements 
set ny 100  ;# Y-dir elements
set e1 1    ;# from which element start
set n1 1    ;# from which node start  

# ------------------ quad element (node 1~10201)-----------------------------------------
#                           $matTag   $E           $v    $rho
nDMaterial ElasticIsotropic  2000    15005714.286  0.3   2020  ;# E:unit -> Pa
block2D $nx $ny $e1 $n1 quad "1 PlaneStrain 2000" {
    1 0.0   0.0
    2 10.0  0.0
    3 10.0  10.0
    4 0.0   10.0 
}
set n 100
for {set i 0} {$i < [expr $n+1]} {incr i} { 
    #---- tie B.C : Only Left and Right node have same disp x,y----------
    equalDOF [expr ($nx+1)*$i+1] [expr ($nx+1)*$i+101] 1 2
    #---- much rigorous way to each node have same disp -------
    # equalDOF [expr 6*$i+1] [expr 6*$i+2] 1 2
    # equalDOF [expr 6*$i+2] [expr 6*$i+3] 1 2
    # equalDOF [expr 6*$i+3] [expr 6*$i+4] 1 2
    # equalDOF [expr 6*$i+4] [expr 6*$i+5] 1 2
    # equalDOF [expr 6*$i+5] [expr 6*$i+6] 1 2
}
# print -node 808 
# ==================== Build Beam element (node 10202~10302)-----------------------------------------
model BasicBuilder -ndm 2 -ndf 3
for {set j 0} {$j < $nx+1} {incr j} {
    node [expr 10202+$j] [expr 0.1*$j] 0.0
    mass [expr 10202+$j] 1 1 1
    fix [expr 10202+$j] 0 0 1
}
# # --------  simple beam setting -----------------
# for {set j 0} {$j < 4} {incr j} {
#     fix [expr 2*$j+810] 1 1 1     ;# even: pin support
#     fix [expr 2*$j+811] 0 1 1     ;# odd : roller support
# }

# # for {set j 0} {$j < 7} {incr j} {
# #     equalDOF 810 [expr 811+$j] 1 2
# #     # puts "810 ,[expr 811+$j]"
# # }
# ------------------- Beam equalDOF: same x,y disp --------------------
equalDOF 10202 10302 1 2

# ------------------ elastic BeamColumn element (100 ele:10001~10100)------------------------
set A [expr 0.1*1]
set E1 1e+05;                      # bigger much harder(1e+05) / smaller much softer (1e-06)
set Iz [expr (0.1*0.1*0.1)/12]
geomTransf Linear 1

for {set k 0} {$k < $nx} {incr k} {
    element elasticBeamColumn [expr 10001+$k] [expr 10202+$k] [expr 10203+$k]  $A  $E1 $Iz 1 ;# 
}

#---------- Bottom Beam and Soil connect ------------------------
for {set l 0} {$l < $nx+1} {incr l} {
    equalDOF [expr 10202+$l] [expr 1+$l] 1 2
}
# ============================ Beam element dashpot =============================== #
for {set k 0} {$k < $nx+1} {incr k} {
# ------------- traction dashpot (node 10303,10304, 10503,10504)------------
    node [expr 10303+2*$k] [expr 0.1*$k] 0.0
    node [expr 10304+2*$k] [expr 0.1*$k] 0.0
# ---------- dashpot dir: cp -> y dir; cs -> x dir ---------------------     
    fix [expr 10303+2*$k] 0 1 1  ;# x dir dashpot　
    fix [expr 10304+2*$k] 1 1 1  
# ------------- Normal dashpot (node 10505,10506~ 10705,10706) ------------
    node [expr 10505+2*$k] [expr 0.1*$k] 0.0
    node [expr 10506+2*$k] [expr 0.1*$k] 0.0
    fix [expr 10505+2*$k] 1 0 1  ;# y dir dashpot　
    fix [expr 10506+2*$k] 1 1 1 
}
# ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
# --------------traction dashpot------------------
for {set k 0} {$k < $nx+1} {incr k} {
# ------- traction dashpot --------------
    equalDOF [expr 10202+$k] [expr 10303+2*$k] 1
# ------- Normal dashpot --------------
    equalDOF [expr 10202+$k] [expr 10505+2*$k] 2
}
puts "Finished creating all dashpot boundary conditions and equalDOF..."
# ------------------- ZeroLength to Build dashpot: Material ----------------------------------
set rho 2020   ;# kg/m3 
set Vp 100     ;# m/s 
set Vs 53.45224838248488     ;# m/s 
set sizeX 0.1  ;# m
set Smp  [expr 0.5*$rho*$Vp*$sizeX]  ;# Side node dashpot :N (newton)
set Sms  [expr 0.5*$rho*$Vs*$sizeX]  ;# Side node dashpot :N (newton)
set Cmp  [expr $rho*$Vp*$sizeX]  ;# Center node dashpot :N (newton)
set Cms  [expr $rho*$Vs*$sizeX]  ;# Center node dashpot :N (newton)

uniaxialMaterial Viscous 4000 $Smp 1   ;# P wave: Side node
uniaxialMaterial Viscous 4001 $Sms 1   ;# S wave: Side node

uniaxialMaterial Viscous 4002 $Cmp 1   ;# P wave: Center node
uniaxialMaterial Viscous 4003 $Cms 1   ;# S wave: Center node
#----------- dashpot elements: Vs with x dir / Vp with y-dir------------------
set xdir 1
set ydir 2
# ---- traction dashpot element ---(left and right)
element zeroLength 20000 10304 10303 -mat 4001 -dir $xdir
element zeroLength 20100 10504 10503 -mat 4001 -dir $xdir
# ---- Normal dashpot element ---(left and right)
element zeroLength 20101 10506 10505 -mat 4000 -dir $ydir
element zeroLength 20201 10706 10705 -mat 4000 -dir $ydir

for {set m 1} {$m < $nx} {incr m} {
# -------------- traction dashpot element(ele 20001~20099) -----------------------
    element zeroLength [expr 20000+$m] [expr 10304+2*$m] [expr 10303+2*$m] -mat 4003 -dir $xdir
    # puts "[expr 20000+$m] ,[expr 10304+2*$m] ,[expr 10303+2*$m]"
# -------------- Normal dashpot element (ele 20102~20200)-----------------------
    element zeroLength [expr 20101+$m] [expr 10506+2*$m] [expr 10505+2*$m] -mat 4002 -dir $ydir
    # puts "[expr 20101+$m] ,[expr 10506+2*$m] ,[expr 10505+2*$m]"
}
puts "Finished creating dashpot material and element..."
# ================= Apply Distributed Load at Beam element ==========================
# ----------given input force (node 1,2) and "Bottom Stress B.C"---------------------#
set filePath fs.txt   ;# fp2.txt/ fs.txt
timeSeries Path 705 -dt 0.0001 -filePath $filePath;        #10(m)/100=0.1(s); 0.1/100 cell=0.001(s); 0.001/10 steps=0.0001(s)

set p [expr (2.0/($nx+1))]
set Stress 20.0  ;#20.0

pattern Plain 703 705 {
#-------------  S wave -------------------------
    # load 810 $p 0 0
    # load 811 $p 0 0
    # load 812 $p 0 0
    # load 813 $p 0 0
    # load 814 $p 0 0
    # load 815 $p 0 0
    # load 816 $p 0 0
    # load 817 $p 0 0
    for {set u 0} {$u < $nx} {incr u} {
        eleLoad -ele [expr 10001+$u] -type -beamUniform 0 20 0
    }
#-------------  P wave ------------------------- 
    # load 810 0 $p 0
    # load 811 0 $p 0
    # load 812 0 $p 0
    # load 813 0 $p 0
    # load 814 0 $p 0
    # load 815 0 $p 0
    # load 816 0 $p 0
    # load 817 0 $p 0
    # for {set u 0} {$u < $nx} {incr u} {
    #     eleLoad -ele [expr 10001+$u] -type -beamUniform 20 0
    # }

}
puts "finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)" 

# print -node 10201
# print -ele 10000
# ---------- Left B.C (ele 1,5001,9901 / node 1,5051 10101) -----------------------
recorder Element -file "Stress/10msoil/ele1_stress_S.out" -time -ele 1 material 1 stress
recorder Element -file "Stress/10msoil/ele5001_stress_S.out" -time -ele 5001 material 1 stress
recorder Element -file "Stress/10msoil/ele9901_stress_S.out" -time -ele 9901 material 1 stress

recorder Node -file "Velocity/10msoil/node1_vel_S.out" -time -node 1 -dof 1 2 3 vel;
recorder Node -file "Velocity/10msoil/node5051_vel_S.out" -time -node 5051 -dof 1 2 3 vel;
recorder Node -file "Velocity/10msoil/node10101_vel_S.out" -time -node 10101 -dof 1 2 3 vel;

#---------- Right B.C (ele 100,5100,10000 / node 101,5151 10201)-----------------------
recorder Element -file "Stress/10msoil/ele100_stress_S.out" -time -ele 100 material 1 stress
recorder Element -file "Stress/10msoil/ele5100_stress_S.out" -time -ele 5100 material 1 stress
recorder Element -file "Stress/10msoil/ele10000_stress_S.out" -time -ele 10000 material 1 stress

recorder Node -file "Velocity/10msoil/node101_vel_S.out" -time -node 101 -dof 1 2 3 vel;
recorder Node -file "Velocity/10msoil/node5151_vel_S.out" -time -node 5151 -dof 1 2 3 vel;
recorder Node -file "Velocity/10msoil/node10201_vel_S.out" -time -node 10201 -dof 1 2 3 vel;

#---------- Center Element/Node (ele 51,5051,9951 / node 51,5101,10151) -----------------------
recorder Element -file "Stress/10msoil/ele51_stress_S.out" -time -ele 51 material 1 stress
recorder Element -file "Stress/10msoil/ele5051_stress_S.out" -time -ele 5051 material 1 stress
recorder Element -file "Stress/10msoil/ele9951_stress_S.out" -time -ele 9951 material 1 stress

recorder Node -file "Velocity/10msoil/node51_vel_S.out" -time -node 51 -dof 1 2 3 vel;
recorder Node -file "Velocity/10msoil/node5101_vel_S.out" -time -node 5101 -dof 1 2 3 vel;
recorder Node -file "Velocity/10msoil/node10151_vel_S.out" -time -node 10151 -dof 1 2 3 vel;

# # # ---------- Structure stress/velocity -----------------------
# # recorder Element -file "extend_soil/stress/Column1_stress.out" -time -ele 611 globalForce
# # recorder Element -file "extend_soil/stress/Column2_stress.out" -time -ele 612 globalForce
# # recorder Element -file "extend_soil/stress/Beam_stress.out" -time -ele 613 globalForce

# # recorder Node -file "extend_soil/velocity/node1030_vel.out" -time -node 1030 -dof 1 2 3 vel;
# # recorder Node -file "extend_soil/velocity/node1031_vel.out" -time -node 1031 -dof 1 2 3 vel;
# # recorder Node -file "extend_soil/velocity/node1032_vel.out" -time -node 1032 -dof 1 2 3 vel;
# # recorder Node -file "extend_soil/velocity/node1033_vel.out" -time -node 1033 -dof 1 2 3 vel;

# # ============= recorder MPCO HDF5 ====================
# # recorder mpco "extend_soil/MPCO/allele" -E material.stress force localforce -N velocity ;#
# # recorder mpco "extend_soil/MPCO/Pwave_dahpot" -E material.stress force localforce -N velocity displacement ;#
# # recorder mpco "extend_soil/MPCO/Swave_sideBC" -E material.stress force localforce -N velocity displacement ;#

#dynamic analysis
constraints Transformation
numberer RCM
system UmfPack
test EnergyIncr 1.0e-8 200; #1.0e-6 200
algorithm Newton
integrator Newmark 0.5 0.25
analysis Transient
analyze 8000 0.0001; #total time: 0.8s
puts "finish analyze:0 ~ 0.8s"

# print -ele 701 702 703 704 705 706 707
