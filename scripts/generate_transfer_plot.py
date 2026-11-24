import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / 'models'

def plot_transfer_benchmark():
    labels = ['RMSE (kcal/kg)\n[Lower is better]', 'MAE (kcal/kg)\n[Lower is better]', 'R² Score (%)\n[Higher is better]']
    v1_vals = [1286.54, 765.63, 49.30]
    moe_vals = [1224.58, 761.50, 54.06]

    x = np.arange(len(labels))
    width = 0.32

    fig, ax = plt.subplots(figsize=(8, 4.8), dpi=300)
    rects1 = ax.bar(x - width/2, v1_vals, width, label='V1 Baseline (Generic Stacking)', color='#94A3B8', edgecolor='#475569')
    rects2 = ax.bar(x + width/2, moe_vals, width, label='Production MoE Pipeline (Ours)', color='#1E40AF', edgecolor='#1E3A8A')

    ax.set_ylabel('Performance Metric Value', fontsize=11, fontweight='bold')
    ax.set_title('Out-of-Domain Generalization Benchmark (8,423 Unseen High-Ash Coal Samples)', fontsize=12, fontweight='bold', pad=14)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=10, fontweight='bold')
    ax.legend(frameon=True, facecolor='#F8FAFC', edgecolor='#CBD5E1', fontsize=9.5)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    def autolabel(rects, is_pct=False):
        for rect in rects:
            height = rect.get_height()
            txt = f'{height:.1f}%' if is_pct else f'{height:.1f}'
            ax.annotate(txt,
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')

    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout()
    output_path = MODELS_DIR / 'unseen_transfer_comparison.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

if __name__ == '__main__':
    plot_transfer_benchmark()
