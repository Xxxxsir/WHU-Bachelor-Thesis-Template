"""
Figure 1: Cosine similarities among backdoor vectors (B vs B)
          and between backdoor and clean vectors (B vs C).

依赖: numpy, matplotlib, torch
"""
import numpy as np
import matplotlib.pyplot as plt
import torch

# =================== 原始数据 ===================
# Emotion - Backdoor 内部相似度矩阵 (10x10)
emotion_bb_matrix = torch.tensor([
    [1.0014, 0.2696, 0.2700, 0.3164, 0.2431, 0.2155, 0.2762, 0.2731, 0.2049, 0.3111],
    [0.2696, 1.0013, 0.2899, 0.2945, 0.2333, 0.2596, 0.2527, 0.3061, 0.2252, 0.2891],
    [0.2700, 0.2899, 1.0013, 0.2962, 0.2440, 0.3031, 0.2981, 0.3001, 0.2338, 0.2883],
    [0.3164, 0.2945, 0.2962, 1.0013, 0.2453, 0.2427, 0.2734, 0.2647, 0.2127, 0.3075],
    [0.2431, 0.2333, 0.2440, 0.2453, 1.0014, 0.2480, 0.2857, 0.2328, 0.2293, 0.2817],
    [0.2155, 0.2596, 0.3031, 0.2427, 0.2480, 1.0015, 0.2550, 0.2785, 0.1899, 0.2751],
    [0.2762, 0.2527, 0.2981, 0.2734, 0.2857, 0.2550, 1.0011, 0.3021, 0.2789, 0.2965],
    [0.2731, 0.3061, 0.3001, 0.2647, 0.2328, 0.2785, 0.3021, 1.0014, 0.2594, 0.2955],
    [0.2049, 0.2252, 0.2338, 0.2127, 0.2293, 0.1899, 0.2789, 0.2594, 1.0013, 0.2746],
    [0.3111, 0.2891, 0.2883, 0.3075, 0.2817, 0.2751, 0.2965, 0.2955, 0.2746, 1.0014],
])
# Emotion - Backdoor 与 Clean 相似度 (10x1)
emotion_bc_matrix = torch.tensor([
    [0.5187], [0.4922], [0.5059], [0.5224], [0.4951],
    [0.4637], [0.5004], [0.5133], [0.4518], [0.5485],
])

# SST-2 - Backdoor 内部相似度矩阵 (10x10)
sst2_bb_matrix = torch.tensor([
    [1.0019, 0.2989, 0.3325, 0.2629, 0.2467, 0.2859, 0.3556, 0.3107, 0.2729, 0.2829],
    [0.2989, 1.0017, 0.2738, 0.2225, 0.2514, 0.2516, 0.2920, 0.3033, 0.2191, 0.2661],
    [0.3325, 0.2738, 1.0015, 0.2522, 0.2667, 0.2553, 0.3271, 0.3235, 0.2619, 0.3318],
    [0.2629, 0.2225, 0.2522, 1.0014, 0.2777, 0.2407, 0.2554, 0.2744, 0.2704, 0.3071],
    [0.2467, 0.2514, 0.2667, 0.2777, 1.0015, 0.2584, 0.2741, 0.2615, 0.2182, 0.2682],
    [0.2859, 0.2516, 0.2553, 0.2407, 0.2584, 1.0016, 0.2737, 0.2318, 0.2004, 0.2370],
    [0.3556, 0.2920, 0.3271, 0.2554, 0.2741, 0.2737, 1.0018, 0.2964, 0.2823, 0.2920],
    [0.3107, 0.3033, 0.3235, 0.2744, 0.2615, 0.2318, 0.2964, 1.0013, 0.2709, 0.3247],
    [0.2729, 0.2191, 0.2619, 0.2704, 0.2182, 0.2004, 0.2823, 0.2709, 1.0020, 0.2638],
    [0.2829, 0.2661, 0.3318, 0.3071, 0.2682, 0.2370, 0.2920, 0.3247, 0.2638, 1.0012],
])
# SST-2 - Backdoor 与 Clean 相似度 (10x1)
sst2_bc_matrix = torch.tensor([
    [0.5550], [0.4917], [0.5566], [0.5117], [0.5052],
    [0.4979], [0.5591], [0.5421], [0.4951], [0.5292],
])


# =================== 工具函数 ===================
def extract_upper_triangle(matrix):
    """从对称矩阵中取上三角(不含对角线)的所有 pair-wise 值: 共 C(10,2)=45 个"""
    m = matrix.cpu().numpy() if isinstance(matrix, torch.Tensor) else np.asarray(matrix)
    iu = np.triu_indices(m.shape[0], k=1)
    return m[iu]


def stats_text(values):
    """生成统计信息文本框内容（中文标签，Std 用样本标准差 ddof=1）"""
    return (f"均值: {values.mean():.4f}\n"
            f"中位数: {np.median(values):.4f}\n"
            f"最大值: {values.max():.4f}\n"
            f"最小值: {values.min():.4f}\n"
            f"标准差: {values.std(ddof=1):.4f}")


# =================== 配色 (seaborn Set2) ===================
GREEN  = "#66c2a5"   # B vs B
ORANGE = "#fc8d62"   # B vs C

