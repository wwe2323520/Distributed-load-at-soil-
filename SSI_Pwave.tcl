wipe
model BasicBuilder -ndm 2 -ndf 2

#================================ Built Node：Global id======================================#
set b [expr 10.0/100.0]; #0.1
set n 100

for { set i 0} {$i <[expr $n+1]} {incr i} { ;#{$i <[expr $n+1]}
    #       id         x    y 
    node [expr 2*$i+1] 0.0  [expr $i*$b]; # 1.3.5.7-201
    node [expr 2*$i+2] $b [expr $i*$b]; # 2.4.6.8-202
}
#======================== Built Material and Quad element：===========================================#
#                           $matTag   $E          $v    $rho
nDMaterial ElasticIsotropic  2000   15005714.286  0.3   2020    ;  # E=15005714.286#1600,vp =100, vs=53.452 ,E=11885714.286, G=4571428.571 n/m2, rho= 1600 kg/m3=1.6 ton/m3
for { set a 0} {$a < $n} {incr a} {
    #                eletag                i              j             k           l                         
    element quad [expr $a+1]     [expr 2*$a+1] [expr 2*$a+2] [expr 2*$a+4] [expr 2*$a+3] 1 "PlaneStress" 2000   
}
#========================== Boundary Condition =========================================#
# fix 1 0 1
# fix 2 0 1
for {set i 0} {$i <[expr $n+1]} {incr i} {      ;#node 3~202 same Disp
    equalDOF  [expr 2*$i+1] [expr 2*$i+2] 1 2;
}
#========================== Force Input: Sin(Wst) TimeSeries =============================#
set filePath u1.txt
timeSeries Path 702 -dt 1e-4 -filePath $filePath;       #10(m)/100=0.1(s); 0.1/100 cell=0.001(s); 0.001/10 steps=0.0001(s)
pattern Plain 703 702 {
    load 1 1 0;                                             # like "normal vector direction"
    load 2 1 0; 
}
puts "finish Input Force File:0 ~ 0.187s(+1), Input Stress B.C:0.374s(-1)" 

#================================ Try Absorbing B.C Element ===============================#
# set G 5771428.571428572
# set rho 2020
# element ASDAbsorbingBoundary2D 105 1 2 4 3 $G 0.3 $rho 1  B

#========================== Force 2 Input:velocity timeseries to make wave transport and Input velocity boundary(node 1,2) ==#
# # MultipleSupport SineWave ground motion (different velocity input at spec'd support nodes) -- two nodes here
# set iSupportNode "1 2";			# support nodes where ground motions are input, for multiple-support excitation
# set iGMdirection "1 1";			# ground-motion direction  -- for each support node
#---------------------------------    perform Dynamic Ground-Motion Analysis------------#
# set filePath2 disp.txt;                                   #v1.txt
# set dt 1e-4;                                            #1e-4
# timeSeries Path 704 -dt $dt -filePath $filePath2; #1e-4

# # the following commands are unique to the Multiple-Support Earthquake excitation
# set IDloadTag 705;	
# set IDgmSeries 706;	    # for multipleSupport Excitation
# set DtGround $dt;	# time-step Dt for input grond motion 0.0001
# # multiple-support excitation: velocity input at individual nodes
# pattern MultipleSupport $IDloadTag  {
# 	foreach SupportNode $iSupportNode GMdirection $iGMdirection {
# 		set IDgmSeries [expr $IDgmSeries +1]

# 		groundMotion $IDgmSeries Plain -disp 704 -int Simpson; #Simpson/Trapezoidal
# 	     	imposedMotion $SupportNode  $GMdirection $IDgmSeries
# 	};	# end foreach	
# };	# end pattern
# puts "finish velocity File:0.0 ~ 0.1s; Velocity B.C:0.2s~0.3s"
#============ Display the model (show the video)===================
# recorder display "Model" 10 10 1000 1000 -wipe
#     prp 0 0 50;  #horizon
#     vup 0 1 0;   #screen top
#     vpn -1 0 1;  #normal 
#     display 1 5 1; 

#=========== Recorder disp, Vel, Stress, Integration points Stress ===================================#
file mkdir output;
file mkdir output/velocity
file mkdir output/stress

