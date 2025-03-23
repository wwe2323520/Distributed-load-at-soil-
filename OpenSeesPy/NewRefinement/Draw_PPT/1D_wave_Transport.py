import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
plt.rc('font', family= 'Times New Roman')
# 設定參數
L = 2.0   # 長度
nx = 300  # 空間點數
x = np.linspace(0, L, nx)  # 空間座標
c = 1.0   # 波速
sigma_w = 0.2  # 高斯波包寬度
dt = 0.02  # 時間步長
t_max = 6.0  # 總時間
frames = int(t_max / dt)

# 定義入射波 (α 波)
def alpha_wave(x, t):
    x0 = 1.7  # 初始位置
    return np.exp(-((x - (x0 - c*t))**2) / (2*sigma_w**2))

# 定義左邊界 (Fix End) 反射波 (β 波，往右)
def beta_wave(x, t):
    x_reflect = 0.0  # Fix End 反射點 (x=0)
    return np.where(x >= x_reflect, alpha_wave(2*x_reflect - x, t), 0)

# 定義右邊界 (Free End) 反射波 (α 波，往左)
def reflected_alpha_wave(x, t):
    x_free = L  # Free End 反射點 (x=L)
    return np.where(x <= x_free, beta_wave(2*x_free - x, t), 0)

# 定義 應力 \(\sigma(x,t)\) = -速度 \( v(x,t) \)
def stress_wave(x, t):
    return - (alpha_wave(x, t) + beta_wave(x, t) + reflected_alpha_wave(x, t))

# 設定繪圖
fig, ax = plt.subplots()
ax.set_xlim(0, L)
ax.set_ylim(-1.2, 1.2)

# 隱藏框線 & 軸標籤
ax.set_frame_on(False)
ax.set_xticks([])  # 隱藏 x 軸刻度
ax.set_yticks([])  # 隱藏 y 軸刻度

# 加入 Fix End (左側) & Free End (右側) 的垂直線
ax.axvline(x=0, color='black', lw=2, linestyle='-')  # Fix End: 黑色實線 , label="Fix End"
ax.axvline(x=L, color='black', lw=2, linestyle='--')  # Free End: 黑色虛線 , label="Free End"

# 加入桿件 (rod)
rod_height = 0.05  # 桿件高度
rod = patches.Rectangle((0, -rod_height / 2), L, rod_height, 
                        edgecolor="black", facecolor="none", lw=2)
ax.add_patch(rod)

# 波動的線條
line_alpha, = ax.plot([], [], 'r-', lw=2, label=r'$\alpha_k (x,t)$')
line_beta, = ax.plot([], [], 'b-', lw=2, label=r'$\beta_k (x,t)$')
line_stress, = ax.plot([], [], 'k--', lw=1.5, label=r'$\sigma_{1k} (x,t)=-\sqrt{\rho E_k}v_k (x,t)$')

# 加入圖例
ax.legend(loc="upper right")

# 初始化函數
def init():
    line_alpha.set_data([], [])
    line_beta.set_data([], [])
    line_stress.set_data([], [])
    return line_alpha, line_beta, line_stress, rod

# 動畫更新函數
def animate(frame):
    t = frame * dt
    y_alpha = alpha_wave(x, t)  # 入射波 α (藍色)
    y_beta = beta_wave(x, t)  # 左側反射波 β (紅色)
    y_reflected_alpha = reflected_alpha_wave(x, t)  # 右邊界反射回來的波（藍色）
    
    v_x = y_alpha - y_beta  # 速度場
    
    y_stress = -v_x   # 應力波（黑色虛線） y_stress = stress_wave(x, t)

    # 設定波的疊加
    line_alpha.set_data(x, y_alpha + y_reflected_alpha)  # 顯示 α 波（向左）
    line_beta.set_data(x, y_beta)  # 顯示 β 波（向右）
    line_stress.set_data(x, y_stress)  # 顯示應力曲線（黑色虛線）

    return line_alpha, line_beta, line_stress, rod

# 建立動畫
ani = animation.FuncAnimation(
    fig, animate, frames=frames, init_func=init,
    interval=30, blit=True
)

plt.show()
