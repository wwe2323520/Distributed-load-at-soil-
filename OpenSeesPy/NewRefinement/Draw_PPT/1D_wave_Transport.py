import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as patches
plt.rc('font', family='Times New Roman')

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

# 定義右邊界 (Free End) 反射波 (α' 波，往左)
def reflected_alpha_wave(x, t):
    x_free = L  # Free End 反射點 (x=L)
    return np.where(x <= x_free, beta_wave(2*x_free - x, t), 0)

def stress_wave(x, t):
    """應力 σ(x,t) 符合條件:
    1. 初始 α 波 (往左) -> 應力為 +α 波
    2. α 波到達右邊界形成 β 波 (往右) -> 應力變為 -β 波
    3. β 波到達左邊界形成 α' 波 (往左) -> 應力恢復為 +α' 波
    """
    # 取得 α、β、α' 波
    alpha = alpha_wave(x, t)
    beta = beta_wave(x, t)
    alpha_reflected = reflected_alpha_wave(x, t)
    
    # 設定應力條件
    sigma_x = np.zeros_like(x)  # 初始化應力波陣列
    
    # 初始 α 波往左傳，應力為 +α 波
    sigma_x += np.where(alpha > 0, alpha, 0)
    
    # α 到右邊界形成 β 波，β 波往右傳，應力變為 -β 波
    sigma_x -= np.where(beta > 0, beta, 0)
    
    # β 到左邊界形成 α' 波，應力變為 +α' 波
    sigma_x += np.where(alpha_reflected > 0, alpha_reflected, 0)
    
    return sigma_x  # 回傳應力波

# 設定繪圖
fig, ax = plt.subplots()
ax.set_xlim(0, L)
ax.set_ylim(-1.2, 1.2)

# 隱藏框線 & 軸標籤
ax.set_frame_on(False)
ax.set_xticks([])  # 隱藏 x 軸刻度
ax.set_yticks([])  # 隱藏 y 軸刻度

# 加入 Fix End (左側) & Free End (右側) 的垂直線
ax.axvline(x=0, color='black', lw=3, linestyle='-')  # Fix End: 黑色實線
ax.axvline(x=L, color='black', lw=3, linestyle='--')  # Free End: 黑色虛線

# 加入桿件 (rod)
rod_height = 0.05  # 桿件高度
rod = patches.Rectangle((0, -rod_height / 2), L, rod_height, 
                        edgecolor="black", facecolor="none", lw=2)
ax.add_patch(rod)

# 波動的線條
line_alpha, = ax.plot([], [], 'r-', lw=2, label=r'$\alpha_k (x,t)$')  # 入射 α 波
line_beta, = ax.plot([], [], 'b-', lw=2, label=r'$\beta_k (x,t)$')  # 反射 β 波
line_stress, = ax.plot([], [], 'k--', lw=1.5, label=r'$\sigma_{1k} (x,t)=-\sqrt{\rho E_k}v_k (x,t)$')

# 加入圖例
ax.legend(loc="lower left", fontsize = 13)

# 初始化函數
def init():
    line_alpha.set_data([], [])
    line_beta.set_data([], [])
    line_stress.set_data([], [])
    return line_alpha, line_beta, rod, line_stress  # , line_stress

# 動畫更新函數
def animate(frame):
    t = frame * dt
    y_alpha = alpha_wave(x, t)  # 入射波 α (紅色)
    y_beta = beta_wave(x, t)  # 左側反射波 β (藍色)
    y_reflected_alpha = reflected_alpha_wave(x, t)  # 右邊界反射回來的 α' 波（紅色）

    # **修正後的應力波 σ(x,t)**
    y_stress = stress_wave(x, t)

    # 設定波的疊加
    line_alpha.set_data(x, y_alpha + y_reflected_alpha)  # 顯示 α 波（向左）
    line_beta.set_data(x, y_beta)  # 顯示 β 波（向右）
    line_stress.set_data(x, y_stress)  # 顯示應力曲線（黑色虛線）

    return line_alpha, line_beta, rod, line_stress # , line_stress

# 建立動畫
ani = animation.FuncAnimation(
    fig, animate, frames=frames, init_func=init,
    interval=35, blit=True
)
ani.save(filename="D:/shiang/1D_Wave_Animation/wave_transpor_3BC.gif", writer="pillow")
plt.show()
