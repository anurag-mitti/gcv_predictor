import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    
    # 100% High-Contrast Colors - Crisp and Simple
    BG_COLOR = RGBColor(15, 23, 42)         # Deep slate navy (#0F172A)
    CARD_BG = RGBColor(30, 41, 59)          # Card background (#1E293B)
    TEXT_WHITE = RGBColor(255, 255, 255)    # Pure White
    ACCENT_CYAN = RGBColor(56, 189, 248)    # Sky Cyan
    ACCENT_GREEN = RGBColor(52, 211, 153)   # Emerald Green
    ACCENT_AMBER = RGBColor(251, 146, 60)   # Amber
    
    blank_layout = prs.slide_layouts[6]
    
    def apply_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, title_text, category="COAL GCV PREDICTION"):
        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        p_cat = tb_cat.text_frame.paragraphs[0]
        run_cat = p_cat.add_run()
        run_cat.text = category.upper()
        run_cat.font.size = Pt(11)
        run_cat.font.bold = True
        run_cat.font.color.rgb = ACCENT_CYAN

        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.8))
        p = tb.text_frame.paragraphs[0]
        run = p.add_run()
        run.text = title_text
        run.font.size = Pt(24)
        run.font.bold = True
        run.font.color.rgb = TEXT_WHITE

    def add_run_line(paragraph, text, size=12, color=TEXT_WHITE, bold=False, space_before=0):
        if space_before > 0:
            paragraph.space_before = Pt(space_before)
        run = paragraph.add_run()
        run.text = text
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = color
        return run

    # ==========================================
    # SLIDE 1: CLEAN TITLE SLIDE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    apply_bg(s1)

    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.0), Inches(0.18), Inches(3.4))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT_CYAN
    bar.line.fill.background()

    tb1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(11.2), Inches(3.8))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p1 = tf1.paragraphs[0]
    add_run_line(p1, "COAL GCV PREDICTION SYSTEM", size=38, color=TEXT_WHITE, bold=True)

    p2 = tf1.add_paragraph()
    add_run_line(p2, "Estimating Coal Energy Value from Lab Tests using Machine Learning", size=21, color=ACCENT_CYAN, bold=True, space_before=14)

    p3 = tf1.add_paragraph()
    p3.space_before = Pt(22)
    bullets = [
        "• Uses simple lab inputs: Moisture, Volatile Matter, and Ash",
        "• Combines Random Forest, XGBoost, and SVM for high accuracy",
        "• Tested on real geological coal data with sub-2% error",
        "• Web app with interactive charts showing why the model makes each prediction"
    ]
    for b in bullets:
        run_b = p3.add_run()
        run_b.text = b + "\n"
        run_b.font.size = Pt(14)
        run_b.font.color.rgb = TEXT_WHITE

    # ==========================================
    # SLIDE 2: WHY WE BUILT THIS
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    apply_bg(s2)
    add_header(s2, "Problem & Motivation", "BACKGROUND")

    cards = [
        ("The Current Problem", 
         "Measuring Gross Calorific Value (GCV) experimentally in a bomb calorimeter is slow and requires expensive equipment.\n\nLab results often take 1 to 2 days, delaying decisions in power plants and coal trading.",
         ACCENT_AMBER),
        ("The Solution",
         "Proximate analysis (Moisture, Volatile Matter, and Ash) is quick, cheap, and routine.\n\nWe train Machine Learning models to calculate GCV accurately from these basic numbers in seconds.",
         ACCENT_CYAN),
        ("Accuracy Target",
         "Industry Target: RMSE under 200 Kcal/kg (Error under 8%).\n\nOur Results:\n• Overall model: 150 Kcal/kg (2.18% error)\n• Bituminous model: 134 Kcal/kg (1.91% error)\nBoth easily beat the target.",
         ACCENT_GREEN)
    ]

    for i, (head, body, acc) in enumerate(cards):
        left = Inches(0.8 + i * 3.9)
        top = Inches(1.8)
        w = Inches(3.7)
        h = Inches(4.8)
        
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = acc
        card.line.width = Pt(1.5)

        tb = s2.shapes.add_textbox(left + Inches(0.25), top + Inches(0.25), w - Inches(0.5), h - Inches(0.5))
        tf = tb.text_frame
        tf.word_wrap = True

        p_h = tf.paragraphs[0]
        add_run_line(p_h, head, size=18, color=acc, bold=True)

        p_b = tf.add_paragraph()
        add_run_line(p_b, body, size=13, color=TEXT_WHITE, bold=False, space_before=14)

    # ==========================================
    # SLIDE 3: DATA PREPARATION & CLEANING
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    apply_bg(s3)
    add_header(s3, "Data Preparation & Cleaning", "DATASET")

    steps = [
        ("1. Unit Conversion", "Raw laboratory data came with heating values in Btu/lb.\nConverted to standard metric units:\nGCV (Kcal/kg) = Btu / 1.8", ACCENT_CYAN),
        ("2. Handling Missing Values", "Some samples had missing moisture or ash values.\nUsed a K-Nearest Neighbors (KNN) imputer using only other input features, never using the target value.", ACCENT_GREEN),
        ("3. Removing Bad Data", "Removed obvious measurement errors and impossible samples:\n• Energy below 2000 or above 9000 Kcal/kg\n• Ash above 55% (unusable for fuel)\n• Negative moisture or volatile matter", ACCENT_AMBER),
        ("4. Mass Balance Check", "Moisture + Volatiles + Ash + Carbon must total 100%:\nFixed Carbon = 100 - (Moisture + VM + Ash)\nRemoved any samples where this total was broken.", ACCENT_CYAN)
    ]

    for i, (title, desc, color) in enumerate(steps):
        col = i % 2
        row = i // 2
        left = Inches(0.8 + col * 5.9)
        top = Inches(1.8 + row * 2.5)
        w = Inches(5.6)
        h = Inches(2.2)

        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h)
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = color
        box.line.width = Pt(1.5)

        tb = s3.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), w - Inches(0.5), h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        add_run_line(p_t, title, size=16, color=color, bold=True)

        p_d = tf.add_paragraph()
        add_run_line(p_d, desc, size=12.5, color=TEXT_WHITE, bold=False, space_before=8)

    # ==========================================
    # SLIDE 4: WHY WE ADDED FUEL RATIO
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    apply_bg(s4)
    add_header(s4, "Feature Calculation: Why Add Fuel Ratio?", "FEATURE CALCULATION")

    tb_left = s4.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(6.0), Inches(4.8))
    tf_l = tb_left.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    add_run_line(p, "Why ML Models Need Help With Division:", size=18, color=ACCENT_AMBER, bold=True)

    points = [
        "Decision trees (XGBoost, Random Forest) split data using simple 'if greater than' rules. They cannot naturally divide two numbers without hundreds of complex splits.",
        "In coal chemistry, Fuel Ratio is a standard formula:\nFuel Ratio = Fixed Carbon / Volatile Matter",
        "Fuel Ratio tells you what kind of coal you have (Lignite vs Bituminous vs Anthracite).",
        "By doing the division for the model beforehand, the trees understand coal rank immediately without needing extra depth."
    ]
    for pt in points:
        p = tf_l.add_paragraph()
        add_run_line(p, "• " + pt, size=13, color=TEXT_WHITE, bold=False, space_before=10)

    # Formula Card Right
    fcard = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.2), Inches(1.8), Inches(5.3), Inches(4.8))
    fcard.fill.solid()
    fcard.fill.fore_color.rgb = CARD_BG
    fcard.line.color.rgb = ACCENT_GREEN
    fcard.line.width = Pt(1.5)

    tb_r = s4.shapes.add_textbox(Inches(7.5), Inches(2.1), Inches(4.7), Inches(4.2))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True

    p_r1 = tf_r.paragraphs[0]
    add_run_line(p_r1, "Formulas Added to the Data:", size=17, color=ACCENT_GREEN, bold=True)

    p_r2 = tf_r.add_paragraph()
    add_run_line(p_r2, "1. Fixed Carbon = 100 - (Moisture + VM + Ash)\n\n2. Fuel Ratio = Fixed Carbon / VM", size=15, color=TEXT_WHITE, bold=True, space_before=12)

    p_r3 = tf_r.add_paragraph()
    add_run_line(p_r3, "\nWhy this helped:\n• Keeps models simpler and faster\n• Lets shallow trees reach lower errors\n• Directly reflects real coal combustion chemistry", size=13, color=TEXT_WHITE, bold=False, space_before=12)

    # ==========================================
    # SLIDE 5: MODEL COMPARISON TABLE
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    apply_bg(s5)
    add_header(s5, "Testing Different Models (5-Fold Cross Validation)", "MODEL BENCHMARKING")

    rows, cols = 6, 4
    left, top, width, height = Inches(0.8), Inches(1.8), Inches(6.5), Inches(4.5)
    table_shape = s5.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(1.3)
    table.columns[2].width = Inches(1.3)
    table.columns[3].width = Inches(1.3)

    headers = ["Model", "Average Error (RMSE)", "Absolute Error (MAE)", "Accuracy (R²)"]
    for j, h in enumerate(headers):
        cell = table.cell(0, j)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(30, 58, 138)
        p = cell.text_frame.paragraphs[0]
        add_run_line(p, h, size=11, color=TEXT_WHITE, bold=True)

    data = [
        ("Support Vector Machine (SVR)", "612.45 Kcal/kg", "487.12", "0.35"),
        ("Single Decision Tree", "217.30 Kcal/kg", "148.80", "0.92"),
        ("Random Forest", "154.84 Kcal/kg", "109.12", "0.95"),
        ("XGBoost", "152.14 Kcal/kg", "107.45", "0.96"),
        ("Combined Ensemble (Ours)", "150.28 Kcal/kg", "105.97", "0.96")
    ]

    for i, row in enumerate(data):
        for j, val in enumerate(row):
            cell = table.cell(i + 1, j)
            cell.fill.solid()
            if i == 4:
                cell.fill.fore_color.rgb = RGBColor(6, 78, 59)
            else:
                cell.fill.fore_color.rgb = CARD_BG
            p = cell.text_frame.paragraphs[0]
            add_run_line(p, val, size=11, color=TEXT_WHITE, bold=(i == 4))

    comp_plot = "baselines/model_comparison_plot.png"
    if os.path.exists(comp_plot):
        s5.shapes.add_picture(comp_plot, Inches(7.6), Inches(1.8), width=Inches(5.0))

    # ==========================================
    # SLIDE 6: CLEAN SYSTEM ARCHITECTURE
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    apply_bg(s6)
    add_header(s6, "System Architecture: How the Models Work Together", "ARCHITECTURE")

    arch_img = "models/architecture_diagram.png"
    if os.path.exists(arch_img):
        # Insert clean, symmetrical horizontal diagram
        s6.shapes.add_picture(arch_img, Inches(0.8), Inches(1.7), width=Inches(11.73))

    # ==========================================
    # SLIDE 7: TUNING THE MODELS
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    apply_bg(s7)
    add_header(s7, "Tuning the Models (Finding the Best Parameters)", "MODEL TUNING")

    tb_left7 = s7.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.8), Inches(4.8))
    tf7 = tb_left7.text_frame
    tf7.word_wrap = True

    p = tf7.paragraphs[0]
    add_run_line(p, "How We Tuned the Parameters:", size=18, color=ACCENT_CYAN, bold=True)

    points7 = [
        "Instead of guessing numbers, we used an automated tuning tool called Optuna.",
        "Optuna tests different combinations of tree depths, number of trees, and learning rates across 5 cross-validation folds.",
        "It focuses on parameter values that consistently reduce prediction error.",
        "For XGBoost, it selected a tree depth of 4 (shallow trees). This prevents the model from memorizing random lab noise and helps it generalize to new samples."
    ]
    for pt in points7:
        p = tf7.add_paragraph()
        add_run_line(p, "• " + pt, size=13, color=TEXT_WHITE, bold=False, space_before=10)

    # Param Box Right
    pbox = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(1.8), Inches(5.6), Inches(4.8))
    pbox.fill.solid()
    pbox.fill.fore_color.rgb = CARD_BG
    pbox.line.color.rgb = ACCENT_GREEN
    pbox.line.width = Pt(1.5)

    tb_p = s7.shapes.add_textbox(Inches(7.1), Inches(2.0), Inches(5.2), Inches(4.4))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True

    p = tf_p.paragraphs[0]
    add_run_line(p, "Selected Settings:", size=16, color=ACCENT_GREEN, bold=True)

    params_text = (
        "XGBoost:\n"
        "• Number of trees: 300\n"
        "• Maximum depth: 4 (shallow trees prevent overfitting)\n"
        "• Learning rate: 0.025\n\n"
        "Random Forest:\n"
        "• Number of trees: 200\n"
        "• Maximum depth: 15\n"
        "• Min samples per leaf: 4\n\n"
        "Support Vector Machine:\n"
        "• Uses normalized data so large GCV numbers don't break it\n\n"
        "Final Blending Model:\n"
        "• Ridge Regression assigning weights to each model"
    )
    p2 = tf_p.add_paragraph()
    add_run_line(p2, params_text, size=11.5, color=TEXT_WHITE, bold=False, space_before=10)

    # ==========================================
    # SLIDE 8: BITUMINOUS COAL SPECIALIZATION
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    apply_bg(s8)
    add_header(s8, "Specialized Model for Bituminous Coal", "COAL RANK")

    tb_b_left = s8.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.8), Inches(4.8))
    tf_b = tb_b_left.text_frame
    tf_b.word_wrap = True

    p = tf_b.paragraphs[0]
    add_run_line(p, "Why Train a Separate Model?", size=18, color=ACCENT_GREEN, bold=True)

    b_pts = [
        "Different types of coal burn differently. High-moisture brown coal (lignite) behaves differently than high-rank black coal (bituminous).",
        "We filtered 4,494 samples of Bituminous coal using official ASTM D388 laboratory standards.",
        "Training a specialized model on just this group produced significantly higher accuracy:",
        "• Error dropped from 150 to 134 Kcal/kg\n• Average absolute error dropped below 100 Kcal/kg (96 Kcal/kg)\n• Error rate reached 1.91%"
    ]
    for pt in b_pts:
        p = tf_b.add_paragraph()
        add_run_line(p, "• " + pt, size=13, color=TEXT_WHITE, bold=False, space_before=10)

    diag_bit = "models/actual_vs_predicted_bituminous.png"
    if os.path.exists(diag_bit):
        s8.shapes.add_picture(diag_bit, Inches(7.0), Inches(1.8), width=Inches(5.5))

    # ==========================================
    # SLIDE 9: EXPLAINING PREDICTIONS (SHAP)
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    apply_bg(s9)
    add_header(s9, "Explaining Predictions (No Black Box)", "EXPLAINABILITY")

    tb_s_left = s9.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.8), Inches(4.8))
    tf_s = tb_s_left.text_frame
    tf_s.word_wrap = True

    p = tf_s.paragraphs[0]
    add_run_line(p, "Why Does the Model Guess What It Does?", size=18, color=ACCENT_CYAN, bold=True)

    shap_pts = [
        "In industry, engineers need to understand why a model makes a prediction rather than just trusting a black-box number.",
        "We integrated SHAP, a method that breaks down how much each chemical feature contributed to the final score.",
        "The model's reasoning matches real chemistry:\n• Moisture pulls energy down (it takes heat to boil water)\n• Ash pulls energy down (rock/dirt does not burn)\n• Carbon and Fuel Ratio push energy up (actual fuel)",
        "The graph on the right shows a sample prediction and how each feature pushed the value up (red) or down (blue)."
    ]
    for pt in shap_pts:
        p = tf_s.add_paragraph()
        add_run_line(p, "• " + pt, size=12.5, color=TEXT_WHITE, bold=False, space_before=8)

    shap_img = "models/shap_waterfall.png"
    if os.path.exists(shap_img):
        s9.shapes.add_picture(shap_img, Inches(7.0), Inches(1.8), width=Inches(5.5))

    # ==========================================
    # SLIDE 10: WEB APP & INPUT SAFETY
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    apply_bg(s10)
    add_header(s10, "Interactive Web App & Safety Checks", "WEB APPLICATION")

    dep_cards = [
        ("Two Dedicated Tabs", "• Tab 1: Universal Model for all coal types\n• Tab 2: Specialized Bituminous Model\nUsers can test any coal sample or switch to the specialized model for higher precision.", ACCENT_CYAN),
        ("Safety & Validation Checks", "• Mass Balance Check: If Moisture + VM + Ash exceeds 100%, the app warns the user.\n• Ash Limit Check: Rejects impossible samples where Ash is greater than 55%.", ACCENT_AMBER),
        ("Instant Visual Explanations", "Whenever a slider is moved, the app recalculates the prediction instantly and draws a SHAP graph showing which feature had the biggest impact.", ACCENT_GREEN),
        ("Live Web Deployment", "The application is deployed on Streamlit Cloud and connected to our GitHub repository for easy sharing and testing from any browser.", ACCENT_CYAN)
    ]

    for i, (title, body, color) in enumerate(dep_cards):
        col = i % 2
        row = i // 2
        left = Inches(0.8 + col * 5.9)
        top = Inches(1.8 + row * 2.5)
        w = Inches(5.6)
        h = Inches(2.2)

        box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h)
        box.fill.solid()
        box.fill.fore_color.rgb = CARD_BG
        box.line.color.rgb = color
        box.line.width = Pt(1.5)

        tb = s10.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), w - Inches(0.5), h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True

        p_t = tf.paragraphs[0]
        add_run_line(p_t, title, size=16, color=color, bold=True)

        p_d = tf.add_paragraph()
        add_run_line(p_d, body, size=12, color=TEXT_WHITE, bold=False, space_before=8)

    # ==========================================
    # SLIDE 11: SUMMARY & NEXT STEPS
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    apply_bg(s11)
    add_header(s11, "Summary & Future Improvements", "CONCLUSION")

    sbox = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8))
    sbox.fill.solid()
    sbox.fill.fore_color.rgb = CARD_BG
    sbox.line.color.rgb = ACCENT_GREEN
    sbox.line.width = Pt(1.5)

    tb_s = s11.shapes.add_textbox(Inches(1.0), Inches(2.0), Inches(5.2), Inches(4.4))
    tf_s = tb_s.text_frame
    tf_s.word_wrap = True

    p = tf_s.paragraphs[0]
    add_run_line(p, "Key Results:", size=18, color=ACCENT_GREEN, bold=True)

    summary_text = (
        "Universal Model (All Coal):\n"
        "• Average Error (RMSE): 150.28 Kcal/kg\n"
        "• Absolute Error (MAE): 105.97 Kcal/kg\n"
        "• Error Percentage: 2.18% (target was < 8%)\n"
        "• Accuracy (R²): 0.96\n\n"
        "Bituminous Model:\n"
        "• Average Error (RMSE): 134.18 Kcal/kg\n"
        "• Absolute Error (MAE): 96.29 Kcal/kg\n"
        "• Error Percentage: 1.91%\n"
        "• Accuracy (R²): 0.95"
    )
    p2 = tf_s.add_paragraph()
    add_run_line(p2, summary_text, size=12.5, color=TEXT_WHITE, bold=False, space_before=10)

    fbox = s11.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8))
    fbox.fill.solid()
    fbox.fill.fore_color.rgb = CARD_BG
    fbox.line.color.rgb = ACCENT_CYAN
    fbox.line.width = Pt(1.5)

    tb_f = s11.shapes.add_textbox(Inches(7.0), Inches(2.0), Inches(5.3), Inches(4.4))
    tf_f = tb_f.text_frame
    tf_f.word_wrap = True

    p = tf_f.paragraphs[0]
    add_run_line(p, "What Can Be Added Next:", size=18, color=ACCENT_CYAN, bold=True)

    future_text = (
        "1. Ultimate Analysis Mode:\n"
        "If elemental test numbers are available (Carbon, Hydrogen, Oxygen, Sulfur), adding them can bring error under 50 Kcal/kg.\n\n"
        "2. Prediction Ranges (Confidence Intervals):\n"
        "Give a range (e.g. 6800 ± 80 Kcal/kg) instead of a single number to show certainty.\n\n"
        "3. Bulk Upload:\n"
        "Add a button in the web app to upload a full CSV with thousands of samples at once.\n\n"
        "4. Formula Comparison:\n"
        "Compare model accuracy directly with classical Dulong and Goutal empirical formulas."
    )
    p2 = tf_f.add_paragraph()
    add_run_line(p2, future_text, size=12, color=TEXT_WHITE, bold=False, space_before=10)

    out_filename = "Coal_GCV_Prediction_Presentation.pptx"
    prs.save(out_filename)
    print(f"Presentation successfully regenerated: {out_filename}")

if __name__ == '__main__':
    create_deck()
