wipe
# ================== Build quad element with block2D ================================
model BasicBuilder -ndm 2 -ndf 2
set nx 7    ;# X-dri elements 
set ny 100  ;# Y-dir elements
set e1 1    ;# from which element start
set n1 1    ;# from which node start  

# ------------------ quad element (node 1~808)-----------------------------------------
#                           $matTag   $E           $v    $rho
nDMaterial ElasticIsotropic  2000    15005714.286  0.3   2020  ;# E:unit -> Pa
block2D $nx $ny $e1 $n1 quad "1 PlaneStrain 2000" {
    1 0   0
    2 0.7  0
    3 0.7 10
    4 0   10 
}

set n 100
for {set i 0} {$i < [expr $n+1]} {incr i} { 
    #---- tie B.C : Only Left and Right node have same disp x,y----------
    equalDOF [expr ($nx+1)*$i+1] [expr ($nx+1)*$i+8] 1 2
    #---- much rigorous way to each node have same disp -------
    # equalDOF [expr 6*$i+1] [expr 6*$i+2] 1 2
    # equalDOF [expr 6*$i+2] [expr 6*$i+3] 1 2
    # equalDOF [expr 6*$i+3] [expr 6*$i+4] 1 2
    # equalDOF [expr 6*$i+4] [expr 6*$i+5] 1 2
    # equalDOF [expr 6*$i+5] [expr 6*$i+6] 1 2
}
# print -node 808 
# ==================== Build Beam element (node 810~817)-----------------------------------------
model BasicBuilder -ndm 2 -ndf 3
for {set j 0} {$j < $nx+1} {incr j} {
    node [expr 810+$j] [expr 0.1*$j] 0.0
    mass [expr 810+$j] 1 1 1
    fix [expr 810+$j] 0 0 1
}

# ------------------ elastic BeamColumn element: ele 701~707 ------------------------
set A [expr 0.1*1]
set E1 1e+05;                      # bigger much harder(1e+05) / smaller much softer (1e-06)
set Iz [expr (0.1*0.1*0.1)/12]
geomTransf Linear 1

element elasticBeamColumn 701 810 811  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 702 811 812  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 703 812 813  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 704 813 814  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 705 814 815  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 706 815 816  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 707 816 817  $A  $E1 $Iz 1 ;# 
# ------------------- Beam equalDOF: same x,y disp --------------------
equalDOF 810 817 1 2

#---------- Bottom Beam and Soil connect ------------------------
for {set l 0} {$l < $nx+1} {incr l} {
    equalDOF [expr 810+$l] [expr 1+$l] 1 2
}

# ============================ Beam element dashpot =============================== #
for {set k 0} {$k < $nx+1} {incr k} {
# ------------- traction dashpot (node 818,819~ 832,833)------------
    node [expr 818+2*$k] [expr 0.1*$k] 0.0
    node [expr 819+2*$k] [expr 0.1*$k] 0.0
# ---------- dashpot dir: cp -> y dir; cs -> x dir ---------------------     
    fix [expr 818+2*$k] 0 1 1  ;# x dir dashpot　
    fix [expr 819+2*$k] 1 1 1  

# ------------- Normal dashpot (node 834,835~ 848,849) ------------
    node [expr 834+2*$k] [expr 0.1*$k] 0.0
    node [expr 835+2*$k] [expr 0.1*$k] 0.0
    fix [expr 834+2*$k] 1 0 1  ;# y dir dashpot　
    fix [expr 835+2*$k] 1 1 1  
}
# # ------ connect dashpot with BEAM bot layer :Vs with x dir / Vp with y-dir --------------
# --------------traction dashpot------------------
equalDOF 810 818 1
equalDOF 811 820 1
equalDOF 812 822 1
equalDOF 813 824 1
equalDOF 814 826 1
equalDOF 815 828 1
equalDOF 816 830 1
equalDOF 817 832 1
# --------------Normal dashpot------------------
equalDOF 810 834 2
equalDOF 811 836 2
equalDOF 812 838 2
equalDOF 813 840 2
equalDOF 814 842 2
equalDOF 815 844 2
equalDOF 816 846 2
equalDOF 817 848 2
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
# #----------- dashpot elements: Vs with x dir / Vp with y-dir------------------
set xdir 1
set ydir 2
element zeroLength 800 819 818 -mat 4003 -dir $xdir ;# node 1: Left side
element zeroLength 801 821 820 -mat 4003 -dir $xdir ;
element zeroLength 803 823 822 -mat 4003 -dir $xdir ;
element zeroLength 804 825 824 -mat 4003 -dir $xdir ;
element zeroLength 805 827 826 -mat 4003 -dir $xdir ;
element zeroLength 806 829 828 -mat 4003 -dir $xdir ;
element zeroLength 807 831 830 -mat 4003 -dir $xdir ;
element zeroLength 808 833 832 -mat 4003 -dir $xdir ;# node 8: Right side

element zeroLength 809 835 834 -mat 4002 -dir $ydir ;# node 1: Left side
element zeroLength 810 837 836 -mat 4002 -dir $ydir ;
element zeroLength 811 839 838 -mat 4002 -dir $ydir ;
element zeroLength 812 841 840 -mat 4002 -dir $ydir ;
element zeroLength 813 843 842 -mat 4002 -dir $ydir ;
element zeroLength 814 845 844 -mat 4002 -dir $ydir ;
element zeroLength 815 847 846 -mat 4002 -dir $ydir ;
element zeroLength 816 849 848 -mat 4002 -dir $ydir ;# node 8: Right side
puts "Finished creating dashpot material and element..."

