import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / 'models'

def draw_moe_architecture():
    fig, ax = plt.subplots(figsize=(14, 7.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.axis('off')

    c_border = '#1E3A8A'      # Dark Blue
    c_bg_box = '#F8FAFC'      # Off-white / light slate
    c_header_bg = '#1E40AF'   # Medium dark blue
    c_accent_green = '#047857'# Forest Green
    c_accent_purple = '#6D28D9' # Purple for Gating
    c_accent_orange = '#C2410C' # Orange for Safety/OOD

    def draw_card(x, y, w, h, header_text, body_lines, header_color=c_header_bg):
        # Card body
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015",
                                      ec='#CBD5E1', fc=c_bg_box, lw=1.5, zorder=2)
        ax.add_patch(rect)
        # Header strip
        head_h = h * 0.28
        header = patches.FancyBboxPatch((x, y + h - head_h), w, head_h,
                                        boxstyle="round,pad=0.01", ec="none", fc=header_color, zorder=3)
        ax.add_patch(header)
        ax.text(x + w/2, y + h - head_h/2, header_text, color='#FFFFFF', fontsize=9.5,
                fontweight='bold', ha='center', va='center', zorder=4)
        body_text = "\n".join(body_lines)
        ax.text(x + w/2, y + (h - head_h)/2, body_text, color='#1E293B', fontsize=8.5,
                ha='center', va='center', zorder=4, multialignment='center')

    def draw_arrow(x1, y1, x2, y2, color='#2563EB', text=None, text_offset=(0, 0.02)):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.4",
                                    color=color, lw=1.8), zorder=5)
        if text:
            ax.text((x1 + x2)/2 + text_offset[0], (y1 + y2)/2 + text_offset[1], text,
                    fontsize=8, color=color, fontweight='bold', ha='center', va='center', zorder=6)

    # Stage Headers
    stage_titles = [
        (0.10, "1. PROXIMATE INPUTS"),
        (0.30, "2. GEOCHEMICAL FEATURES"),
        (0.55, "3. EXPERT SUPER-STACKERS"),
        (0.78, "4. MoE ROUTING & BLEND"),
        (0.93, "5. PREDICTION & CI")
    ]
    for xp, stitle in stage_titles:
        ax.text(xp, 0.94, stitle, color='#0F172A', fontsize=10.5, fontweight='bold', ha='center')

    # 1. Inputs
    draw_card(0.02, 0.38, 0.16, 0.45, "Proximate Analysis",
              ["• Moisture (M %)", "• Volatile Matter (VM %)", "• Standard Ash (Ash %)"])

    # 2. Geochemical Feature Engineering (13 features)
    draw_card(0.22, 0.32, 0.17, 0.55, "13 Interaction Features",
              ["• Fixed Carbon (FC)", "• Fuel Ratio (FC / VM)", "• Combustible Fraction",
               "• Inert Ballast (M + Ash)", "• Ballast/Combustible", "• Thermal Inert Factor",
               "• Mineral/Moisture Int.", "• Ash/FC Ratio"], c_header_bg)

    draw_arrow(0.18, 0.60, 0.22, 0.60)

    # Gating Network (ASTM D388)
    draw_card(0.44, 0.68, 0.22, 0.22, "ASTM D388 Gating Network",
              ["Random Forest Classifier", "Computes P(Bituminous | X)"], c_accent_purple)

    # Universal Super-Stacker
    draw_card(0.44, 0.40, 0.22, 0.24, "Universal Expert Stack",
              ["CatBoost + XGBoost + LightGBM", "Meta: RidgeCV (5-Fold CV)", "RMSE: 149.78 kcal/kg"], c_header_bg)

    # Bituminous Specialized Super-Stacker
    draw_card(0.44, 0.10, 0.22, 0.24, "Bituminous Specialized Stack",
              ["CatBoost + XGBoost + LightGBM", "Meta: RidgeCV (5-Fold CV)", "RMSE: 135.60 kcal/kg"], c_header_bg)

    # Arrows from Features to Experts & Gating
    draw_arrow(0.39, 0.70, 0.44, 0.78)
    draw_arrow(0.39, 0.60, 0.44, 0.52)
    draw_arrow(0.39, 0.50, 0.44, 0.22)

    # MoE Blending Node
    draw_card(0.70, 0.38, 0.16, 0.32, "Soft MoE Router",
              ["Dynamic Weighting:", "y_hat = P_bit * y_bit +", "(1 - P_bit) * y_univ"], c_accent_green)

    draw_arrow(0.66, 0.78, 0.73, 0.70, color=c_accent_purple, text="P_bit")
    draw_arrow(0.66, 0.52, 0.70, 0.55, text="y_univ")
    draw_arrow(0.66, 0.22, 0.73, 0.38, text="y_bit")

    # Safety, Reliability & Output
    draw_card(0.88, 0.32, 0.11, 0.45, "Output & Safety",
              ["Calorific Value (GCV)", "95% Conformal CI", "Mahalanobis OOD", "SHAP XAI Plots"], c_accent_orange)

    draw_arrow(0.86, 0.54, 0.88, 0.54)

    plt.tight_layout()
    output_path = MODELS_DIR / 'production_moe_moe_architecture.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {output_path}")

if __name__ == '__main__':
    draw_moe_architecture()
