wipe
# ================== Build quad element with block2D ================================
model BasicBuilder -ndm 2 -ndf 2
set nx 6    ;# X-dri elements 
set ny 100  ;# Y-dir elements
set e1 1    ;# from which element start
set n1 1    ;# from which node start  
# ------------------ quad element (node 1~707)-----------------------------------------
#                           $matTag   $E           $v    $rho
nDMaterial ElasticIsotropic  2000    15005714.286  0.3   2020 
block2D $nx $ny $e1 $n1 quad "1 PlaneStrain 2000" {
    1 0   0
    2 0.6 0
    3 0.6 10
    4 0   10 
} 
# print -node 358

# ------------------ B.C(left/right equal); (free inside) ------------------------
set n 100
for {set i 0} {$i < [expr $n+1]} {incr i} { 
    equalDOF [expr 7*$i+1] [expr 7*$i+2] 1 2
    # equalDOF [expr 7*$i+6] [expr 7*$i+7] 1 2
    equalDOF [expr 7*$i+2] [expr 7*$i+3] 1 2
    equalDOF [expr 7*$i+3] [expr 7*$i+4] 1 2
    equalDOF [expr 7*$i+4] [expr 7*$i+5] 1 2
    equalDOF [expr 7*$i+5] [expr 7*$i+6] 1 2
    equalDOF [expr 7*$i+6] [expr 7*$i+7] 1 2
}
# print -ele 600
# ================== Build Beam element(node 708~714) ================================
model BasicBuilder -ndm 2 -ndf 3
for {set j 0} {$j < 7} {incr j} {
    node [expr 708+$j] [expr 0.1*$j] 0.0
}
# ------------------ elastic BeamColumn element ------------------------
set A [expr 0.1*1]
set E1 1e+05;                      # bigger much harder(1e+05) / smaller much softer (1e-06)
set Iz [expr (0.1*0.1*0.1)/12]
geomTransf Linear 1

# for {set k 0} {$k < 6} {incr k} {   ;# ele 605~610  
#     #                        eleTag   i   j
#     element elasticBeamColumn [expr 605+$k] [expr 708+$k] [expr 709+$k]  $A  $E1 $Iz 1 ;# -release 3
#     # puts "[expr 605+$k] ,[expr 708+$k], [expr 709+$k]"
# }
element elasticBeamColumn 605 708 709  $A  $E1 $Iz 1 ;# -release 3
element elasticBeamColumn 606 709 710  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 607 710 711  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 608 711 712  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 609 712 713  $A  $E1 $Iz 1 ;# 
element elasticBeamColumn 610 713 714  $A  $E1 $Iz 1 ;# -release 3

equalDOF 708 709 1 2
equalDOF 713 714 1 2

for {set l 0} {$l < 7} {incr l} {
    equalDOF [expr 708+$l] [expr 1+$l] 1 2
}

# ----------given input force (node 1,2) and "Bottom Stress B.C"---------------------#
set filePath fp.txt
timeSeries Path 702 -dt 0.0001 -filePath $filePath;                                     #10(m)/100=0.1(s); 0.1/100 cell=0.001(s); 0.001/10 steps=0.0001(s)
set p [expr (2.0/7.0)]
pattern Plain 703 702 {
    load 708 0 $p 0
    load 709 0 $p 0
    load 710 0 $p 0
    load 711 0 $p 0
    load 712 0 $p 0
    load 713 0 $p 0
    load 714 0 $p 0
    # eleLoad -ele 605 -type -beamUniform [expr (20.0/6.0)] 0
    # eleLoad -ele 606 -type -beamUniform [expr (20.0/6.0)] 0
    # eleLoad -ele 607 -type -beamUniform [expr (20.0/6.0)] 0
    # eleLoad -ele 608 -type -beamUniform [expr (20.0/6.0)] 0
    # eleLoad -ele 609 -type -beamUniform [expr (20.0/6.0)] 0
    # eleLoad -ele 610 -type -beamUniform [expr (20.0/6.0)] 0
}
puts "finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)" 

# file mkdir extend_soil;
# file mkdir extend_soil/velocity
# file mkdir extend_soil/stress

#----------Left B.C -----------------------
recorder Element -file "extend_soil/stress/ele1_stress.out" -time -ele 1 material 1 stress
recorder Element -file "extend_soil/stress/ele301_stress.out" -time -ele 301 material 1 stress
recorder Element -file "extend_soil/stress/ele595_stress.out" -time -ele 595 material 1 stress

recorder Node -file "extend_soil/velocity/node1_vel.out" -time -node 1 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node351_vel.out" -time -node 351 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node701_vel.out" -time -node 701 -dof 1 2 3 vel;

#----------Right B.C -----------------------
recorder Element -file "extend_soil/stress/ele6_stress.out" -time -ele 6 material 1 stress
recorder Element -file "extend_soil/stress/ele306_stress.out" -time -ele 306 material 1 stress
recorder Element -file "extend_soil/stress/ele600_stress.out" -time -ele 600 material 1 stress

recorder Node -file "extend_soil/velocity/node7_vel.out" -time -node 7 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node357_vel.out" -time -node 357 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node707_vel.out" -time -node 707 -dof 1 2 3 vel;

#----------Center Element/Node -----------------------
recorder Element -file "extend_soil/stress/ele3_stress.out" -time -ele 3 material 1 stress
recorder Element -file "extend_soil/stress/ele303_stress.out" -time -ele 303 material 1 stress
recorder Element -file "extend_soil/stress/ele597_stress.out" -time -ele 597 material 1 stress

recorder Node -file "extend_soil/velocity/node4_vel.out" -time -node 4 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node354_vel.out" -time -node 354 -dof 1 2 3 vel;
recorder Node -file "extend_soil/velocity/node704_vel.out" -time -node 704 -dof 1 2 3 vel;

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