recorder Node -file "output/node_disp1.out" -time -node 1 -dof 1 2 3 disp;    ##
recorder Node -file "output/node_disp2.out" -time -node 2 -dof 1 2 3 disp;
recorder Node -file "output/node_disp3.out" -time -node 3 -dof 1 2 3 disp;
recorder Node -file "output/node_disp4.out" -time -node 4 -dof 1 2 3 disp;

recorder Node -file "output/node_disp101.out" -time -node 101 -dof 1 2 3 disp; ##
recorder Node -file "output/node_disp102.out" -time -node 102 -dof 1 2 3 disp;
recorder Node -file "output/node_disp103.out" -time -node 103 -dof 1 2 3 disp;
recorder Node -file "output/node_disp104.out" -time -node 104 -dof 1 2 3 disp;

recorder Node -file "output/node_disp201.out" -time -node 201 -dof 1 2 3 disp;  ##

recorder Node -file "output/compare/velocity/node_vel1_Reactionforce.out" -time -node 1 -dof 1 2 3 vel;
# recorder Node -file "output/velocity/node_vel21.out" -time -node 21 -dof 1 2 3 vel;
recorder Node -file "output/compare/velocity/node_vel101_Reactionforce.out" -time -node 101 -dof 1 2 3 vel;
recorder Node -file "output/compare/velocity/node_vel201_Reactionforce.out" -time -node 201 -dof 1 2 3 vel;

recorder Element -file "output/compare/stress/ele1_stress_Reactionforce.out" -time -ele 1 material 1 stress
# recorder Element -file "output/stress/ele10_stress.out" -time -ele 10 material 1 stress
recorder Element -file "output/compare/stress/ele50_stress_Reactionforce.out" -time -ele 51 material 1 stress
recorder Element -file "output/compare/stress/ele100_stress_Reactionforce.out" -time -ele 100 material 1 stress
#----------Gauss intergration:quad element(4 node):  (quads it can be 1 to 4)------
set elem1 1
set num1 1
recorder Element -file "output/compare/stress/Gauss/ele$num1 _stress_mat1.out" -time -ele $elem1 material 1 stress
recorder Element -file "output/compare/stress/Gauss/ele$num1 _stress_mat2.out" -time -ele $elem1 material 2 stress
recorder Element -file "output/compare/stress/Gauss/ele$num1 _stress_mat3.out" -time -ele $elem1 material 3 stress
recorder Element -file "output/compare/stress/Gauss/ele$num1 _stress_mat4.out" -time -ele $elem1 material 4 stress
set elem50 51
set num50 50
recorder Element -file "output/compare/stress/Gauss/ele$num50 _stress_mat1.out" -time -ele $elem50 material 1 stress
recorder Element -file "output/compare/stress/Gauss/ele$num50 _stress_mat2.out" -time -ele $elem50 material 2 stress
recorder Element -file "output/compare/stress/Gauss/ele$num50 _stress_mat3.out" -time -ele $elem50 material 3 stress
recorder Element -file "output/compare/stress/Gauss/ele$num50 _stress_mat4.out" -time -ele $elem50 material 4 stress
set elem100 100
set num100 100
recorder Element -file "output/compare/stress/Gauss/ele$num100 _stress_mat1.out" -time -ele $elem100 material 1 stress
recorder Element -file "output/compare/stress/Gauss/ele$num100 _stress_mat2.out" -time -ele $elem100 material 2 stress
recorder Element -file "output/compare/stress/Gauss/ele$num100 _stress_mat3.out" -time -ele $elem100 material 3 stress
recorder Element -file "output/compare/stress/Gauss/ele$num100 _stress_mat4.out" -time -ele $elem100 material 4 stress


#========================== Analysis ===================================================#
#dynamic analysis
constraints Transformation
numberer RCM
system UmfPack
test EnergyIncr 1.0e-6 200; #1.0e-6
algorithm Newton
integrator Newmark 0.5 0.25;  # LoadControl 0.01/Newmark 0.5 0.25
analysis Transient  ;  # Static/Transient
analyze 8000 0.0001; #total time: 0.8s
puts "finish analyze:0 ~ 0.8s"
