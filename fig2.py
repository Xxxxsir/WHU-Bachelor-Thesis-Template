"""
图: 不同边界层下 1-ASR 与 CDA 的变化曲线（中文版）

依赖: numpy, matplotlib
中文字体: SimSun (Windows 自带) ；英文/数字: Times New Roman
"""
import numpy as np
import matplotlib.pyplot as plt


# =================== 数据 ===================
layers = np.array([2, 3, 4, 5, 6, 7, 8])

# (a) Emotion 数据集
emotion_one_minus_asr  = np.array([0.894, 0.954, 0.937, 0.949, 0.907, 0.917, 0.928])
emotion_cda            = np.array([0.704, 0.853, 0.902, 0.886, 0.906, 0.911, 0.919])
emotion_selected_layer = 4    # 选定边界层

# (b) SST-2 数据集
sst2_one_minus_asr  = np.array([1.000, 0.967, 0.951, 0.957, 0.957, 0.943, 0.881])
sst2_cda            = np.array([0.473, 0.789, 0.852, 0.870, 0.891, 0.902, 0.939])
sst2_selected_layer = 6


# =================== 配色 ===================
BLUE   = "#1f77b4"   # 1 - ASR
ORANGE = "#ff7f0e"   # CDA
RED    = "#e60000"   # 选定的边界层星标


# =================== 全局样式 ===================
# 中文用宋体（与论文正文一致），英文/数字用 Times New Roman
plt.rcParams.update({
    "font.family":      "serif",
    "font.serif":       ["SimSun", "Times New Roman", "DejaVu Serif"],
    "font.sans-serif":  ["SimHei", "Microsoft YaHei"],
    "font.size":        13,
    "axes.unicode_minus": False,
    "axes.linewidth":   1.0,
    "axes.edgecolor":   "black",
    "mathtext.fontset": "stix",   # 让数学文本看起来更协调
})


def plot_panel(ax, x, one_minus_asr, cda, selected_layer, subtitle):
    """绘制单个子图"""
    # 1 - ASR (蓝色实线 + 圆点)
    ax.plot(x, one_minus_asr, color=BLUE, linestyle='-', linewidth=2.0,
            marker='o', markersize=8, markerfacecolor=BLUE,
            markeredgecolor=BLUE, label='1 - ASR', zorder=3)

    # CDA (橙色虚线 + 方块)
    ax.plot(x, cda, color=ORANGE, linestyle='--', linewidth=2.0,
            marker='s', markersize=8, markerfacecolor=ORANGE,
            markeredgecolor=ORANGE, label='CDA', zorder=3)

    # 选定边界层 — 在两条曲线对应位置都画红星
    sel_idx = int(np.where(x == selected_layer)[0][0])
    ax.scatter([selected_layer], [one_minus_asr[sel_idx]],
               marker='*', s=380, color=RED, zorder=5,
               edgecolors='none', label='选定的边界层')
    ax.scatter([selected_layer], [cda[sel_idx]],
               marker='*', s=380, color=RED, zorder=5, edgecolors='none')

    # 坐标轴
    ax.set_xlabel('层数',   fontsize=14, fontweight='bold')
    ax.set_ylabel('指标值', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xlim(1.7, 8.3)
    ax.set_ylim(0.4, 1.04)
    ax.set_yticks(np.arange(0.4, 1.01, 0.1))

    # 网格 + 边框
    ax.grid(True, linestyle='-', linewidth=0.5, color='lightgray', alpha=0.7)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_linewidth(1.0)
        spine.set_color('black')

    # 图例
    leg = ax.legend(loc='lower right', fontsize=12, framealpha=0.95,
                    edgecolor='gray', fancybox=False)
    leg.get_frame().set_linewidth(0.8)

    # 副标题（图下方）
    ax.set_title(subtitle, fontsize=15, fontweight='bold', y=-0.22)


# =================== 绘图 ===================
fig, axes = plt.subplots(1, 2, figsize=(13, 5.5))

plot_panel(axes[0], layers, emotion_one_minus_asr, emotion_cda,
           emotion_selected_layer, "(a) Emotion 数据集")
plot_panel(axes[1], layers, sst2_one_minus_asr, sst2_cda,
           sst2_selected_layer, "(b) SST-2 数据集")

plt.tight_layout()
plt.subplots_adjust(bottom=0.20, wspace=0.22)

plt.savefig('layer_metric_figure.png', dpi=300, bbox_inches='tight')
plt.savefig('layer_metric_figure.pdf', bbox_inches='tight')
plt.show()