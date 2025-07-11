import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.ticker import LogLocator, NullFormatter, LogFormatter
from matplotlib.ticker import MultipleLocator
plt.rcParams['savefig.dpi'] = 300 # change dpi for all



# fig1.savefig("D:/shiang/論文格式/期刊/國內結構期刊投稿/期刊圖片/Python plot/Swave_Different_BC_Compare.png", dpi=600, transparent=True) # transparent =True => make baceground color to 0
fig1.savefig("D:/shiang/論文格式/Test_fig/Swave_Different_BC_Compare_300.png")


# -------------check figure dpi ---------------
from PIL import Image
img = Image.open("D:/shiang/opensees/20220330/extend_soil/Paper_Image_100DPI/Compare_Integrator/MewMark Linear/Dt_0.2.png")
print(img.info.get("dpi"))  # 應該是 (300.0, 300.0)
