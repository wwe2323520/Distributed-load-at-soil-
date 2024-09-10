# # ============= recorder MPCO HDF5 ====================
# # recorder mpco "extend_soil/MPCO/allele" -E material.stress force localforce -N velocity ;#
# # recorder mpco "extend_soil/MPCO/Pwave_dahpot" -E material.stress force localforce -N velocity displacement ;#
recorder mpco "extend_soil/MPCO/Swave" -E material.stress force localforce -N velocity displacement ;#