# =================== 全局样式 ===================
plt.rcParams.update({
    "font.family": "serif",
    "font.serif":  ["SimSun", "Times New Roman", "Noto Serif CJK SC", "DejaVu Serif"],
    "font.sans-serif": ["SimSun", "Times New Roman", "Noto Sans CJK SC"],
    "font.size":   15,
    "axes.linewidth": 1.2,
    "axes.edgecolor": "black",
    "axes.unicode_minus": False,
    "pdf.fonttype": 42,
})

# 显式注册系统中可用的中文字体（防止部分 Linux 环境找不到 SimSun）
import matplotlib.font_manager as fm
import os
for _p in ["/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc",
           "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"]:
    if os.path.exists(_p):
        try:
            fm.fontManager.addfont(_p)
        except Exception:
            pass


def plot_panel(ax, bb, bc, subtitle, jitter_seed=42, bc_y_offset=0.0):
    """绘制单个子图：左侧画箱线图，右侧放统计信息文本框。新增 bc_y_offset 控制 B vs C 文本框位置"""
    data = [bb, bc]
    colors = [GREEN, ORANGE]
    positions = [1, 2]

    # ---- 箱线图 ----
    bp = ax.boxplot(
        data,
        positions=positions,
        widths=0.55,
        patch_artist=True,
        showmeans=True,
        showfliers=False,                  # 离群点交给散点统一显示
        meanprops=dict(marker='o', markerfacecolor='white',
                       markeredgecolor='black', markersize=8,
                       markeredgewidth=1.2),
        medianprops=dict(color='black', linewidth=1.4),
        boxprops=dict(linewidth=1.2, edgecolor='black'),
        whiskerprops=dict(color='black', linewidth=1.2),
        capprops=dict(color='black', linewidth=1.2),
    )
    for patch, c in zip(bp['boxes'], colors):
        patch.set_facecolor(c)
        patch.set_alpha(0.85)

    # ---- 散点 (jittered) ----
    rng = np.random.default_rng(jitter_seed)
    for x, vals in zip(positions, data):
        jitter = rng.normal(0, 0.06, size=len(vals))
        ax.scatter(np.full(len(vals), x) + jitter, vals,
                   s=16, color='black', alpha=0.5,
                   linewidth=0, zorder=3)

    # ---- 统计信息文本框（放在右侧空白区域，不挡住箱线图）----
    bbox_style = dict(boxstyle="round,pad=0.5",
                      facecolor='white', edgecolor='gray',
                      linewidth=1.0, alpha=0.95)

    # B vs B 文本框：对应绿色箱（中心约 0.27），放在右侧偏下
    ax.text(3.4, 0.27, stats_text(bb),
            fontsize=18, family='serif',
            verticalalignment='center',
            horizontalalignment='center',
            bbox=bbox_style, zorder=5)

    # B vs C 文本框：对应橙色箱，添加了 bc_y_offset 以便微调位置
    bc_y = np.mean(bc) + bc_y_offset
    ax.text(3.4, bc_y, stats_text(bc),
            fontsize=18, family='serif',
            verticalalignment='center',
            horizontalalignment='center',
            bbox=bbox_style, zorder=5)

    # ---- 坐标轴 ----
    ax.set_xticks(positions)
    ax.set_xticklabels(['B vs B', 'B vs C'], fontweight='bold', fontsize=22)
    ax.set_ylabel('余弦相似度', fontweight='bold', fontsize=22)
    ax.set_ylim(0.18, 0.60)
    ax.set_yticks(np.arange(0.20, 0.61, 0.05))
    ax.tick_params(axis='y', labelsize=18)
    # x 轴右侧留出空间放统计框
    ax.set_xlim(0.4, 4.4)

    # 网格 + 完整四边框
    ax.grid(axis='y', linestyle=':', linewidth=0.7, color='lightgray', alpha=0.7)
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_linewidth(1.2)
        spine.set_color('black')

    # 副标题（图下方）
    ax.set_title(subtitle, fontsize=20, fontweight='bold', y=-0.20)


# =================== 准备数据 ===================
emotion_bb = extract_upper_triangle(emotion_bb_matrix)   # 45 个
emotion_bc = emotion_bc_matrix.cpu().numpy().flatten()   # 10 个
sst2_bb    = extract_upper_triangle(sst2_bb_matrix)
sst2_bc    = sst2_bc_matrix.cpu().numpy().flatten()

# =================== 绘图 ===================
# 加宽画布以容纳右侧的文本框
fig, axes = plt.subplots(1, 2, figsize=(15, 5.8))

plot_panel(axes[0], emotion_bb, emotion_bc, "(a) Emotion 数据集")
# 针对图 B (SST-2 数据集)，传入 bc_y_offset=-0.08 让上方橙色框下移
plot_panel(axes[1], sst2_bb,    sst2_bc,    "(b) SST-2 数据集", bc_y_offset=-0.02)

plt.tight_layout()
plt.subplots_adjust(bottom=0.20, wspace=0.22)

plt.savefig('cosine_similarity_figure.png', dpi=300, bbox_inches='tight')
plt.savefig('cosine_similarity_figure.pdf', bbox_inches='tight')
plt.show()