import markdown
from weasyprint import HTML
import tempfile
import os

def convert_md_to_pdf(markdown_text, output_filename):
    """
    Convert markdown text to a PDF file

    Args:
        markdown_text (str): Markdown formatted text
        output_filename (str): Name of the output PDF file
    """
    # Convert markdown to HTML
    html_text = markdown.markdown(markdown_text, extensions=['tables'])

    # Add some basic CSS for better formatting
    styled_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                line-height: 1.5;
            }}
            h1 {{
                text-align: center;
                color: #333;
            }}
            h2 {{
                color: #2c5282;
                border-bottom: 1px solid #eee;
                padding-bottom: 5px;
            }}
            table {{
                border-collapse: collapse;
                width: 100%;
                margin: 15px 0;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
            }}
            th {{
                background-color: #f2f2f2;
            }}
            hr {{
                border: none;
                height: 1px;
                background-color: #ddd;
                margin: 20px 0;
            }}
            .footer {{
                margin-top: 30px;
                font-style: italic;
                text-align: center;
                color: #777;
            }}
        </style>
    </head>
    <body>
        {html_text}
        <div class="footer">
            This document was generated for AI testing purposes. All data is synthetic.
        </div>
    </body>
    </html>
    """

    # Create temporary HTML file
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
        f.write(styled_html.encode('utf-8'))
        temp_html_filename = f.name

    # Convert HTML to PDF
    HTML(filename=temp_html_filename).write_pdf(output_filename)

    # Remove temporary file
    os.unlink(temp_html_filename)

    print(f"PDF created successfully at: {output_filename}")


# Read the markdown content from a file or use a string directly
# For this example, I'll use a multiline string
markdown_text = """# MEDICAL REPORT
## MEMORIAL HEALTHCARE SYSTEM
**Facility ID**: MHS-2023-774
**Report Date**: March 12, 2025

---

## PATIENT INFORMATION
**Patient ID**: MHS-P112233
**Name**: SMITH, JOHN DOE
**DOB**: 05/15/1975
**Sex**: Male
**MRN**: 987654321
**Admission Date**: March 10, 2025
**Primary Physician**: Dr. Elizabeth Chen

---

## REASON FOR VISIT
Patient presented with complaints of persistent cough for 3 weeks, intermittent fever, and fatigue.

---

## VITAL SIGNS
- **Temperature**: 38.2 °C
- **Blood Pressure**: 128/82 mmHg
- **Heart Rate**: 88 bpm
- **Respiratory Rate**: 22 breaths/min
- **Oxygen Saturation**: 96% on room air

---

## PHYSICAL EXAMINATION
**General**: Patient is a 49-year-old male, alert and oriented x3, in mild respiratory distress
**HEENT**: Normocephalic, atraumatic, Oropharynx is clear, No cervical lymphadenopathy
**Chest**: Decreased breath sounds in right lower lobe, Dull to percussion
**Cardiovascular**: Regular rate and rhythm, No murmurs, gallops, or rubs
**Abdomen**: Soft, non-tender, non-distended, Normal bowel sounds
**Extremities**: No edema, Normal peripheral pulses
**Neurological**: Grossly intact, No focal deficits

---

## LABORATORY RESULTS
**CBC**:
- WBC: 12.4 × 10^9/L (High)
- RBC: 4.5 × 10^12/L
- Hemoglobin: 14.2 g/dL
- Hematocrit: 42%
- Platelets: 250 × 10^9/L

**Chemistry**:
- Sodium: 138 mEq/L
- Potassium: 4.1 mEq/L
- Chloride: 101 mEq/L
- BUN: 15 mg/dL
- Creatinine: 0.9 mg/dL
- Glucose: 105 mg/dL

**Inflammatory Markers**:
- CRP: 75 mg/L (High)
- ESR: 45 mm/hr (High)

---

## IMAGING
**Chest X-ray**: Right lower lobe consolidation consistent with pneumonia. No pleural effusion or pneumothorax.

**CT Chest (contrast)**:
- Right lower lobe consolidation with air bronchograms
- No evidence of pulmonary embolism
- Small reactive right hilar lymphadenopathy
- No pleural effusion

---

## MICROBIOLOGY
**Sputum Culture**:
- Sample quality: Acceptable
- Predominant organism: Streptococcus pneumoniae
- Antibiotic sensitivity: Sensitive to penicillin, amoxicillin, ceftriaxone

---

## ASSESSMENT
1. Community-acquired pneumonia, right lower lobe, moderate severity
2. Mild dehydration
3. History of seasonal allergies

---

## TREATMENT PLAN
1. Antibiotic therapy: Ceftriaxone 1g IV daily for 3 days, then transition to oral amoxicillin 500mg TID for 7 days
2. Antipyretics: Acetaminophen 650mg Q6H PRN for fever/pain
3. IV fluids: 0.9% NS at 100mL/hr for 24 hours, then reassess
4. Incentive spirometry Q2H while awake
5. Oxygen therapy: PRN to maintain O2 saturation > 92%

---

## RECOMMENDATIONS
1. Follow up with primary care physician in 7-10 days
2. Repeat chest X-ray in 4-6 weeks
3. Rest and adequate hydration
4. Return to ED if symptoms worsen or fever persists beyond 48 hours of antibiotic therapy

---

## DISPOSITION
Patient admitted to Medical Floor, Room 415

---

## NOTES
Patient has no known drug allergies. Patient received pneumococcal vaccine 2 years ago. No recent travel history.

---

## SIGNATURE
**Attending Physician**: Dr. Michael Rodriguez, MD
**Electronic Signature ID**: MR72254
**Date & Time**: March 12, 2025, 14:30

*This is a synthetic medical document created for AI testing purposes. All patient information is fictional and does not represent a real person.*
"""

# Generate the PDF
output_file = "synthetic_medical_report.pdf"
convert_md_to_pdf(markdown_text, output_file)
