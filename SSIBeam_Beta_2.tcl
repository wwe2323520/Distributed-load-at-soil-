wipe
# print -node 358
# ================== Build Beam element(node 708~714) ================================
model BasicBuilder -ndm 2 -ndf 3
for {set j 0} {$j < 6} {incr j} {
    node [expr 607+$j] [expr 0.1*$j] 0.0
    mass [expr 607+$j] 1 1 1
}
for {set g 0} {$g < 5} {incr g} {
    node [expr 613+$g] [expr 0.05*(2*$g+1)] 0.0
    fix [expr 613+$g] 0 0 1
    mass [expr 613+$g] 1 1 1
}
# fix 607 0 0 1
# fix 608 0 0 1
# fix 609 0 0 1
# fix 610 0 0 1
# fix 611 0 0 1
# fix 612 0 0 1

fix 607 1 1 1
fix 608 0 1 1
fix 609 1 1 1
fix 610 0 1 1
fix 611 1 1 1
fix 612 0 1 1  

# ------------------ elastic BeamColumn element ------------------------
set A [expr 0.1*1]
set E1 1e+05;                      # bigger much harder(1e+05) / smaller much softer (1e-06)
set Iz [expr (0.1*0.1*0.1)/12]
geomTransf Linear 1

# element elasticBeamColumn 500 607 608  $A  $E1 $Iz 1 ;# 
# element elasticBeamColumn 501 608 609  $A  $E1 $Iz 1 ;# 
# element elasticBeamColumn 502 609 610  $A  $E1 $Iz 1 ;# 
# element elasticBeamColumn 503 610 611  $A  $E1 $Iz 1 ;# 
# element elasticBeamColumn 504 611 612  $A  $E1 $Iz 1 ;# 

element elasticBeamColumn 500 607 613  $A  $E1 $Iz 1 ; # 
element elasticBeamColumn 501 613 608  $A  $E1 $Iz 1 ;

element elasticBeamColumn 502 608 614  $A  $E1 $Iz 1 ; # 
element elasticBeamColumn 503 614 609  $A  $E1 $Iz 1 ;

element elasticBeamColumn 504 609 615  $A  $E1 $Iz 1 ; # 
element elasticBeamColumn 505 615 610  $A  $E1 $Iz 1 ;

element elasticBeamColumn 506 610 616  $A  $E1 $Iz 1 ; # 
element elasticBeamColumn 507 616 611  $A  $E1 $Iz 1 ;

element elasticBeamColumn 508 611 617  $A  $E1 $Iz 1 ; # 
element elasticBeamColumn 509 617 612  $A  $E1 $Iz 1 ;

for {set j 0} {$j < 5} {incr j} {
    equalDOF 607 [expr 608+$j]  1 2
}

# equalDOF 607 612 1 2

# ----------given input force (node 1,2) and "Bottom Stress B.C"---------------------#
set filePath fp.txt
timeSeries Path 702 -dt 0.0001 -filePath $filePath;        #10(m)/100=0.1(s); 0.1/100 cell=0.001(s); 0.001/10 steps=0.0001(s)
timeSeries Linear 705 
timeSeries Constant 706 

set p 1
pattern Plain 703 702 {
    load 613 0 0.4 0
    load 614 0 0.4 0
    load 615 0 0.4 0
    load 616 0 0.4 0
    load 617 0 0.4 0
    # eleLoad -ele 500 -type -beamUniform [expr 20/5] 0
    # eleLoad -ele 501 -type -beamUniform [expr 20/5] 0
    # eleLoad -ele 502 -type -beamUniform [expr 20/5] 0
    # eleLoad -ele 503 -type -beamUniform [expr 20/5] 0
    # eleLoad -ele 504 -type -beamUniform [expr 20/5] 0
}
puts "finish Input Force File:0 ~ 0.1s(+1), Inpu Stress B.C:0.2~0.3s(-1)" 

# file mkdir extend_soil;
# file mkdir extend_soil/BeamEle

#----------Beam Element recorder -----------------------

recorder Element -file "extend_soil/BeamEle/ele500_glo.txt" -time -ele 500 globalForce 
recorder Element -file "extend_soil/BeamEle/ele501_glo.txt" -time -ele 501 globalForce 
recorder Element -file "extend_soil/BeamEle/ele502_glo.txt" -time -ele 502 globalForce 
recorder Element -file "extend_soil/BeamEle/ele503_glo.txt" -time -ele 503 globalForce 
recorder Element -file "extend_soil/BeamEle/ele504_glo.txt" -time -ele 504 globalForce 

#dynamic analysis
constraints Transformation
numberer RCM
system UmfPack
test EnergyIncr 1.0e-8 200; #1.0e-6 200
algorithm Newton
integrator Newmark 0.5 0.25
analysis Transient
analyze 10000 0.0001; #total time: 0.8s  8000 0.0001 / 10000 0.0001  
puts "finish analyze:0 ~ 0.8s"

print -ele 500 501 502 503 504
# print -node 607 608 609 610 611 612
