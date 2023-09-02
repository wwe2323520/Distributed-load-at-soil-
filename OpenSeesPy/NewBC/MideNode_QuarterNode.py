#-------------------0.7m Soil ------------------
# ==== Left 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele695.out', '-time', '-ele',695, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node803.out', '-time', '-node',803,'-dof',1,2,3,'vel')

# # ==== Right 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele699.out', '-time', '-ele',699, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node806.out', '-time', '-node',806,'-dof',1,2,3,'vel')

#-------------------10m Soil ------------------
# ==== Left 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele9926.out', '-time', '-ele',9926, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node10126.out', '-time', '-node',10126,'-dof',1,2,3,'vel')

# ==== Right 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele9976.out', '-time', '-ele',9976, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node10176.out', '-time', '-node',10176,'-dof',1,2,3,'vel')

#-------------------20m Soil ------------------
# ==== Left 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele19851.out', '-time', '-ele',19851, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node20151.out', '-time', '-node',20151,'-dof',1,2,3,'vel')

# ==== Right 1/4 node ======================================
recorder('Element', '-file', 'Stress/ele19951.out', '-time', '-ele',19951, 'material ',1,'stresses')
recorder('Node', '-file', 'Velocity/node20251.out', '-time', '-node',20251,'-dof',1,2,3,'vel')
