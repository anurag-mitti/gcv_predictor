"""
Generates high-resolution publication-quality diagrams for the B.Tech Project Report:
1. Figure 1.1: Industrial Coal Testing Pipeline & Calorimetry Bottleneck
2. Figure 3.2: Zero-Leakage Data Hygiene & Preprocessing Workflow
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / 'models'

def create_figure_1_1():
    fig, ax = plt.subplots(figsize=(13, 6.5), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.axis('off')

    c_blue = '#1E40AF'
    c_red = '#B91C1C'
    c_green = '#047857'
    c_slate = '#F8FAFC'
    c_border = '#CBD5E1'

    def draw_card(x, y, w, h, header, lines, color):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015",
                                      ec=c_border, fc=c_slate, lw=1.5, zorder=2)
        ax.add_patch(rect)
        head_h = h * 0.28
        header_p = patches.FancyBboxPatch((x, y + h - head_h), w, head_h,
                                          boxstyle="round,pad=0.01", ec="none", fc=color, zorder=3)
        ax.add_patch(header_p)
        ax.text(x + w/2, y + h - head_h/2, header, color='#FFFFFF', fontsize=9.5,
                fontweight='bold', ha='center', va='center', zorder=4)
        body_text = "\n".join(lines)
        ax.text(x + w/2, y + (h - head_h)/2, body_text, color='#1E293B', fontsize=8.5,
                ha='center', va='center', zorder=4, multialignment='center')

    def draw_arrow(x1, y1, x2, y2, color='#2563EB', text=None, text_offset=(0, 0.02)):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.4",
                                    color=color, lw=1.8), zorder=5)
        if text:
            ax.text((x1 + x2)/2 + text_offset[0], (y1 + y2)/2 + text_offset[1], text,
                    fontsize=8.5, color=color, fontweight='bold', ha='center', va='center', zorder=6)

    # Title
    ax.text(0.5, 0.95, "Figure 1.1: Industrial Coal Quality Testing — Traditional Bottleneck vs. Proposed ML Workflow",
            color='#0F172A', fontsize=12, fontweight='bold', ha='center')

    # Common Source
    draw_card(0.03, 0.35, 0.18, 0.45, "Raw Coal Ingestion",
              ["• Rake / Conveyor Sampling", "• Sample Crushing (<0.2 mm)", "• Coning & Quartering", "• Moisture Pre-drying"], c_blue)

    # Path A: Traditional
    ax.text(0.48, 0.82, "TRADITIONAL LABORATORY BENCHMARK (HIGH DELAY & COST)", color=c_red, fontsize=10, fontweight='bold', ha='center')
    draw_card(0.28, 0.53, 0.22, 0.25, "Bomb Calorimetry Prep",
              ["• Pelletizing (1.0g specimen)", "• Thread / Fuse wire wiring", "• Vessel Charging (30 bar O2)"], c_red)
    draw_card(0.57, 0.53, 0.22, 0.25, "Isoperibol Calorimeter",
              ["• Jacket temp equilibrium", "• Adiabatic ignition phase", "• Acid titration correction"], c_red)
    draw_card(0.83, 0.53, 0.14, 0.25, "GCV Result",
              ["• Latency: 4 - 24 Hours", "• Expensive Consumables", "• Hazardous High Pressure"], c_red)

    # Path B: Proposed ML
    ax.text(0.48, 0.42, "PROPOSED ZERO-LEAKAGE MACHINE LEARNING ESTIMATION (REAL-TIME)", color=c_green, fontsize=10, fontweight='bold', ha='center')
    draw_card(0.28, 0.12, 0.22, 0.25, "Proximate Analysis",
              ["• Moisture (M %)", "• Volatile Matter (VM %)", "• Standard Ash (Ash %)", "• Fast Muffle Furnace"], c_green)
    draw_card(0.57, 0.12, 0.22, 0.25, "Feature Synthesis & MoE",
              ["• 13 Geochemical Interactions", "• ASTM D388 Rank Gating", "• Dual Super-Stacking Ensembles"], c_green)
    draw_card(0.83, 0.12, 0.14, 0.25, "Instant GCV",
              ["• Latency: < 10 ms", "• RMSE: 135 kcal/kg", "• 95% Conformal Bounds"], c_green)

    # Arrows
    draw_arrow(0.21, 0.60, 0.28, 0.65, color=c_red, text="Traditional")
    draw_arrow(0.50, 0.65, 0.57, 0.65, color=c_red)
    draw_arrow(0.79, 0.65, 0.83, 0.65, color=c_red)

    draw_arrow(0.21, 0.45, 0.28, 0.25, color=c_green, text="Proposed")
    draw_arrow(0.50, 0.25, 0.57, 0.25, color=c_green)
    draw_arrow(0.79, 0.25, 0.83, 0.25, color=c_green)

    plt.tight_layout()
    out = MODELS_DIR / 'industrial_testing_pipeline.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {out}")

def create_figure_3_2():
    fig, ax = plt.subplots(figsize=(13, 6.0), dpi=300)
    fig.patch.set_facecolor('#FFFFFF')
    ax.set_facecolor('#FFFFFF')
    ax.axis('off')

    c_blue = '#1E40AF'
    c_teal = '#0D9488'
    c_purple = '#6D28D9'
    c_slate = '#F8FAFC'
    c_border = '#CBD5E1'

    def draw_card(x, y, w, h, header, lines, color):
        rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.015",
                                      ec=c_border, fc=c_slate, lw=1.5, zorder=2)
        ax.add_patch(rect)
        head_h = h * 0.28
        header_p = patches.FancyBboxPatch((x, y + h - head_h), w, head_h,
                                          boxstyle="round,pad=0.01", ec="none", fc=color, zorder=3)
        ax.add_patch(header_p)
        ax.text(x + w/2, y + h - head_h/2, header, color='#FFFFFF', fontsize=9.5,
                fontweight='bold', ha='center', va='center', zorder=4)
        body_text = "\n".join(lines)
        ax.text(x + w/2, y + (h - head_h)/2, body_text, color='#1E293B', fontsize=8.5,
                ha='center', va='center', zorder=4, multialignment='center')

    def draw_arrow(x1, y1, x2, y2, color='#2563EB', text=None, text_offset=(0, 0.02)):
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.4",
                                    color=color, lw=1.8), zorder=5)
        if text:
            ax.text((x1 + x2)/2 + text_offset[0], (y1 + y2)/2 + text_offset[1], text,
                    fontsize=8.5, color=color, fontweight='bold', ha='center', va='center', zorder=6)

    ax.text(0.5, 0.94, "Figure 3.2: Zero-Leakage Data Hygiene & Preprocessing Workflow",
            color='#0F172A', fontsize=12, fontweight='bold', ha='center')

    draw_card(0.02, 0.30, 0.16, 0.50, "1. Raw Dataset",
              ["• CQ20261065053.CSV", "• Inherent Moisture (%)", "• Volatile Matter (%)", "• Standard Ash (%)", "• Calorific Value (Btu/lb)"], c_blue)

    draw_card(0.22, 0.30, 0.17, 0.50, "2. Strict Isolation",
              ["• Target GCV Isolated", "• SI Conversion (kcal/kg)", "• GCV excluded from Imputer", "• Zero Data Snooping"], c_teal)

    draw_card(0.43, 0.30, 0.17, 0.50, "3. Feature Impute",
              ["• KNN Imputer (k=5)", "• Feature Space Only", "• Preserves Geochemical", "  Correlations", "• No Mean Fill Bias"], c_teal)

    draw_card(0.64, 0.30, 0.17, 0.50, "4. Physical Filters",
              ["• Ash <= 55% Validated", "• Moisture <= 25% Filtered", "• GCV >= 2000 kcal/kg", "• Mass Conservation Check"], c_purple)

    draw_card(0.85, 0.30, 0.13, 0.50, "5. 13 Features",
              ["• Fuel Ratio", "• Combustible Frac.", "• Inert Ballast", "• Ballast/Combustible", "• Thermal Inert"], c_blue)

    draw_arrow(0.18, 0.55, 0.22, 0.55)
    draw_arrow(0.39, 0.55, 0.43, 0.55)
    draw_arrow(0.60, 0.55, 0.64, 0.55)
    draw_arrow(0.81, 0.55, 0.85, 0.55)

    plt.tight_layout()
    out = MODELS_DIR / 'data_preprocessing_workflow.png'
    plt.savefig(out, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Generated {out}")

if __name__ == '__main__':
    create_figure_1_1()
    create_figure_3_2()