# # ================= Apply Distributed Load at Beam element ==========================
# ----------given input force (node 1,2) and "Bottom Stress B.C"---------------------#
set filePath fs.txt   ;# fp.txt/ fs.txt
timeSeries Path 702 -dt 0.0001 -filePath $filePath;        #10(m)/100=0.1(s); 0.1/100 cell=0.001(s); 0.001/10 steps=0.0001(s)

set p [expr (2.0/($nx+1))]
set Stress 20.0  ;#20.0

pattern Plain 703 702 {
    #-------------  S wave -------------------------
    # load 810 $p 0 0
    # load 811 $p 0 0
    # load 812 $p 0 0
    # load 813 $p 0 0
    # load 814 $p 0 0
    # load 815 $p 0 0
    # load 816 $p 0 0
    # load 817 $p 0 0
    eleLoad -ele 701 -type -beamUniform 0 20 0
    eleLoad -ele 702 -type -beamUniform 0 20 0
    eleLoad -ele 703 -type -beamUniform 0 20 0
    eleLoad -ele 704 -type -beamUniform 0 20 0
    eleLoad -ele 705 -type -beamUniform 0 20 0
    eleLoad -ele 706 -type -beamUniform 0 20 0
    eleLoad -ele 707 -type -beamUniform 0 20 0

#-------------  P wave ------------------------- 
    # load 810 0 $p 0
    # load 811 0 $p 0
    # load 812 0 $p 0
    # load 813 0 $p 0
    # load 814 0 $p 0
    # load 815 0 $p 0
    # load 816 0 $p 0
    # load 817 0 $p 0
    
    # eleLoad -ele 701 -type -beamUniform  20 0
    # eleLoad -ele 702 -type -beamUniform  20 0
    # eleLoad -ele 703 -type -beamUniform  20 0
    # eleLoad -ele 704 -type -beamUniform  20 0
    # eleLoad -ele 705 -type -beamUniform  20 0
    # eleLoad -ele 706 -type -beamUniform  20 0
    # eleLoad -ele 707 -type -beamUniform0 20 0
}
puts "finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)" 

# print -ele 697
# ---------- Left B.C -----------------------
recorder Element -file "extend_soil/stress/ele1_stress.out" -time -ele 1 material 1 stress
recorder Element -file "extend_soil/stress/ele351_stress.out" -time -ele 351 material 1 stress
recorder Element -file "extend_soil/stress/ele694_stress.out" -time -ele 694 material 1 stress

recorder Node -file "extend_soil/velocity/node1_vel.out" -time -node 1 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node401_vel.out" -time -node 401 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node801_vel.out" -time -node 801 -dof 1 2 3 vel;

#---------- Right B.C -----------------------
recorder Element -file "extend_soil/stress/ele7_stress.out" -time -ele 7 material 1 stress
recorder Element -file "extend_soil/stress/ele357_stress.out" -time -ele 357 material 1 stress
recorder Element -file "extend_soil/stress/ele700_stress.out" -time -ele 700 material 1 stress

recorder Node -file "extend_soil/velocity/node8_vel.out" -time -node 8 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node408_vel.out" -time -node 408 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node808_vel.out" -time -node 808 -dof 1 2 3 vel;

#---------- Center Element/Node -----------------------
recorder Element -file "extend_soil/stress/ele4_stress.out" -time -ele 4 material 1 stress
recorder Element -file "extend_soil/stress/ele354_stress.out" -time -ele 354 material 1 stress
recorder Element -file "extend_soil/stress/ele697_stress.out" -time -ele 697 material 1 stress

recorder Node -file "extend_soil/velocity/node4_vel.out" -time -node 4 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node404_vel.out" -time -node 404 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node804_vel.out" -time -node 804 -dof 1 2 3 vel;

# # ---------- Structure stress/velocity -----------------------
# recorder Element -file "extend_soil/stress/Column1_stress.out" -time -ele 611 globalForce
# recorder Element -file "extend_soil/stress/Column2_stress.out" -time -ele 612 globalForce
# recorder Element -file "extend_soil/stress/Beam_stress.out" -time -ele 613 globalForce

# recorder Node -file "extend_soil/velocity/node1030_vel.out" -time -node 1030 -dof 1 2 3 vel;
# recorder Node -file "extend_soil/velocity/node1031_vel.out" -time -node 1031 -dof 1 2 3 vel;
# recorder Node -file "extend_soil/velocity/node1032_vel.out" -time -node 1032 -dof 1 2 3 vel;
# recorder Node -file "extend_soil/velocity/node1033_vel.out" -time -node 1033 -dof 1 2 3 vel;

# ============= recorder MPCO HDF5 ====================
# recorder mpco "extend_soil/MPCO/allele" -E material.stress force localforce -N velocity ;#
# recorder mpco "extend_soil/MPCO/Pwave_dahpot" -E material.stress force localforce -N velocity displacement ;#
# recorder mpco "extend_soil/MPCO/Swave_sideBC" -E material.stress force localforce -N velocity displacement ;#

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
