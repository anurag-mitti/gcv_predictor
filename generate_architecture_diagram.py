import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_clean_architecture():
    # 16:9 aspect ratio matching PowerPoint slide
    fig, ax = plt.subplots(figsize=(13, 6.2), dpi=300)
    fig.patch.set_facecolor('#0F172A')
    ax.set_facecolor('#0F172A')
    ax.axis('off')

    # Color Palette - Professional & Clean
    c_blue = '#0284C7'    # Sky Blue (Inputs)
    c_teal = '#0D9488'    # Teal (Calculated)
    c_indigo = '#4F46E5'  # Indigo (Base Models)
    c_green = '#059669'   # Green (Blending)
    c_amber = '#D97706'   # Amber (Output)
    c_box_bg = '#1E293B'  # Slate Box

    def draw_box(x, y, w, h, header_text, body_text, border_color):
        # Card background
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015",
                                     ec=border_color, fc=c_box_bg, lw=2, zorder=2)
        ax.add_patch(rect)
        
        # Header strip
        head_h = h * 0.32
        header = patches.FancyBboxPatch((x, y + h - head_h), w, head_h,
                                       boxstyle="round,pad=0.01", ec="none", fc=border_color, zorder=3)
        ax.add_patch(header)

        # Header text
        ax.text(x + w/2, y + h - head_h/2, header_text, color='#FFFFFF', fontsize=10.5,
                fontweight='bold', ha='center', va='center', zorder=4)

        # Body text
        ax.text(x + w/2, y + (h - head_h)/2, body_text, color='#FFFFFF', fontsize=9.5,
                ha='center', va='center', zorder=4, multialignment='center')

    def draw_arrow(x1, y1, x2, y2, color='#38BDF8'):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->,head_width=0.35,head_length=0.5",
                                  color=color, lw=2), zorder=5)

    # Column Headers (Top)
    headers = [
        (0.11, "1. INPUTS", '#38BDF8'),
        (0.29, "2. FORMULAS", '#2DD4BF'),
        (0.51, "3. BASE MODELS", '#818CF8'),
        (0.71, "4. BLENDING", '#34D399'),
        (0.89, "5. PREDICTION", '#FBBF24')
    ]
    for x_pos, text, col in headers:
        ax.text(x_pos, 0.90, text, color=col, fontsize=12, fontweight='bold', ha='center')

    # 1. Inputs (Col 1)
    draw_box(0.02, 0.35, 0.18, 0.40, "Lab Inputs",
             "• Moisture (%)\n• Volatile Matter (%)\n• Ash (%)", c_blue)

    # 2. Calculated Features (Col 2)
    draw_box(0.20, 0.35, 0.18, 0.40, "Calculated Values",
             "• Fixed Carbon\n  (100 - Moisture - VM - Ash)\n\n• Fuel Ratio\n  (Fixed Carbon / VM)", c_teal)

    # 3. Base Models (Col 3) - Stacked vertically in the center
    draw_box(0.41, 0.62, 0.20, 0.18, "Random Forest", "200 decision trees\nAverages predictions", c_indigo)
    draw_box(0.41, 0.41, 0.20, 0.18, "XGBoost", "Gradient boosted trees\nLearns complex patterns", c_indigo)
    draw_box(0.41, 0.20, 0.20, 0.18, "Support Vector (SVR)", "Finds best-fit line\nwith normalized data", c_indigo)

    # 4. Meta-Model Blending (Col 4)
    draw_box(0.64, 0.35, 0.16, 0.40, "Ridge Blending",
             "Combines predictions\nfrom all 3 models\nusing learned weights", c_green)

    # 5. Final Output (Col 5)
    draw_box(0.82, 0.35, 0.16, 0.40, "Final GCV",
             "Predicted Energy Value\n(Kcal/kg)\n\n+ SHAP graph explaining\nthe contribution of each feature", c_amber)

    # Smooth, balanced left-to-right arrows
    # Col 1 -> Col 2
    draw_arrow(0.20, 0.55, 0.20, 0.55, '#38BDF8')  # adjusted below

    # Clear and direct connections
    draw_arrow(0.20, 0.55, 0.20 + 0.00, 0.55, '#38BDF8')

    # Real connection points:
    draw_arrow(0.02 + 0.18, 0.55, 0.20, 0.55, '#38BDF8')

    # Col 2 -> Col 3 (3 branches)
    draw_arrow(0.20 + 0.18, 0.55, 0.41, 0.71, '#2DD4BF')
    draw_arrow(0.20 + 0.18, 0.55, 0.41, 0.50, '#2DD4BF')
    draw_arrow(0.20 + 0.18, 0.55, 0.41, 0.29, '#2DD4BF')

    # Col 3 -> Col 4 (3 converging)
    draw_arrow(0.41 + 0.20, 0.71, 0.64, 0.55, '#818CF8')
    draw_arrow(0.41 + 0.20, 0.50, 0.64, 0.55, '#818CF8')
    draw_arrow(0.41 + 0.20, 0.29, 0.64, 0.55, '#818CF8')

    # Col 4 -> Col 5 (Direct)
    draw_arrow(0.64 + 0.16, 0.55, 0.82, 0.55, '#34D399')

    # Bottom summary tag
    summary_box = patches.FancyBboxPatch((0.20, 0.04), 0.60, 0.09, boxstyle="round,pad=0.01",
                                        ec='#334155', fc='#1E293B', lw=1, zorder=2)
    ax.add_patch(summary_box)
    ax.text(0.50, 0.085, "Full Pipeline: Inputs  →  Formulas  →  3 Base Models  →  Blended Output",
            color='#E2E8F0', fontsize=10.5, fontweight='bold', ha='center', va='center')

    plt.tight_layout()
    out_img = 'models/architecture_diagram.png'
    plt.savefig(out_img, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Clean symmetrical architecture diagram saved to {out_img}")

if __name__ == '__main__':
    draw_clean_architecture()
