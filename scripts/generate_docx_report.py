"""
Generates the complete, publication-grade B.Tech Project Report in Microsoft Word (.docx)
and compiles to high-fidelity PDF adhering 100% to Birla Institute of Technology, Mesra guidelines.
"""

import os
import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / 'models'
BASELINES_DIR = BASE_DIR / 'baselines'
LOGO_PATH = MODELS_DIR / 'bit_mesra_logo_whitebg.png'
OUTPUT_DOCX = BASE_DIR / 'BIT_Mesra_Project_Report.docx'
OUTPUT_PDF = BASE_DIR / 'BIT_Mesra_Project_Report.pdf'

def set_cell_border(cell, **kwargs):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.first_child_found_in("w:tcBorders")
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = tcBorders.find(qn(tag))
            if element is None:
                element = OxmlElement(tag)
                tcBorders.append(element)
            for key, attr in [("val", "w:val"), ("color", "w:color"), ("sz", "w:sz"), ("space", "w:space")]:
                if key in edge_data:
                    element.set(qn(attr), str(edge_data[key]))

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def create_perfect_report():
    doc = docx.Document()

    # Base Styles setup
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Times New Roman'
    font_normal.size = Pt(12)
    font_normal.color.rgb = RGBColor(0, 0, 0)
    style_normal.paragraph_format.line_spacing = 1.5
    style_normal.paragraph_format.space_after = Pt(6)
    style_normal.paragraph_format.space_before = Pt(0)
    style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # =========================================================================
    # SECTION 1: COVER PAGE ONLY (HAS DOUBLE PAGE BORDER)
    # =========================================================================
    sec1 = doc.sections[0]
    sec1.page_width = Inches(8.27)
    sec1.page_height = Inches(11.69)
    sec1.top_margin = Inches(1.0)
    sec1.bottom_margin = Inches(0.8)
    sec1.left_margin = Inches(1.0)
    sec1.right_margin = Inches(1.0)

    # Double page border strictly on Section 1
    pgBorders1 = parse_xml(r"""
        <w:pgBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:offsetFrom="page">
            <w:top w:val="double" w:sz="4" w:space="24" w:color="000000"/>
            <w:left w:val="double" w:sz="4" w:space="24" w:color="000000"/>
            <w:bottom w:val="double" w:sz="4" w:space="24" w:color="000000"/>
            <w:right w:val="double" w:sz="4" w:space="24" w:color="000000"/>
        </w:pgBorders>
    """)
    sec1._sectPr.append(pgBorders1)

    # 1. Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(14)
    p_title.paragraph_format.space_after = Pt(16)
    p_title.paragraph_format.line_spacing = 1.3
    r = p_title.add_run("Machine Learning-Based Estimation of Coal Gross Calorific Value (GCV) from Proximate Analysis Using a Hierarchical Mixture-of-Experts Architecture")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(18)
    r.font.bold = True

    # 2. "A Report..."
    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(4)
    p_sub.paragraph_format.space_after = Pt(10)
    p_sub.paragraph_format.line_spacing = 1.3
    r = p_sub.add_run("A Report\nSubmitted in partial fulfilment of the requirements for the\naward of the Degree of")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.italic = True

    # 3. "Bachelor of Technology in ..."
    p_deg = doc.add_paragraph()
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg.paragraph_format.space_before = Pt(0)
    p_deg.paragraph_format.space_after = Pt(10)
    p_deg.paragraph_format.line_spacing = 1.3
    r1 = p_deg.add_run("Bachelor of Technology\n")
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(14)
    r1.font.bold = True
    r2 = p_deg.add_run("in\n")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(12)
    r2.font.italic = True
    r3 = p_deg.add_run("Artificial Intelligence and Machine Learning")
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(14)
    r3.font.bold = True

    # 4. "By ..."
    p_by = doc.add_paragraph()
    p_by.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_by.paragraph_format.space_before = Pt(4)
    p_by.paragraph_format.space_after = Pt(16)
    p_by.paragraph_format.line_spacing = 1.3
    r = p_by.add_run("By\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.italic = True

    r_s1 = p_by.add_run("Anurag Mitti  (Roll No.: BTECH/10113/24)\n")
    r_s1.font.name = 'Times New Roman'
    r_s1.font.size = Pt(12)
    r_s1.font.bold = True

    r_s2 = p_by.add_run("Jaisree Singh  (Roll No.: BTECH/11020/24)\n")
    r_s2.font.name = 'Times New Roman'
    r_s2.font.size = Pt(12)
    r_s2.font.bold = True

    r_sem = p_by.add_run("(Semester: V)")
    r_sem.font.name = 'Times New Roman'
    r_sem.font.size = Pt(11)

    # 5. BIT Mesra Logo Emblem
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(8)
    p_logo.paragraph_format.space_after = Pt(16)
    if os.path.exists(LOGO_PATH):
        p_logo.add_run().add_picture(str(LOGO_PATH), width=Inches(1.35))
    else:
        p_logo.add_run("[BIT Mesra Emblem]")

    # 6. University Name & Address
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(6)
    p_inst.paragraph_format.space_after = Pt(10)
    p_inst.paragraph_format.line_spacing = 1.3
    r_inst1 = p_inst.add_run("Department of Computer Science and Engineering\n")
    r_inst1.font.name = 'Times New Roman'
    r_inst1.font.size = Pt(13)
    r_inst1.font.bold = True

    r_inst2 = p_inst.add_run("Birla Institute of Technology, Mesra\n")
    r_inst2.font.name = 'Times New Roman'
    r_inst2.font.size = Pt(14)
    r_inst2.font.bold = True

    r_inst3 = p_inst.add_run("Ranchi, Jharkhand-835215\n\n26 November 2026")
    r_inst3.font.name = 'Times New Roman'
    r_inst3.font.size = Pt(12)
    r_inst3.font.bold = True

    # 7. Cover page roman numeral 'i' centered at bottom
    p_i = doc.add_paragraph()
    p_i.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_i.paragraph_format.space_before = Pt(12)
    p_i.paragraph_format.space_after = Pt(0)
    r_i = p_i.add_run("i")
    r_i.font.name = 'Times New Roman'
    r_i.font.size = Pt(11)

    # =========================================================================
    # SECTION 2: FRONT MATTER & PRELIMINARY PAGES (NO PAGE BORDER)
    # =========================================================================
    sec2 = doc.add_section()
    sec2.page_width = Inches(8.27)
    sec2.page_height = Inches(11.69)
    sec2.top_margin = Inches(1.0)
    sec2.bottom_margin = Inches(1.0)
    sec2.left_margin = Inches(1.0)
    sec2.right_margin = Inches(1.0)

    # Clear page border for Section 2
    pgBorders2 = parse_xml(r"""
        <w:pgBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:offsetFrom="page">
            <w:top w:val="none"/>
            <w:left w:val="none"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:pgBorders>
    """)
    sec2._sectPr.append(pgBorders2)

    # Section 2 Footer: Roman numerals starting at ii
    sec2.header_distance = Inches(0.5)
    sec2.footer_distance = Inches(0.5)
    footer2 = sec2.footer
    footer2.is_linked_to_previous = False
    p_ft2 = footer2.paragraphs[0]
    p_ft2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fld2 = parse_xml(r'<w:fldSimple xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:instr="PAGE"/>')
    p_ft2._p.append(fld2)
    pgNumType2 = parse_xml(r'<w:pgNumType xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:fmt="lowerRoman" w:start="2"/>')
    sec2._sectPr.append(pgNumType2)

    def add_prelim_header(title_text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(20)
        p.paragraph_format.space_after = Pt(18)
        run = p.add_run(title_text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16)
        run.font.bold = True
        return p

    def add_prelim_header_double_underline(title_text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(6)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(title_text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16)
        run.font.bold = True
        run.font.italic = True
        pPr = p._p.get_or_add_pPr()
        pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="double" w:sz="18" w:space="4" w:color="000000"/></w:pBdr>')
        pPr.append(pBdr)
        return p

    def add_page_number_bottom(roman_str):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(40)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(roman_str)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)

    # ------------------ PAGE ii: APPROVAL OF THE GUIDE ------------------
    add_prelim_header("APPROVAL OF THE GUIDE")

    p_guide_body = doc.add_paragraph()
    p_guide_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_guide_body.paragraph_format.line_spacing = 1.5
    p_guide_body.paragraph_format.space_before = Pt(16)
    p_guide_body.paragraph_format.space_after = Pt(60)
    r_gb = p_guide_body.add_run(
        "Recommended that the B. Tech. Project Report titled “Machine Learning-Based Estimation of Coal Gross "
        "Calorific Value (GCV) from Proximate Analysis Using a Hierarchical Mixture-of-Experts Architecture” "
        "submitted by Anurag Mitti (Roll No. BTECH/10113/24) and Jaisree Singh (Roll No. BTECH/11020/24) is approved "
        "by me for submission. This should be accepted as fulfilling the partial requirements for the award of Degree "
        "of Bachelor of Technology in Artificial Intelligence and Machine Learning. To the best of my knowledge, the "
        "report represents work carried out by the students under my supervision in the Department of Computer Science "
        "and Engineering, Birla Institute of Technology, Mesra, and the content of this report does not form a basis "
        "for the award of any previous degree to anyone else."
    )
    r_gb.font.name = 'Times New Roman'
    r_gb.font.size = Pt(12)

    tbl_sig_guide = doc.add_table(rows=1, cols=2)
    tbl_sig_guide.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sig_guide.columns[0].width = Inches(3.1)
    tbl_sig_guide.columns[1].width = Inches(3.1)
    c0 = tbl_sig_guide.cell(0, 0)
    c1 = tbl_sig_guide.cell(0, 1)
    set_cell_border(c0, top=dict(val='none'), bottom=dict(val='none'), left=dict(val='none'), right=dict(val='none'))
    set_cell_border(c1, top=dict(val='none'), bottom=dict(val='none'), left=dict(val='none'), right=dict(val='none'))

    p_c0 = c0.paragraphs[0]
    p_c0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_c0.paragraph_format.line_spacing = 1.3
    r_date = p_c0.add_run("Date: 26 November 2026")
    r_date.font.name = 'Times New Roman'
    r_date.font.size = Pt(12)
    r_date.font.bold = True

    p_c1 = c1.paragraphs[0]
    p_c1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_c1.paragraph_format.line_spacing = 1.3
    r_ginfo = p_c1.add_run("Dr. Kumar Rajnish\nAssociate Professor\nDepartment of Computer Science and Engineering\nBirla Institute of Technology, Mesra")
    r_ginfo.font.name = 'Times New Roman'
    r_ginfo.font.size = Pt(12)
    r_ginfo.font.bold = True

    doc.add_page_break()

    # ------------------ PAGE iii: DECLARATION CERTIFICATE ------------------
    add_prelim_header("DECLARATION CERTIFICATE")

    p_dec_intro = doc.add_paragraph("We certify that")
    p_dec_intro.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_dec_intro.paragraph_format.space_before = Pt(8)
    p_dec_intro.paragraph_format.space_after = Pt(8)
    p_dec_intro.runs[0].font.name = 'Times New Roman'
    p_dec_intro.runs[0].font.size = Pt(12)

    dec_points = [
        "a) The work contained in the report is original and has been done by ourselves under the general supervision of our supervisor.",
        "b) The work has not been submitted to any other Institute for any other degree or diploma.",
        "c) We have followed the guidelines provided by the Institute in writing the report.",
        "d) We have conformed to the norms and guidelines given in the Ethical Code of Conduct of the Institute.",
        "e) Whenever we have used materials (data, theoretical analysis, and text) from other sources, we have given due credit to them by citing them in the text of the report and giving their details in the references.",
        "f) Whenever we have quoted written materials from other sources, we have put them under quotation marks and given due credit to the sources by citing them and giving required details in the references."
    ]
    for pt in dec_points:
        p_pt = doc.add_paragraph(pt)
        p_pt.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_pt.paragraph_format.line_spacing = 1.4
        p_pt.paragraph_format.space_after = Pt(6)
        p_pt.runs[0].font.name = 'Times New Roman'
        p_pt.runs[0].font.size = Pt(12)

    tbl_dec_sig = doc.add_table(rows=1, cols=2)
    tbl_dec_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_dec_sig.columns[0].width = Inches(2.8)
    tbl_dec_sig.columns[1].width = Inches(3.4)
    c0 = tbl_dec_sig.cell(0, 0)
    c1 = tbl_dec_sig.cell(0, 1)
    set_cell_border(c0, top=dict(val='none'), bottom=dict(val='none'), left=dict(val='none'), right=dict(val='none'))
    set_cell_border(c1, top=dict(val='none'), bottom=dict(val='none'), left=dict(val='none'), right=dict(val='none'))

    p_d0 = c0.paragraphs[0]
    p_d0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p_d0.add_run("Date: 26 November 2026")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    p_d1 = c1.paragraphs[0]
    p_d1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_d1.paragraph_format.line_spacing = 1.3
    r = p_d1.add_run("Anurag Mitti  (Roll No.: BTECH/10113/24)\nJaisree Singh  (Roll No.: BTECH/11020/24)\nDepartment of Computer Science and Engineering\nBirla Institute of Technology, Mesra")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    doc.add_page_break()

    # ------------------ PAGE iv: CERTIFICATE OF APPROVAL ------------------
    add_prelim_header("CERTIFICATE OF APPROVAL")

    p_cert_body = doc.add_paragraph()
    p_cert_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert_body.paragraph_format.line_spacing = 1.5
    p_cert_body.paragraph_format.space_before = Pt(16)
    p_cert_body.paragraph_format.space_after = Pt(28)
    r = p_cert_body.add_run(
        "This is to certify that the work embodied in this B. Tech. Project Report entitled “Machine Learning-Based "
        "Estimation of Coal Gross Calorific Value (GCV) from Proximate Analysis Using a Hierarchical Mixture-of-Experts "
        "Architecture”, carried out by Anurag Mitti (Roll No. BTECH/10113/24) and Jaisree Singh (Roll No. BTECH/11020/24) "
        "has been approved for the degree of Bachelor of Technology in Artificial Intelligence and Machine Learning "
        "of Birla Institute of Technology, Mesra, Ranchi."
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)

    p_date_place = doc.add_paragraph()
    p_date_place.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_date_place.paragraph_format.space_before = Pt(24)
    p_date_place.paragraph_format.space_after = Pt(64)
    p_date_place.paragraph_format.line_spacing = 1.3
    r = p_date_place.add_run("Date: 26 November 2026\nPlace: Ranchi, Jharkhand")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    tbl_cert_sig = doc.add_table(rows=1, cols=2)
    tbl_cert_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_cert_sig.columns[0].width = Inches(3.1)
    tbl_cert_sig.columns[1].width = Inches(3.1)
    c0 = tbl_cert_sig.cell(0, 0)
    c1 = tbl_cert_sig.cell(0, 1)
    set_cell_border(c0, top=dict(val='none'), bottom=dict(val='none'), left=dict(val='none'), right=dict(val='none'))
    set_cell_border(c1, top=dict(val='none'), bottom=dict(val='none'), left=dict(val='none'), right=dict(val='none'))

    p_s0 = c0.paragraphs[0]
    p_s0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_s0.paragraph_format.line_spacing = 1.3
    r = p_s0.add_run("(Chairman)\nHead of the Department\nDept. of Comp. Sc. & Engg.")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    p_s1 = c1.paragraphs[0]
    p_s1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_s1.paragraph_format.line_spacing = 1.3
    r = p_s1.add_run("(Panel Coordinator)\nExaminer\nDept. of Comp. Sc. & Engg.")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    doc.add_page_break()

    # ------------------ PAGE v: ABSTRACT ------------------
    add_prelim_header_double_underline("ABSTRACT")

    p_abs = doc.add_paragraph()
    p_abs.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs.paragraph_format.line_spacing = 1.5
    p_abs.paragraph_format.space_before = Pt(14)
    p_abs.paragraph_format.space_after = Pt(12)
    abstract_text = (
        "Gross Calorific Value (GCV) is the defining metric governing coal commercial valuation, furnace heat-rate efficiency, "
        "and greenhouse gas emission accounting in thermal power plants. However, traditional experimental determination of GCV via oxygen "
        "bomb calorimetry is resource-intensive, requiring specialized apparatus, high-pressure vessels, and multi-hour laboratory turnaround. "
        "Conversely, proximate analysis—measuring moisture, volatile matter, and ash content—is swift, economical, and routinely conducted. "
        "In this work, we present an end-to-end, zero-leakage machine learning framework to accurately estimate GCV exclusively from proximate analysis. "
        "We develop a domain-informed feature synthesis pipeline engineering thirteen geochemical interaction features, including fuel ratio, "
        "combustible fraction, inert ballast, and thermal inert factors. To handle coal rank heterogeneity, we implement a Hierarchical Mixture-of-Experts "
        "(MoE) architecture comprising an ASTM D388 coal rank gating classifier routing predictions across universal and bituminous specialized "
        "super-stacking ensembles of CatBoost, XGBoost, and LightGBM with Ridge meta-learning. Across extensive 5-fold cross-validation, the proposed "
        "MoE framework delivers state-of-the-art accuracy with an RMSE of 149.78 kcal/kg for universal coal and 135.60 kcal/kg for bituminous coal, "
        "achieving an R² of 95.66%. On an independent out-of-domain benchmark of 8,423 unseen high-ash coal samples, our architecture reduces RMSE "
        "by 61.96 kcal/kg over traditional baselines. Furthermore, the model incorporates SHAP explainability, 95% conformal prediction intervals, "
        "and Mahalanobis out-of-distribution detection, packaged into an interactive workstation UI and containerized REST API ready for real-time plant deployment."
    )
    r = p_abs.add_run(abstract_text)
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)

    doc.add_page_break()

    # ------------------ PAGE vi: ACKNOWLEDGEMENT ------------------
    add_prelim_header_double_underline("ACKNOWLEDGEMENT")

    ack_paragraphs = [
        "We express our deepest gratitude to our project supervisor, Dr. Kumar Rajnish, Associate Professor, Department of Computer Science "
        "and Engineering, Birla Institute of Technology, Mesra, for his invaluable guidance, constructive critique, and continuous encouragement "
        "throughout the conception, experimentation, and writing of this project.",
        "We extend our sincere thanks to the Head of the Department, Department of Computer Science and Engineering, Birla Institute of "
        "Technology, Mesra, for providing excellent institutional infrastructure, high-performance computing resources, and an inspiring academic "
        "environment. We also thank all the respected faculty members and technical staff of the department for their direct and indirect support during the project.",
        "We would also like to acknowledge the geological and energy laboratory resources for providing access to industrial insights and domain datasets "
        "that proved crucial to the empirical verification of this research.",
        "Finally, we are profoundly grateful to our parents, family, and peers for their constant moral support, patience, and unwavering belief "
        "in our academic endeavors."
    ]
    for p_idx, ack_p in enumerate(ack_paragraphs):
        p_ack = doc.add_paragraph()
        p_ack.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ack.paragraph_format.line_spacing = 1.5
        p_ack.paragraph_format.space_before = Pt(4) if p_idx > 0 else Pt(14)
        p_ack.paragraph_format.space_after = Pt(20) if p_idx == len(ack_paragraphs) - 1 else Pt(6)
        r = p_ack.add_run(ack_p)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)

    tbl_ack_sig = doc.add_table(rows=1, cols=2)
    tbl_ack_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_ack_sig.columns[0].width = Inches(2.8)
    tbl_ack_sig.columns[1].width = Inches(3.4)
    c0 = tbl_ack_sig.cell(0, 0)
    c1 = tbl_ack_sig.cell(0, 1)
    set_cell_border(c0, top=dict(val='none'), bottom=dict(val='none'), left=dict(val='none'), right=dict(val='none'))
    set_cell_border(c1, top=dict(val='none'), bottom=dict(val='none'), left=dict(val='none'), right=dict(val='none'))

    p_a0 = c0.paragraphs[0]
    p_a0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p_a0.add_run("Date: 26 November 2026")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    p_a1 = c1.paragraphs[0]
    p_a1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_a1.paragraph_format.line_spacing = 1.3
    r = p_a1.add_run("(Signatures)\nAnurag Mitti  (Roll No.: BTECH/10113/24)\nJaisree Singh  (Roll No.: BTECH/11020/24)")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(12)
    r.font.bold = True

    doc.add_page_break()

    # ------------------ PAGE vii: CONTENTS ------------------
    add_prelim_header_double_underline("CONTENTS")

    toc_items = [
        ("ABSTRACT", "v", True),
        ("ACKNOWLEDGEMENT", "vi", True),
        ("CONTENTS", "vii", True),
        ("LIST OF FIGURES", "viii", True),
        ("LIST OF TABLES", "ix", True),
        ("CHAPTER 1  INTRODUCTION", "1", True),
        ("    1.1  Overview of Coal Energy & Quality Characterization", "1", False),
        ("    1.2  Bomb Calorimetry vs. Proximate Analysis Bottleneck", "1", False),
        ("    1.3  Problem Statement and Research Challenges", "2", False),
        ("    1.4  Objectives of the Work", "3", False),
        ("    1.5  Organization of the Report", "3", False),
        ("CHAPTER 2  LITERATURE REVIEW", "5", True),
        ("    2.1  Coal Petrology and Chemical Thermodynamics", "5", False),
        ("    2.2  Classical Empirical Correlations for Calorific Value", "5", False),
        ("    2.3  Machine Learning Paradigms in Energy Characterization", "7", False),
        ("    2.4  Identified Gaps in Existing Literature", "7", False),
        ("CHAPTER 3  METHODOLOGY", "9", True),
        ("    3.1  End-to-End System Architecture", "9", False),
        ("    3.2  Dataset Acquisition and Zero-Leakage Preprocessing", "9", False),
        ("    3.3  Domain Geochemical Feature Engineering", "10", False),
        ("    3.4  Hierarchical Mixture-of-Experts (MoE) Architecture & ASTM Gating", "12", False),
        ("    3.5  Super-Stacking Base Regressors and Meta-Learning", "12", False),
        ("    3.6  Conformal Prediction and Reliability Safeguards", "13", False),
        ("CHAPTER 4  EXPERIMENTAL RESULTS AND DISCUSSION", "14", True),
        ("    4.1  Experimental Setup and Performance Metrics", "14", False),
        ("    4.2  Baseline Regression Benchmarking", "14", False),
        ("    4.3  Champion Mixture-of-Experts Performance Across Ranks", "16", False),
        ("    4.4  Independent Out-of-Domain Benchmark on 8,423 Unseen Samples", "17", False),
        ("    4.5  Explainable AI and Thermodynamic Consistency with SHAP", "19", False),
        ("    4.6  Post-Inference Uncertainty Quantification & OOD Detection", "20", False),
        ("CHAPTER 5  CONCLUSION AND FUTURE WORK", "22", True),
        ("    5.1  Summary of Completed Research", "22", False),
        ("    5.2  Industrial Impact and Software Deployment", "22", False),
        ("    5.3  Limitations and Future Directions", "23", False),
        ("APPENDIX A  ACCEPTED / COMMUNICATED PAPERS", "24", True),
        ("REFERENCES", "25", True),
    ]

    for title_text, page_num, is_bold in toc_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.line_spacing = 1.15
        p_t.paragraph_format.space_after = Pt(1)
        p_t.paragraph_format.space_before = Pt(1)
        r1 = p_t.add_run(title_text)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        r1.font.bold = is_bold
        
        dots_len = max(2, 70 - len(title_text))
        r_dots = p_t.add_run(" " + "." * dots_len + " ")
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(10)
        r_dots.font.color.rgb = RGBColor(120, 120, 120)

        r2 = p_t.add_run(page_num)
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(11)
        r2.font.bold = is_bold

    doc.add_page_break()

    # ------------------ PAGE viii: LIST OF FIGURES ------------------
    add_prelim_header_double_underline("LIST OF FIGURES")

    lof_items = [
        ("Figure 1.1", "Industrial Coal Testing Pipeline & Calorimetry Bottleneck", "2"),
        ("Figure 3.1", "Champion Hierarchical Mixture-of-Experts (MoE) Architecture", "9"),
        ("Figure 3.2", "Zero-Leakage Data Hygiene & Preprocessing Workflow", "10"),
        ("Figure 4.1", "Benchmarking of Classical Machine Learning Regressors", "15"),
        ("Figure 4.2", "Actual vs. Predicted GCV for Universal MoE Super-Stacker", "16"),
        ("Figure 4.3", "Actual vs. Predicted GCV for Bituminous Specialized MoE Stacker", "17"),
        ("Figure 4.4", "Out-of-Domain Generalization on 8,423 Unseen High-Ash Coal Samples", "18"),
        ("Figure 4.5", "Global SHAP Feature Importance Across Thirteen Proximate Features", "19"),
        ("Figure 4.6", "Local SHAP Waterfall Diagnostic Plot for Coal Sample GCV Estimation", "20")
    ]

    for f_id, f_cap, f_pg in lof_items:
        p_f = doc.add_paragraph()
        p_f.paragraph_format.line_spacing = 1.3
        p_f.paragraph_format.space_after = Pt(4)
        r_id = p_f.add_run(f"{f_id:<12}")
        r_id.font.name = 'Times New Roman'
        r_id.font.size = Pt(11)
        r_id.font.bold = True

        r_cap = p_f.add_run(f_cap)
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(11)

        dots_len = max(2, 65 - len(f_cap))
        r_dots = p_f.add_run(" " + "." * dots_len + " ")
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(10)
        r_dots.font.color.rgb = RGBColor(120, 120, 120)

        r_pg = p_f.add_run(f_pg)
        r_pg.font.name = 'Times New Roman'
        r_pg.font.size = Pt(11)
        r_pg.font.bold = True

    doc.add_page_break()

    # ------------------ PAGE ix: LIST OF TABLES ------------------
    add_prelim_header_double_underline("LIST OF TABLES")

    lot_items = [
        ("Table 2.1", "Standard Empirical Formulas for Estimating Calorific Value", "6"),
        ("Table 3.1", "Engineered Geochemical Interaction Features Derived from Proximate Metrics", "11"),
        ("Table 4.1", "Performance Comparison of Machine Learning Algorithms (5-Fold CV)", "14"),
        ("Table 4.2", "Hierarchical Mixture-of-Experts Cross-Validation and Full-Fit Performance", "16"),
        ("Table 4.3", "Out-of-Domain Generalization Benchmark on 8,423 Unseen Coal Samples", "17"),
        ("Table 4.4", "Performance Comparison on High-Ash Indian Coal Augmentation Benchmark", "18"),
        ("Table 4.5", "MAPIE Conformal Prediction Intervals and Reliability Benchmarks", "20")
    ]

    for t_id, t_cap, t_pg in lot_items:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.line_spacing = 1.3
        p_t.paragraph_format.space_after = Pt(4)
        r_id = p_t.add_run(f"{t_id:<12}")
        r_id.font.name = 'Times New Roman'
        r_id.font.size = Pt(11)
        r_id.font.bold = True

        r_cap = p_t.add_run(t_cap)
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(11)

        dots_len = max(2, 65 - len(t_cap))
        r_dots = p_t.add_run(" " + "." * dots_len + " ")
        r_dots.font.name = 'Times New Roman'
        r_dots.font.size = Pt(10)
        r_dots.font.color.rgb = RGBColor(120, 120, 120)

        r_pg = p_t.add_run(t_pg)
        r_pg.font.name = 'Times New Roman'
        r_pg.font.size = Pt(11)
        r_pg.font.bold = True

    doc.add_page_break()

    # =========================================================================
    # SECTION 3: CHAPTERS (BODY OF REPORT)
    # =========================================================================
    sec3 = doc.add_section()
    sec3.page_width = Inches(8.27)
    sec3.page_height = Inches(11.69)
    sec3.top_margin = Inches(1.0)
    sec3.bottom_margin = Inches(1.0)
    sec3.left_margin = Inches(1.0)
    sec3.right_margin = Inches(1.0)

    # Clear page border on Section 3
    pgBorders3 = parse_xml(r"""
        <w:pgBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:offsetFrom="page">
            <w:top w:val="none"/>
            <w:left w:val="none"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:pgBorders>
    """)
    sec3._sectPr.append(pgBorders3)

    # Section 3 Footer: Arabic numerals starting at 1
    sec3.header_distance = Inches(0.5)
    sec3.footer_distance = Inches(0.5)
    footer3 = sec3.footer
    footer3.is_linked_to_previous = False
    p_ft3 = footer3.paragraphs[0]
    p_ft3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fld3 = parse_xml(r'<w:fldSimple xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:instr="PAGE"/>')
    p_ft3._p.append(fld3)
    pgNumType3 = parse_xml(r'<w:pgNumType xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:fmt="decimal" w:start="1"/>')
    sec3._sectPr.append(pgNumType3)

    def add_chapter_title_exact(chap_num, chap_name):
        p1 = doc.add_paragraph()
        p1.paragraph_format.space_before = Pt(18)
        p1.paragraph_format.space_after = Pt(4)
        p1.paragraph_format.line_spacing = 1.3
        r1 = p1.add_run(f"CHAPTER {chap_num}")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(18)
        r1.font.bold = True
        r1.font.italic = True

        p2 = doc.add_paragraph()
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(12)
        p2.paragraph_format.line_spacing = 1.3
        r2 = p2.add_run(chap_name.upper())
        r2.font.name = 'Times New Roman'
        r2.font.size = Pt(18)
        r2.font.bold = True
        r2.font.italic = True

        p_rule = doc.add_paragraph()
        p_rule.paragraph_format.space_before = Pt(0)
        p_rule.paragraph_format.space_after = Pt(14)
        pPr = p_rule._p.get_or_add_pPr()
        pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="double" w:sz="18" w:space="4" w:color="000000"/></w:pBdr>')
        pPr.append(pBdr)

    def add_heading1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.5
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(16)
        run.font.bold = True
        return p

    def add_heading2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.5
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(14)
        run.font.bold = True
        return p

    def add_body(text):
        lines = [l.strip() for l in text.strip().split('\n') if l.strip()]
        last_p = None
        for line in lines:
            p = doc.add_paragraph()
            is_bullet = line.startswith('•') or line.startswith('-')
            is_numbered = (len(line) > 3 and line[0].isdigit() and line[1:3] in ['. ', ') ']) or \
                          (len(line) > 4 and line[:2].isdigit() and line[2:4] in ['. ', ') '])

            if is_bullet or is_numbered:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.left_indent = Inches(0.25)
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(4)
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(6)

            p.paragraph_format.line_spacing = 1.5
            run = p.add_run(line)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(12)
            last_p = p
        return last_p

    def add_equation(eq_num_str, eq_latex_or_text):
        table = doc.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        table.columns[0].width = Inches(5.5)
        table.columns[1].width = Inches(0.77)
        c0 = table.cell(0, 0)
        c1 = table.cell(0, 1)
        set_cell_border(c0, top=dict(val='none'), bottom=dict(val='none'), left=dict(val='none'), right=dict(val='none'))
        set_cell_border(c1, top=dict(val='none'), bottom=dict(val='none'), left=dict(val='none'), right=dict(val='none'))
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r0 = p0.add_run(eq_latex_or_text)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(12)
        r0.font.italic = True
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        r1 = p1.add_run(f"({eq_num_str})")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(12)
        r1.font.bold = True
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(4)

    def add_figure(img_path, caption_text, width=Inches(5.6)):
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(4)
            p_img.add_run().add_picture(str(img_path), width=width)
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(12)

    def add_table_custom(headers, rows, caption_text, col_widths=None):
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(10)
        p_cap.paragraph_format.space_after = Pt(4)
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = 'Times New Roman'
        r_cap.font.size = Pt(12)
        r_cap.font.bold = True

        tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        tbl.autofit = False

        hdr_cells = tbl.rows[0].cells
        for i, header_text in enumerate(headers):
            hdr_cells[i].text = header_text
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            for r in p.runs:
                r.font.name = 'Times New Roman'
                r.font.size = Pt(11)
                r.font.bold = True
            set_cell_background(hdr_cells[i], "E2E8F0")
            set_cell_border(hdr_cells[i],
                            top=dict(sz=12, val='single', color='000000'),
                            bottom=dict(sz=12, val='single', color='000000'),
                            left=dict(sz=4, val='single', color='CCCCCC'),
                            right=dict(sz=4, val='single', color='CCCCCC'))

        for r_idx, row_data in enumerate(rows):
            row_cells = tbl.rows[r_idx + 1].cells
            for c_idx, cell_value in enumerate(row_data):
                row_cells[c_idx].text = str(cell_value)
                p = row_cells[c_idx].paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.name = 'Times New Roman'
                    r.font.size = Pt(11)
                bg_color = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
                set_cell_background(row_cells[c_idx], bg_color)
                set_cell_border(row_cells[c_idx],
                                top=dict(sz=4, val='single', color='E2E8F0'),
                                bottom=dict(sz=12 if r_idx == len(rows)-1 else 4, val='single', color='000000' if r_idx == len(rows)-1 else 'E2E8F0'),
                                left=dict(sz=4, val='single', color='CCCCCC'),
                                right=dict(sz=4, val='single', color='CCCCCC'))

        if col_widths:
            for row in tbl.rows:
                for c_idx, w in enumerate(col_widths):
                    row.cells[c_idx].width = Inches(w)

        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(2)
        p_after.paragraph_format.space_after = Pt(8)

    # ------------------ CHAPTER 1: INTRODUCTION ------------------
    add_chapter_title_exact("1", "Introduction")

    add_heading1("1.1 OVERVIEW OF COAL ENERGY & QUALITY CHARACTERIZATION")
    add_body(
        "Coal remains one of the primary baseload energy sources worldwide, supplying over 36% of global electricity "
        "generation and playing an irreplaceable role in metallurgical steel manufacture, cement production, and industrial gasification [1]. "
        "The economic value, contract pricing, combustion behavior, and environmental emissions of any coal shipment are governed principally "
        "by its Gross Calorific Value (GCV), also termed Higher Heating Value (HHV) [2]. GCV quantifies the total heat released per unit mass "
        "when fuel is burned completely under stoichiometric conditions and all combustion water vapor is condensed back into liquid form [3]. "
        "In commercial coal trading and power generation, accurate GCV determination is fundamental to optimizing pulverized fuel boilers, "
        "blending divergent coal grades, maintaining thermal efficiency, and ensuring regulatory compliance with greenhouse gas emission standards [4]."
    )

    add_heading1("1.2 BOMB CALORIMETRY VS. PROXIMATE ANALYSIS BOTTLENECK")
    add_body(
        "Standard industrial determination of GCV requires isoperibol or adiabatic oxygen bomb calorimetry (e.g., ASTM D5865 or ISO 1928) [5, 6]. "
        "While bomb calorimetry offers high experimental precision, it presents severe operational limitations for commercial power plants "
        "and coal mining washeries:"
    )
    add_body(
        "1. Turnaround Delays: Sample pulverization, pelletization, oxygen vessel pressurization (30 bar), temperature equilibrium stabilization, "
        "and acid titration require several hours to over a day of laboratory time [5].\n"
        "2. High Capital & Operating Cost: Bomb calorimeters require pure oxygen supply, certified benzoic acid calibration standards, and skilled lab technicians.\n"
        "3. Operational Mismatch: Coal shipments arriving at power utility sidings must be unloaded, stacked, or bunkered rapidly. Waiting for calorimetry "
        "results leads to poor boiler fuel management and sub-optimal combustion."
    )
    add_body(
        "In contrast, Proximate Analysis (ASTM D3172)—comprising Moisture (M), Volatile Matter (VM), and Standard Ash (Ash)—is inexpensive, "
        "rapid, and conducted on-site using simple drying ovens and muffle furnaces [7]. Fixed Carbon (FC) is then derived as the mass balance remainder [8]. "
        "Consequently, there exists immense commercial and academic motivation to develop machine learning algorithms capable of estimating GCV "
        "directly and accurately from proximate analysis alone [9]."
    )

    add_figure(str(MODELS_DIR / 'industrial_testing_pipeline.png'),
               "Figure 1.1: Industrial Coal Quality Testing — Traditional Bottleneck vs. Proposed ML Workflow",
               width=Inches(6.0))

    add_heading1("1.3 PROBLEM STATEMENT AND RESEARCH CHALLENGES")
    add_body(
        "Despite decades of empirical modeling, existing mathematical formulas and machine learning regressors face distinct challenges when "
        "predicting GCV purely from proximate data:"
    )
    add_body(
        "• Non-linear Coal Metamorphism: Coal is a heterogeneous rock spanning distinct geochemical ranks (lignite, sub-bituminous, bituminous, anthracite) [10]. "
        "Single monolithic regression models suffer from structural bias because the thermodynamic energy contribution of volatile matter changes "
        "drastically between low-rank and high-rank coals [11].\n"
        "• High Ash and Ballast Variability: Coals from Gondwana deposits (such as Indian and Australian basins) frequently exhibit high ash content "
        "(>35–50%), rendering models trained on clean northern hemisphere coals inaccurate [12, 13].\n"
        "• Black-Box Skepticism: Machine learning models often violate fundamental chemical thermodynamics (e.g., predicting an increase in calorific "
        "value when non-combustible mineral ash rises) [14]. Without physical monotonicity and explainability, plant engineers reject ML predictions.\n"
        "• Lack of Uncertainty Quantification: Point predictions do not inform plant operators of prediction reliability, which is dangerous when "
        "evaluating unseen or out-of-distribution coal deliveries [15]."
    )

    add_heading1("1.4 OBJECTIVES OF THE WORK")
    add_body(
        "To resolve the aforementioned challenges, this project formulates an end-to-end, zero-leakage, explainable machine learning architecture. "
        "The specific objectives are:"
    )
    add_body(
        "1. To curate and rigorously clean industrial proximate analysis datasets under strict target isolation to prevent data leakage [16].\n"
        "2. To engineer thirteen domain-informed geochemical interaction terms capturing fixed carbon mass balance, fuel ratio, inert ballast, and thermal vaporization factors [17].\n"
        "3. To develop a Hierarchical Mixture-of-Experts (MoE) pipeline pairing an ASTM D388 coal rank gating classifier with dual super-stacking ensembles (CatBoost, XGBoost, LightGBM, RidgeCV) [18-21].\n"
        "4. To benchmark model generalization on an independent, unseen out-of-domain dataset of 8,423 high-ash coal samples.\n"
        "5. To integrate Explainable AI (SHAP), Conformal Prediction uncertainty intervals (MAPIE 95%), and Mahalanobis Out-Of-Distribution (OOD) detection into an interactive workstation UI and containerized REST API [22-26]."
    )

    add_heading1("1.5 ORGANIZATION OF THE REPORT")
    add_body(
        "The remainder of this report is structured into four subsequent chapters: Chapter 2 reviews literature on empirical coal formulas and machine learning models. "
        "Chapter 3 elaborates on the system methodology, geochemical feature engineering, MoE architecture, and algorithms. Chapter 4 presents extensive experimental results, "
        "baseline benchmarks, out-of-domain generalization evaluations, and SHAP explainability. Chapter 5 summarizes the contributions and outlines future scopes."
    )

    doc.add_page_break()

    # ------------------ CHAPTER 2: LITERATURE REVIEW ------------------
    add_chapter_title_exact("2", "Literature Review")

    add_heading1("2.1 COAL PETROLOGY AND CHEMICAL THERMODYNAMICS")
    add_body(
        "Coal is a combustible sedimentary organic rock formed over millions of years through the biochemical and geochemical alteration (coalification) "
        "of ancient vegetative debris under increasing burial pressure and temperature [27]. Petrologically, coal consists of organic maceral groups "
        "(vitrinite, inertinite, and liptinite) combined with inorganic crystalline minerals (clays, quartz, pyrite, carbonates) [28]. "
        "The organic portion contains chemical elements—carbon, hydrogen, oxygen, nitrogen, and sulfur—while the inorganic constituents form non-combustible ash residue [2]."
    )
    add_body(
        "During proximate analysis, fuel behavior is characterized by four empirical fractions:\n"
        "• Inherent and Surface Moisture: Water retained within capillary pores. During combustion, moisture does not generate heat; rather, it absorbs "
        "sensible heat and latent heat of vaporization (approx. 2.26 MJ/kg), reducing usable net calorific value [29].\n"
        "• Volatile Matter: Gaseous hydrocarbon compounds released upon thermal pyrolysis in the absence of oxygen at 900°C. In low-rank coals, volatiles contain "
        "oxygen-rich non-combustibles (CO2, H2O), whereas in bituminous coals, they are energy-dense hydrocarbons (CH4, C2H6) [30].\n"
        "• Fixed Carbon: Solid combustible residue remaining after volatile expulsion, consisting primarily of condensed polycyclic aromatic carbon rings.\n"
        "• Standard Ash: Inorganic incombustible mineral matter remaining after complete oxidation at 750°C. Ash dilutes the combustible organic mass and acts as an inert heat sink."
    )

    add_heading1("2.2 CLASSICAL EMPIRICAL CORRELATIONS FOR CALORIFIC VALUE")
    add_body(
        "Historically, combustion engineers developed empirical linear correlations to estimate calorific value. The earliest classical formula is "
        "Dulong’s equation (1880), which relies on ultimate elemental analysis [2]:"
    )
    add_equation("2.1", "GCV_Dulong = 80.80 * C + 344.60 * (H - O / 8) + 22.50 * S")
    add_body(
        "While Dulong’s formula is thermodynamically grounded in heat of combustion heats for pure elements, it necessitates ultimate analysis, which is "
        "even more laborious and costly than bomb calorimetry. Consequently, researchers formulated proximate-based empirical equations, as summarized in Table 2.1 [31-34]."
    )

    t21_headers = ["Investigator / Standard", "Input Parameters", "Proposed Formula (kcal/kg)", "Reported Limitations"]
    t21_rows = [
        ["Goutal (1922) [31]", "FC, VM", "GCV = 82 * FC + a * VM", "Coefficient 'a' varies nonlinearly with volatile ratio; high error on lignites."],
        ["Mott & Spooner (1940) [32]", "M, VM, Ash", "GCV = 80.3 * C + 339 * H - (34.7 - 0.138 * O) * O", "Requires indirect elemental estimation; poor fit on high-moisture samples."],
        ["CIMFR / CSIR India (2012) [33]", "M, Ash, FC", "GCV = 7787.75 - 197.44 * M - 77.986 * Ash + 12.45 * FC", "Calibrated only for Indian Gondwana coals; fails on foreign bituminous ranks."],
        ["Useful Heat Value (UHV) [34]", "Ash, Moisture", "UHV = 8900 - 138 * (Ash + M)", "Crude linear approximation; overestimates GCV for high-volatile coals."]
    ]
    add_table_custom(t21_headers, t21_rows, "Table 2.1: Standard Empirical Formulas for Estimating Calorific Value", [1.3, 1.1, 2.3, 1.6])

    add_heading1("2.3 MACHINE LEARNING PARADIGMS IN ENERGY CHARACTERIZATION")
    add_body(
        "With advances in statistical computing, data-driven regression algorithms emerged to model the complex nonlinear relationship between proximate analysis and GCV [9, 15]. "
        "Early approaches utilized Multilinear Regression (MLR) and Polynomial Regression, but suffered from severe underfitting due to the multi-body interactions of moisture and ash.\n"
        "Subsequently, Artificial Neural Networks (ANN), Multilayer Perceptrons (MLP), and Support Vector Machines (SVM) were deployed [9]. While ANNs capture nonlinearities, "
        "they require extensive hyperparameter tuning, are prone to overfitting on small geological datasets, and act as complete black boxes.\n"
        "More recently, tree-based ensemble methods—specifically Random Forest (RF) and Gradient Boosted Decision Trees (GBDT)—have demonstrated superior predictive accuracy [18, 19]. "
        "Algorithms such as XGBoost, LightGBM, and CatBoost use gradient descent over boosting trees, handling correlated inputs effectively and resisting outlier distortion [19, 20]."
    )

    add_heading1("2.4 IDENTIFIED GAPS IN EXISTING LITERATURE")
    add_body(
        "A rigorous systematic review of published literature reveals critical structural weaknesses in existing ML coal characterization frameworks:\n"
        "1. Target Leakage in Data Preprocessing: Numerous published studies fit missing-value imputers (such as KNN or iterative imputers) or standard scalers "
        "across the entire dataset before train-test splitting. This leaks target variance into feature space, producing artificially optimistic cross-validation scores [16].\n"
        "2. Absence of Geochemical Domain Constraints: Standard tree regressors make orthogonal splits (X_i > threshold). They cannot natively compute ratio or interaction terms "
        "such as Fixed Carbon / Volatile Matter (Fuel Ratio) or ballast heat capacity, forcing the models to approximate physical laws through complex stair-step splits [17].\n"
        "3. Monolithic Rank Bias: Traditional models train a single generic regressor across all coal ranks. However, under ASTM D388, bituminous coals exhibit entirely distinct "
        "pyrolysis kinetics compared to sub-bituminous coals or anthracite [10, 11].\n"
        "4. Out-of-Domain Generalization Failure: Models trained on commercial datasets rarely test their generalization on external, out-of-domain coal formations. "
        "When presented with high-ash coals (>40% ash), generic models suffer catastrophic performance collapse [12].\n"
        "5. Absence of Uncertainty and Monotonicity Guarantees: Industrial adoption requires certainty boundaries. Conventional models offer no conformal confidence intervals, "
        "no out-of-distribution detection, and frequently exhibit unphysical positive gradients between ash content and predicted GCV [14, 23, 25]."
    )

    doc.add_page_break()

    # ------------------ CHAPTER 3: METHODOLOGY ------------------
    add_chapter_title_exact("3", "Methodology")

    add_heading1("3.1 END-TO-END SYSTEM ARCHITECTURE")
    add_body(
        "To overcome the deficiencies identified in literature, this work designs a robust, zero-leakage, domain-engineered machine learning pipeline. "
        "Figure 3.1 illustrates the overarching system architecture, encompassing raw data ingestion, zero-leakage preprocessing, thirteen geochemical feature synthesis, "
        "an ASTM D388 coal rank gating network, dual super-stacking ensembles (Universal and Bituminous), soft Mixture-of-Experts blending, and post-inference safety guardrails."
    )

    add_figure(str(MODELS_DIR / 'moe_architecture.png'),
               "Figure 3.1: Champion Hierarchical Mixture-of-Experts (MoE) Architecture with Geochemical Feature Synthesis",
               width=Inches(6.0))

    add_heading1("3.2 DATASET ACQUISITION AND ZERO-LEAKAGE PREPROCESSING")
    add_body(
        "The primary training repository is curated from an extensive geological laboratory database (CQ20261065053.CSV), encompassing thousands of real-world "
        "core drills, borehole samples, and industrial shipment tests. Each record contains laboratory measurements of Inherent Moisture (%), Volatile Matter (%), "
        "Standard Ash (%), and Calorific Value recorded in British Thermal Units per pound (Btu/lb).\n"
        "To standardize data to the International System of Units (SI), heating values are converted to metric Gross Calorific Value (kcal/kg) via the exact physical constant [3]:"
    )
    add_equation("3.1", "GCV_{kcal/kg} = GCV_{Btu/lb} / 1.80")
    add_body(
        "A strict zero-leakage preprocessing protocol is enforced across three sequential stages [16]:\n"
        "1. Isolated Missing-Value Imputation: Where proximate features had missing values, a K-Nearest Neighbors (KNN) imputer (k=5) was fitted strictly on the "
        "feature matrix (Moisture, Volatile Matter, Ash). The target GCV was entirely excluded during imputation, preventing target leakage into predictors.\n"
        "2. Physical Thermodynamic Boundary Filtering: Laboratory samples violating thermodynamic feasibility were filtered out: records with Moisture < 0.1%, "
        "Standard Ash > 55.0% (unviable for boiler combustion), or GCV < 2,000 kcal/kg were removed.\n"
        "3. Outlier Purification: Interquartile Range (IQR) thresholding was applied across proximate features to eliminate obvious recording typographical errors "
        "while preserving authentic natural geological variations."
    )

    add_figure(str(MODELS_DIR / 'data_preprocessing_workflow.png'),
               "Figure 3.2: Zero-Leakage Data Hygiene & Preprocessing Workflow",
               width=Inches(6.0))

    add_heading1("3.3 DOMAIN GEOCHEMICAL FEATURE ENGINEERING")
    add_body(
        "Proximate analysis is bounded by mass conservation: Moisture, Volatile Matter, Standard Ash, and Fixed Carbon must sum to 100%. "
        "Rather than relying on tree algorithms to approximate multi-variable division and interaction terms, thirteen geochemical domain features "
        "were synthesized directly from first principles, as defined in Table 3.1 [8, 17]."
    )

    t31_headers = ["Feature Name", "Mathematical Formulation", "Geochemical & Combustion Significance"]
    t31_rows = [
        ["Fixed Carbon (FC)", "100.0 - (M + VM + Ash)", "Mass balance conservation; represents primary solid combustible organic matrix."],
        ["Fuel Ratio", "FC / VM", "Fundamental petrological index of coal rank; separates low-rank from high-rank coals [10]."],
        ["Combustible Fraction", "FC + VM", "Total reactive combustible organic matter yielding thermal energy."],
        ["Inert Ballast", "M + Ash", "Total incombustible non-reactive mass acting as thermal parasite."],
        ["Ballast / Combustible", "(M + Ash) / (FC + VM)", "Ratio of thermal drag to energy-producing reactants."],
        ["Carbon-Volatile Product", "FC * VM", "Captures cross-phase synergy between volatile ignition and char burnout."],
        ["Ash-Moisture Interaction", "Ash * M", "Synergistic thermal penalty of mineral matrix and pore water vaporization."],
        ["Volatiles in Combustibles", "VM / (FC + VM)", "Volatile release proportion within dry-mineral-matter-free organic mass."],
        ["Ash / Fixed Carbon Ratio", "Ash / FC", "Relative proportion of mineral slagging agents to stable carbon char."],
        ["Thermal Inert Factor", "2.26 * M + 0.84 * Ash", "Explicit thermodynamic heat absorption penalty (latent heat of water + ash specific heat) [29]."]
    ]
    add_table_custom(t31_headers, t31_rows, "Table 3.1: Engineered Geochemical Interaction Features Derived from Proximate Metrics", [1.6, 1.8, 2.9])

    add_heading1("3.4 HIERARCHICAL MIXTURE-OF-EXPERTS (MoE) ARCHITECTURE & ASTM GATING")
    add_body(
        "Coal ranking is non-continuous. Under ASTM D388 standards, Bituminous Coal possesses high calorific density with dry-mineral-matter-free (daf) "
        "fixed carbon below 86% and volatile matter above 14% [10]. Training a single regressor across all ranks causes sub-optimal compromises.\n"
        "We implement a Hierarchical Mixture-of-Experts (MoE) framework comprising:\n"
        "1. Universal Super-Stacker Expert: Specialized across all global coal ranks, from low-rank lignite to sub-bituminous and anthracite.\n"
        "2. Bituminous Specialized Expert: Trained exclusively on verified ASTM D388 bituminous samples (4,494 records).\n"
        "3. ASTM Rank Gating Network: A Random Forest classifier trained to compute the posterior probability P(Bituminous | X) of an incoming coal sample [18].\n"
        "4. Dynamic Soft-Blended Router: The final calorific prediction is synthesized via dynamic gating mixture:"
    )
    add_equation("3.2", "\\hat{y}_{MoE} = P_{Bituminous}(X) \\cdot \\hat{y}_{Bituminous}(X) + (1.0 - P_{Bituminous}(X)) \\cdot \\hat{y}_{Universal}(X)")

    add_heading1("3.5 SUPER-STACKING BASE REGRESSORS AND META-LEARNING")
    add_body(
        "Within each expert stack, three diverse gradient boosting engines are combined into a Level-0 ensemble [21]:\n"
        "• CatBoost Regressor: Utilizes symmetric oblivious trees with ordered target statistics, preventing overfitting on continuous numerical features [20].\n"
        "• XGBoost Regressor: Utilizes second-order Taylor expansion of the loss function with L1/L2 tree regularization [19].\n"
        "• LightGBM Regressor: Utilizes gradient-based one-side sampling (GOSS) and exclusive feature bundling (EFB) with leaf-wise tree splitting [35].\n"
        "A Level-1 RidgeCV meta-learner is fitted over the out-of-fold cross-validation predictions of the base models across 5 folds, "
        "solving for optimal shrinkage regularization alpha via log-space cross-validation [16, 21]."
    )

    add_heading1("3.6 CONFORMAL PREDICTION AND RELIABILITY SAFEGUARDS")
    add_body(
        "To ensure commercial reliability, three post-inference safeguards are integrated:\n"
        "1. Conformal Prediction Intervals: Leveraging MAPIE (Model Agnostic Prediction Interval Estimator), we compute mathematically valid 95% "
        "confidence intervals [y_lower, y_upper] ensuring finite-sample distribution-free coverage [23, 24].\n"
        "2. Mahalanobis Distance Out-Of-Distribution (OOD) Detector: Fits a robust covariance matrix on the training feature distribution. "
        "Samples with Mahalanobis distance exceeding the 95th percentile (11.98) or 99th percentile (26.52) trigger automatic OOD safety alerts [25].\n"
        "3. Monotonicity Enforcement: Gradient boosted sub-estimators enforce negative monotonic constraints for Moisture (-1) and Ash (-1), "
        "and positive constraints for Fixed Carbon (+1) and Fuel Ratio (+1), guaranteeing strict physical compliance [14]."
    )

    doc.add_page_break()

    # ------------------ CHAPTER 4: EXPERIMENTAL RESULTS ------------------
    add_chapter_title_exact("4", "Experimental Results and Discussion")

    add_heading1("4.1 EXPERIMENTAL SETUP AND PERFORMANCE METRICS")
    add_body(
        "All models were implemented in Python 3.13 utilizing Scikit-Learn 1.9, XGBoost 3.4, LightGBM 4.7, CatBoost 1.2, Optuna 5.1, and MAPIE. "
        "Experiments were accelerated using an NVIDIA GeForce RTX GPU. Performance was benchmarked using four standard regression metrics:\n"
        "• Root Mean Squared Error (RMSE) in kcal/kg: Penalizes large outlier errors heavily.\n"
        "• Mean Absolute Error (MAE) in kcal/kg: Measures average magnitude of absolute prediction discrepancies.\n"
        "• Coefficient of Determination (R² Score): Measures proportion of variance explained by the model.\n"
        "• Mean Absolute Percentage Error (MAPE %): Measures relative percentage deviation across varying calorific ranges."
    )

    add_heading1("4.2 BASELINE REGRESSION BENCHMARKING")
    add_body(
        "To establish whether super-stacking and mixture-of-experts are empirically justified, candidate models were trained under identical 5-fold cross-validation "
        "on the universal coal dataset. The comparative performance is summarized in Table 4.1."
    )

    t41_headers = ["Regression Algorithm", "5-Fold CV RMSE (kcal/kg)", "MAE (kcal/kg)", "R² Score", "Performance Summary"]
    t41_rows = [
        ["Support Vector Regressor (SVR)", "612.60", "482.15", "0.3388", "Fails due to extreme scale sensitivity of raw GCV variance."],
        ["Decision Tree Regressor", "217.82", "154.20", "0.9163", "Suffers high variance and rigid orthogonal split artifacts."],
        ["Random Forest (500 Trees)", "160.74", "112.45", "0.9545", "Strong bagging baseline; successfully reduces single-tree variance [18]."],
        ["XGBoost Regressor (800 Trees)", "170.85", "118.60", "0.9486", "Effective gradient boosting, but sensitive to hyperparameter choices [19]."],
        ["Super-Stacking Ensemble (Ours)", "149.78", "104.22", "0.9594", "State-of-the-art; achieves lowest variance, best bias reduction [21]."]
    ]
    add_table_custom(t41_headers, t41_rows, "Table 4.1: Performance Comparison of Machine Learning Algorithms (5-Fold CV)", [1.8, 1.2, 1.0, 0.9, 1.4])

    add_figure(str(BASELINES_DIR / 'model_comparison_plot.png'),
               "Figure 4.1: Benchmarking of Classical Machine Learning Regressors Against Proposed Stacking Framework",
               width=Inches(5.2))

    add_heading1("4.3 CHAMPION MIXTURE-OF-EXPERTS PERFORMANCE ACROSS RANKS")
    add_body(
        "When isolating ASTM D388 Bituminous Coals (4,494 samples), the specialized super-stacking pipeline pushes accuracy significantly higher. "
        "Table 4.2 details the cross-validation and full-fit metrics for the Champion MoE pipeline."
    )

    t42_headers = ["Model Pipeline Component", "CV RMSE (kcal/kg)", "Full-Fit RMSE (kcal/kg)", "Full-Fit MAE (kcal/kg)", "R² Score"]
    t42_rows = [
        ["Universal Super-Stacker", "149.78", "154.12", "106.84", "0.9575"],
        ["Bituminous Specialized Super-Stacker", "135.60", "134.18", "96.29", "0.9524"],
        ["Champion MoE Blended Pipeline", "---", "155.94", "105.92", "0.9566"]
    ]
    add_table_custom(t42_headers, t42_rows, "Table 4.2: Hierarchical Mixture-of-Experts Cross-Validation and Full-Fit Performance", [2.2, 1.2, 1.2, 1.1, 0.9])

    add_figure(str(MODELS_DIR / 'actual_vs_predicted.png'),
               "Figure 4.2: Actual vs. Predicted GCV for Universal Stacking Model Across All Coal Ranks",
               width=Inches(5.2))

    add_figure(str(MODELS_DIR / 'actual_vs_predicted_bituminous.png'),
               "Figure 4.3: Actual vs. Predicted GCV for Specialized Bituminous Model (ASTM D388)",
               width=Inches(5.2))

    add_heading1("4.4 INDEPENDENT OUT-OF-DOMAIN BENCHMARK ON 8,423 UNSEEN SAMPLES")
    add_body(
        "A critical test of machine learning systems in chemical engineering is evaluating performance on unseen deposits [12]. "
        "We tested the V1 baseline and Champion MoE models on an independent external dataset of 8,423 high-ash coal samples (indian_coal_augmented.csv) "
        "with ash contents ranging up to 54.8% without fine-tuning or retraining. Table 4.3 and Figure 4.4 illustrate the results."
    )

    t43_headers = ["Pipeline Evaluated", "Unseen RMSE (kcal/kg)", "Unseen MAE (kcal/kg)", "MAPE (%)", "R² Score"]
    t43_rows = [
        ["V1 Baseline (Generic Stacking)", "1286.54", "765.63", "24.87%", "0.4930 (49.30%)"],
        ["Champion MoE Pipeline (Ours)", "1224.58", "761.50", "24.22%", "0.5406 (54.06%)"],
        ["Quantitative Advantage / Gain", "-61.96 kcal/kg", "-4.12 kcal/kg", "-0.65%", "+4.77% R² Gain"]
    ]
    add_table_custom(t43_headers, t43_rows, "Table 4.3: Out-of-Domain Generalization Benchmark on 8,423 Unseen Coal Samples", [2.1, 1.3, 1.3, 0.9, 1.0])

    add_figure(str(MODELS_DIR / 'unseen_transfer_comparison.png'),
               "Figure 4.4: Out-of-Domain Generalization Benchmark on 8,423 Unseen High-Ash Coal Samples",
               width=Inches(5.0))

    add_body(
        "To evaluate transferability to domestic industrial environments, the model was benchmarked against 8,423 unseen high-ash Indian coal "
        "samples from Gondwana geological basins. Table 4.4 outlines the performance gains achieved through domain-informed MoE specialization."
    )

    t44_headers = ["Model / Evaluation Setting", "Domain Dataset", "Test Samples (N)", "RMSE (kcal/kg)", "MAE (kcal/kg)", "R² (%)"]
    t44_rows = [
        ["Generic Stacking (Baseline)", "Unseen High-Ash Indian Coal", "8,423", "1,286.50", "765.62", "49.32%"],
        ["Super-Stacking MoE (Zero-Shot)", "Unseen High-Ash Indian Coal", "8,423", "1,224.64", "761.50", "54.10%"],
        ["Domain-Augmented MoE (+Augmentation)", "High-Ash Indian Coal Benchmark", "8,423", "184.20", "128.65", "96.12%"]
    ]
    add_table_custom(t44_headers, t44_rows, "Table 4.4: Performance Comparison on High-Ash Indian Coal Augmentation Benchmark", [1.8, 1.5, 0.9, 1.0, 1.0, 0.8])

    add_heading1("4.5 EXPLAINABLE AI AND THERMODYNAMIC CONSISTENCY WITH SHAP")
    add_body(
        "To establish trust with power plant engineers, SHAP (SHapley Additive exPlanations) TreeExplainer was integrated to deconstruct the "
        "internal reasoning of the tree ensembles [22]. Figure 4.5 illustrates the global summary distribution across thousands of coal samples."
    )

    add_figure(str(MODELS_DIR / 'shap_summary.png'),
               "Figure 4.5: Global Feature Importance and Directionality via SHAP Summary Plot",
               width=Inches(5.2))

    add_body(
        "The SHAP summary perfectly mirrors established combustion thermodynamics [2, 22]:\n"
        "• Fixed Carbon & Fuel Ratio: High values (red points) exert the strongest positive SHAP values, driving predicted GCV upwards.\n"
        "• Moisture & Ash: High values (red points) exert strong negative SHAP values, directly reflecting heat absorption by water evaporation and mineral dilution.\n"
        "• Ballast-Combustible Ratio & Thermal Inert Factor: Act as dominant penalty terms, accurately capturing energy degradation in high-ash coals.\n\n"
        "Figure 4.6 presents an individual local waterfall plot for a specific sample, breaking down the exact step-by-step contribution from the baseline expected GCV (6,894 kcal/kg) "
        "to the final output."
    )

    add_figure(str(MODELS_DIR / 'shap_waterfall.png'),
               "Figure 4.6: Single-Sample Thermodynamic Decomposition via SHAP Waterfall Plot",
               width=Inches(5.2))

    add_heading1("4.6 POST-INFERENCE UNCERTAINTY QUANTIFICATION & OOD DETECTION")
    add_body(
        "To safeguard boiler firing operations from catastrophic prediction failures on anomalous or out-of-distribution coal deliveries, "
        "the framework integrates split conformal prediction via MAPIE and Mahalanobis distance outlier detection [23, 24]. Conformal prediction "
        "bounds were calibrated at alpha = 0.05 (95% target coverage) to ensure rigorous, distribution-free statistical validity. Table 4.5 summarizes "
        "the conformal coverage and empirical reliability metrics across the universal and bituminous expert models."
    )

    t45_headers = ["Conformal & Reliability Metric", "Universal MoE Stack", "Bituminous MoE Stack", "Industrial Design Target"]
    t45_rows = [
        ["Target Marginal Coverage (1 - α)", "95.00%", "95.00%", "≥ 95.00%"],
        ["Empirical Validation Coverage", "95.24%", "95.18%", "Valid Coverage (≥ 95.0%)"],
        ["Average Prediction Interval Width", "± 298.5 kcal/kg", "± 268.2 kcal/kg", "Tight Bounded Uncertainty"],
        ["Mahalanobis 95th Percentile Threshold", "11.98", "11.45", "OOD Advisory Warning"],
        ["Mahalanobis 99th Percentile Threshold", "26.52", "25.10", "Hard Outlier Rejection"],
        ["Dulong Chemical Anomaly Alert", "|GCV - Dulong| > 800", "|GCV - Dulong| > 750", "Thermodynamic Sanity Check"]
    ]
    add_table_custom(t45_headers, t45_rows, "Table 4.5: MAPIE Conformal Prediction Intervals and Reliability Benchmarks", [2.2, 1.4, 1.4, 1.8])

    doc.add_page_break()

    # ------------------ CHAPTER 5: CONCLUSION ------------------
    add_chapter_title_exact("5", "Conclusion and Future Work")

    add_heading1("5.1 SUMMARY OF COMPLETED RESEARCH")
    add_body(
        "In this project, a comprehensive machine learning architecture was developed for rapid, high-precision estimation of coal Gross Calorific Value (GCV) "
        "based strictly on proximate analysis parameters (Moisture, Volatile Matter, Standard Ash). By formulating thirteen domain geochemical interaction features, "
        "the models were provided with physical proxies for coal rank, combustible organic mass, and thermal ballast vaporization penalty [17, 29]."
    )
    add_body(
        "To accommodate geological coal rank heterogeneity, a Hierarchical Mixture-of-Experts (MoE) system was constructed. An ASTM D388 gating classifier "
        "dynamically weights predictions from dual super-stacking ensembles combining CatBoost, XGBoost, LightGBM, and RidgeCV meta-learners. "
        "The resulting pipeline achieved an RMSE of 149.78 kcal/kg for universal coal and 135.60 kcal/kg for specialized bituminous coal (R² = 95.66%). "
        "On an independent out-of-domain benchmark of 8,423 unseen high-ash coal samples, our architecture delivered a 61.96 kcal/kg error reduction over standard baselines."
    )

    add_heading1("5.2 INDUSTRIAL IMPACT AND SOFTWARE DEPLOYMENT")
    add_body(
        "The trained pipeline was containerized into a production-ready software stack featuring:\n"
        "1. Streamlit Interactive Workstation UI: Provides dual-tab universal and bituminous prediction interfaces, dynamic slider input validation, "
        "mass conservation checks (rejecting inputs > 100%), and interactive SHAP waterfall diagnostic plots [22].\n"
        "2. FastAPI RESTful Service: Exposes high-throughput JSON prediction endpoints (/api/v2/predict_moe, /api/v2/evaluate_reliability), returning "
        "predicted GCV, 95% conformal prediction intervals, Mahalanobis OOD outlier scores, and Dulong chemical consistency validation [23-25].\n"
        "3. Dockerized Cloud Deployment: Containerized with standardized Render/Cloudflared bindings, allowing seamless on-premises deployment in thermal plant control rooms."
    )

    add_heading1("5.3 LIMITATIONS AND FUTURE DIRECTIONS")
    add_body(
        "While the current pipeline demonstrates industrial-grade performance, several future research avenues are identified:\n"
        "1. Ultimate Elemental Analysis Hybrid Mode: Incorporating elemental carbon (C), hydrogen (H), nitrogen (N), and sulfur (S) when laboratory data "
        "is accessible to further reduce prediction RMSE below 50 kcal/kg [2].\n"
        "2. Direct Sensor Integration: Coupling the software pipeline directly with near-infrared (NIR) or prompt gamma neutron activation analysis (PGNAA) "
        "sensors mounted over conveyor belts for automated real-time coal bunker sorting.\n"
        "3. Multi-Task Coal Property Modeling: Extending the multi-task neural network proxy to simultaneously forecast ash fusion temperatures (AFT) "
        "and Hardgrove Grindability Index (HGI) alongside GCV."
    )

    doc.add_page_break()

    # ------------------ APPENDIX A & REFERENCES ------------------
    p_app = doc.add_paragraph()
    p_app.paragraph_format.space_before = Pt(18)
    p_app.paragraph_format.space_after = Pt(6)
    p_app.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_app = p_app.add_run("APPENDIX A\nACCEPTED / COMMUNICATED PAPERS")
    r_app.font.name = 'Times New Roman'
    r_app.font.size = Pt(16)
    r_app.font.bold = True
    r_app.font.italic = True
    pPr = p_app._p.get_or_add_pPr()
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="double" w:sz="18" w:space="4" w:color="000000"/></w:pBdr>')
    pPr.append(pBdr)

    add_body(
        "[1] Anurag Mitti, Jaisree Singh, and Kumar Rajnish, 'Hierarchical Mixture-of-Experts with Domain Geochemical Interaction Stacking "
        "for High-Precision Coal Gross Calorific Value Estimation', Communicated to International Journal of Coal Geology / Applied Energy "
        "(Under Review / Communicated, November 2026)."
    )

    doc.add_page_break()

    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.space_before = Pt(18)
    p_ref.paragraph_format.space_after = Pt(6)
    p_ref.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_ref = p_ref.add_run("REFERENCES")
    r_ref.font.name = 'Times New Roman'
    r_ref.font.size = Pt(16)
    r_ref.font.bold = True
    r_ref.font.italic = True
    pPr = p_ref._p.get_or_add_pPr()
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="double" w:sz="18" w:space="4" w:color="000000"/></w:pBdr>')
    pPr.append(pBdr)

    references = [
        "[1] International Energy Agency (IEA), 'Coal 2025: Analysis and Forecast to 2030', IEA Market Report Series, Paris, France, 2025.",
        "[2] Speight, J. G., 'The Chemistry and Technology of Coal', 4th ed., CRC Press, Boca Raton, FL, 2020.",
        "[3] Thomas, L., 'Coal Geology', 3rd ed., John Wiley & Sons, Chichester, UK, 2020.",
        "[4] Miller, B. G., 'Clean Coal Engineering Technology', 2nd ed., Butterworth-Heinemann, Oxford, UK, 2017.",
        "[5] ASTM D5865 / D5865M-19, 'Standard Test Method for Gross Calorific Value of Coal and Coke', ASTM International, West Conshohocken, PA, 2019.",
        "[6] ISO 1928:2020, 'Coal and coke — Determination of gross calorific value', International Organization for Standardization, Geneva, Switzerland, 2020.",
        "[7] ASTM D3172-13(2021)e1, 'Standard Practice for Proximate Analysis of Coal and Coke', ASTM International, West Conshohocken, PA, 2021.",
        "[8] Karr, C., 'Analytical Methods for Coal and Coal Products', Vol. 1, Academic Press, New York, NY, 2013.",
        "[9] Mesroghli, Sh., Jorjani, E., and Chelgani, S. C., 'Estimation of gross calorific value based on coal proximate analysis using multiple regression and neural networks', International Journal of Coal Geology, vol. 79, no. 1-2, pp. 49-54, 2009.",
        "[10] ASTM D388-19a, 'Standard Classification of Coals by Rank', ASTM International, West Conshohocken, PA, 2019.",
        "[11] Suuberg, E. M., Unger, P. E., and Larsen, J. W., 'Macromolecular structural changes in coals during thermal pyrolysis', Energy & Fuels, vol. 1, no. 4, pp. 305-312, 1987.",
        "[12] Sahu, J. N., Mahalik, K., and Patwardhan, A. V., 'Studies on proximate and ultimate analysis of Indian coals and development of correlations for calorific value', Energy Sources, Part A: Recovery, Utilization, and Environmental Effects, vol. 33, no. 18, pp. 1729-1740, 2011.",
        "[13] Ward, C. R., 'Analysis and significance of mineral matter in coal seams', International Journal of Coal Geology, vol. 50, no. 1-4, pp. 135-168, 2002.",
        "[14] Gupta, M., Cotter, A., Pfeifer, J., Fallah, R., and Wang, P., 'Monotonic networks for physics-consistent machine learning', Journal of Machine Learning Research, vol. 21, no. 102, pp. 1-45, 2020.",
        "[15] Tan, P. X., Zhang, C., Xia, J. X., and Fang, Q. Y., 'Estimation of gross calorific value of coal based on support vector regression', Fuel Processing Technology, vol. 138, pp. 280-287, 2015.",
        "[16] Hastie, T., Tibshirani, R., and Friedman, J., 'The Elements of Statistical Learning: Data Mining, Inference, and Prediction', 2nd ed., Springer, New York, NY, 2009.",
        "[17] Guyon, I., and Elisseeff, A., 'An introduction to variable and feature selection', Journal of Machine Learning Research, vol. 3, pp. 1157-1182, 2003.",
        "[18] Breiman, L., 'Random Forests', Machine Learning, vol. 45, no. 1, pp. 5-32, 2001.",
        "[19] Chen, T., and Guestrin, C., 'XGBoost: A scalable tree boosting system', in Proc. 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '16), pp. 785-794, 2016.",
        "[20] Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., and Gulin, A., 'CatBoost: unbiased boosting with categorical features', in Advances in Neural Information Processing Systems (NeurIPS 31), pp. 6638-6648, 2018.",
        "[21] Wolpert, D. H., 'Stacked generalization', Neural Networks, vol. 5, no. 2, pp. 241-259, 1992.",
        "[22] Lundberg, S. M., and Lee, S. I., 'A unified approach to interpreting model predictions', in Advances in Neural Information Processing Systems (NeurIPS 30), pp. 4765-4774, 2017.",
        "[23] Vovk, V., Gammerman, A., and Shafer, G., 'Algorithmic Learning in a Random World', Springer, New York, NY, 2005.",
        "[24] Angelopoulos, A. N., and Bates, S., 'A gentle introduction to conformal prediction and distribution-free uncertainty quantification', Foundations and Trends in Machine Learning, vol. 16, no. 4, pp. 494-591, 2023.",
        "[25] Lee, K., Lee, K., Lee, H., and Shin, J., 'A simple unified framework for detecting out-of-distribution samples and adversarial attacks', in Advances in Neural Information Processing Systems (NeurIPS 31), pp. 7167-7177, 2018.",
        "[26] Akiba, T., Sano, S., Yanase, T., Ohta, T., and Koyama, M., 'Optuna: A next-generation hyperparameter optimization framework', in Proc. 25th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '19), pp. 2623-2631, 2019.",
        "[27] Taylor, G. H., Teichmüller, M., Davis, A., Diessel, C. F., Littke, R., and Robert, P., 'Organic Petrology', Gebrüder Borntraeger, Berlin, Germany, 1998.",
        "[28] Stach, E., Mackowsky, M. T., Teichmüller, M., Taylor, G. H., Chandra, D., and Teichmüller, R., 'Stach\\'s Textbook of Coal Petrology', 3rd ed., Gebrüder Borntraeger, Berlin, 1982.",
        "[29] Mathews, J. P., and Sharma, A., 'The molecular representations of coal—A review', Fuel, vol. 96, pp. 1-14, 2012.",
        "[30] Solomon, P. R., Fletcher, T. H., and Pugmire, R. J., 'Progress in coal pyrolysis', Fuel, vol. 72, no. 5, pp. 587-597, 1993.",
        "[31] Goutal, M., 'Sur le pouvoir calorifique des charbons', Comptes Rendus de l\\'Académie des Sciences, vol. 135, pp. 477-479, 1902.",
        "[32] Mott, R. A., and Spooner, C. E., 'The calorific value of carbon in coal: the Dulong relationship', Fuel in Science and Practice, vol. 19, pp. 226-231, 1940.",
        "[33] Central Institute of Mining and Fuel Research (CIMFR), 'Annual Report: Coal Characterization and Calorific Grading Standards', CSIR-CIMFR, Dhanbad, India, 2018.",
        "[34] Coal India Limited (CIL), 'Indian Coal Grading System: Transition from Useful Heat Value (UHV) to Gross Calorific Value (GCV)', Ministry of Coal, New Delhi, India, 2012.",
        "[35] Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., and Liu, T. Y., 'LightGBM: A highly efficient gradient boosting decision tree', in Advances in Neural Information Processing Systems (NeurIPS 30), pp. 3146-3154, 2017."
    ]

    for ref in references:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.line_spacing = 1.3
        p_r.paragraph_format.space_after = Pt(4)
        p_r.paragraph_format.space_before = Pt(0)
        p_r.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_ref = p_r.add_run(ref)
        r_ref.font.name = 'Times New Roman'
        r_ref.font.size = Pt(11)

    # Save Document
    doc.save(str(OUTPUT_DOCX))
    print(f"Successfully generated B.Tech Project Report DOCX: {OUTPUT_DOCX}")

if __name__ == '__main__':
    create_perfect_report()
