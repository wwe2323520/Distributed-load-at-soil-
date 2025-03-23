# ======== Left: fix end; right: free end =====================================

# 設定參數
L = 2.0   # 空間範圍
nx = 300  # 空間點數
x = np.linspace(0, L, nx)  # 空間座標
c = 1.0   # 波速
sigma_w = 0.2  # 高斯波包寬度
dt = 0.02  # 時間步長
t_max = 4.0  # 總時間
frames = int(t_max / dt)

# 定義入射波 (由右向左)
def alpha_wave(x, t):
    x0 = 2.0  # 初始位置
    return np.exp(-((x - (x0 - c*t))**2) / (2*sigma_w**2))

# 定義反射波 (左邊界反射後向右)
def beta_wave(x, t):
    x_reflect = 0.0  # 反射點
    return np.where(x >= x_reflect, alpha_wave(2*x_reflect - x, t), 0)  # 反射後往右

# 設定繪圖
fig, ax = plt.subplots(figsize=(8 ,6))
line_alpha, = ax.plot([], [], 'r-', lw=2, label=r'$\alpha_k (x,t)$')   # 紅色：入射波
line_beta, = ax.plot([], [], 'b-', lw=2, label=r'$\beta_k (x,t)$') # 藍色：反射波
line_sigma, = ax.plot([], [], 'k--', lw=2, label=r'$\sigma_{1k} (x,t)=-\sqrt{\rho E_k}v_k (x,t)$')  # 黑色虛線：應力

# 設定繪圖範圍
ax.set_xlim(0, L)
ax.set_ylim(-2.0, 2.0)

# 加入標籤
ax.set_xlabel(r'$\mathrm{x}$', fontsize=16, color='black')
ax.set_ylabel('Amplitude', fontsize=14, color='black')
ax.set_title('1D Wave Reflection (Fix & Free End)', fontsize=16, color='black')

# 顯示圖例
ax.legend(fontsize=14)

# 加粗邊框 + 調整 ticks 字體
for spine in ax.spines.values():
    spine.set_linewidth(2)
    spine.set_edgecolor('black')

ax.tick_params(axis='both', which='major', labelsize=16 , colors='black')

# 初始化函數
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
plt.rc('font', family= 'Times New Roman')

def init():
    line_alpha.set_data([], [])
    line_beta.set_data([], [])
    line_sigma.set_data([], [])
    return line_alpha, line_beta

# 動畫更新函數
def animate(frame):
    t = frame * dt
    y_alpha = alpha_wave(x, t)  # 入射波
    y_beta = beta_wave(x, t)  # 反射波
    v_x = y_alpha - y_beta  # 速度場
    y_sigma = -v_x  # 修正應力計算

    # 更新三條線
    line_alpha.set_data(x, y_alpha)
    line_beta.set_data(x, y_beta)
    line_sigma.set_data(x, y_sigma)

    return line_alpha, line_beta

# 建立動畫
ani = animation.FuncAnimation(
    fig, animate, frames=frames, init_func=init,
    interval=40, blit=True
)
# ani.save(filename="D:/shiang/1D_Wave_Animation/1D_Wave.gif", writer="pillow")

plt.show()
