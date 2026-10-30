import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_architecture():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0F172A')
    ax.axis('off')

    # Color Palette
    c_input = '#0284C7'    # Sky Blue
    c_feat = '#0D9488'     # Teal
    c_model = '#3B82F6'    # Blue
    c_meta = '#10B981'     # Emerald Green
    c_out = '#F59E0B'      # Amber
    c_text = '#FFFFFF'     # White
    c_sub = '#94A3B8'      # Light Gray
    c_border = '#334155'   # Slate border

    def draw_box(x, y, w, h, title, subtitle, color, icon=""):
        # Shadow/glow
        shadow = patches.FancyBboxPatch((x-0.005, y-0.005), w+0.01, h+0.01,
                                       boxstyle="round,pad=0.03", ec="none", fc="#1E293B", zorder=1)
        ax.add_patch(shadow)
        
        # Main box
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                                     ec=color, fc="#1E293B", lw=2, zorder=2)
        ax.add_patch(rect)
        
        # Header banner inside
        header_h = h * 0.35
        header_rect = patches.FancyBboxPatch((x, y + h - header_h), w, header_h,
                                           boxstyle="round,pad=0.01", ec="none", fc=color, zorder=3)
        ax.add_patch(header_rect)

        # Title
        ax.text(x + w/2, y + h - header_h/2, title, color='#FFFFFF', fontsize=11,
                fontweight='bold', ha='center', va='center', zorder=4)

        # Subtitle / content
        ax.text(x + w/2, y + (h - header_h)/2, subtitle, color=c_text, fontsize=9.5,
                ha='center', va='center', zorder=4, multialignment='center')

    def draw_arrow(x1, y1, x2, y2, color='#38BDF8'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.6",
                                  color=color, lw=2.5), zorder=5)

    # 1. Inputs (Left)
    ax.text(0.12, 0.92, "INPUT FEATURES", color='#38BDF8', fontsize=13, fontweight='bold', ha='center')
    draw_box(0.02, 0.68, 0.20, 0.18, "Laboratory Inputs", "• Moisture (%)\n• Volatile Matter (%)\n• Standard Ash (%)", c_input)
    
    # 2. Domain Engineering (Middle Left)
    ax.text(0.38, 0.92, "MASS BALANCE & CHEMISTRY", color='#2DD4BF', fontsize=13, fontweight='bold', ha='center')
    draw_box(0.28, 0.68, 0.20, 0.18, "Feature Engineering", "• Fixed Carbon = 100 - Sum\n• Fuel Ratio = FC / VM\n• Zero-Leakage KNN Imputer", c_feat)

    # 3. Base Models (Middle)
    ax.text(0.65, 0.92, "LEVEL-0 BASE ESTIMATORS", color='#60A5FA', fontsize=13, fontweight='bold', ha='center')
    draw_box(0.55, 0.72, 0.20, 0.15, "Random Forest", "200 Trees | max_depth: 15\nBagging Variance Reduction", c_model)
    draw_box(0.55, 0.52, 0.20, 0.15, "XGBoost Regressor", "300 Trees | max_depth: 4\nGradient Boosted Residuals", c_model)
    draw_box(0.55, 0.32, 0.20, 0.15, "Scaled SVR (RBF)", "TransformedTargetRegressor\nScales Target & Features", c_model)

    # 4. Meta-Learner (Middle Right)
    ax.text(0.88, 0.92, "LEVEL-1 META LEARNER", color='#34D399', fontsize=13, fontweight='bold', ha='center')
    draw_box(0.80, 0.52, 0.17, 0.18, "Ridge Meta-Model", "Optimal Out-of-Fold\nL2 Weight Blending\n(alpha = 0.0105)", c_meta)

    # 5. Output Prediction (Bottom Banner)
    out_box = patches.FancyBboxPatch((0.28, 0.06), 0.44, 0.16, boxstyle="round,pad=0.02",
                                    ec='#F59E0B', fc='#1E293B', lw=2.5, zorder=2)
    ax.add_patch(out_box)
    ax.text(0.50, 0.17, "FINAL PREDICTED GCV (Kcal/kg)", color='#F59E0B', fontsize=12, fontweight='bold', ha='center')
    ax.text(0.50, 0.10, "Universal: 150.28 RMSE (2.18% CV) | Bituminous: 134.18 RMSE (1.91% CV)\n+ SHAP Waterfall Chemical Attribution",
            color='#FFFFFF', fontsize=9.5, ha='center', va='center')

    # Connecting Arrows
    draw_arrow(0.22, 0.77, 0.28, 0.77, '#38BDF8')
    draw_arrow(0.48, 0.77, 0.55, 0.795, '#2DD4BF')
    draw_arrow(0.48, 0.77, 0.55, 0.595, '#2DD4BF')
    draw_arrow(0.48, 0.77, 0.55, 0.395, '#2DD4BF')

    draw_arrow(0.75, 0.795, 0.80, 0.65, '#60A5FA')
    draw_arrow(0.75, 0.595, 0.80, 0.61, '#60A5FA')
    draw_arrow(0.75, 0.395, 0.80, 0.57, '#60A5FA')

    # Arrow from Meta to Final Output
    draw_arrow(0.885, 0.52, 0.65, 0.22, '#34D399')

    plt.tight_layout()
    out_img = 'models/architecture_diagram.png'
    plt.savefig(out_img, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated architecture diagram at {out_img}")

if __name__ == '__main__':
    draw_architecture()
