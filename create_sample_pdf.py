"""
Create a sample HR policy PDF for testing the chatbot
"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os

def create_sample_hr_policy():
    """Create a sample HR policy PDF"""
    
    # Ensure uploads directory exists
    os.makedirs('uploads', exist_ok=True)
    
    # Create PDF
    pdf_path = 'uploads/sample_hr_policy.pdf'
    doc = SimpleDocTemplate(pdf_path, pagesize=letter)
    
    # Container for the 'Flowable' objects
    elements = []
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='darkblue',
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = styles['Heading2']
    normal_style = styles['BodyText']
    normal_style.alignment = TA_JUSTIFY
    
    # Title
    title = Paragraph("COMPANY HR POLICY MANUAL", title_style)
    elements.append(title)
    elements.append(Spacer(1, 0.5*inch))
    
    # Introduction
    intro = Paragraph(
        "This document outlines the Human Resources policies and procedures for all employees. "
        "Please read this manual carefully and refer to it when you have questions about company policies.",
        normal_style
    )
    elements.append(intro)
    elements.append(Spacer(1, 0.3*inch))
    
    # Leave Policy Section
    elements.append(Paragraph("1. LEAVE POLICY", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("1.1 Annual Leave", styles['Heading3']))
    annual_leave = Paragraph(
        "Permanent employees are entitled to 14 days of annual leave per year. "
        "Annual leave must be requested at least 2 weeks in advance and is subject to manager approval. "
        "Unused annual leave can be carried forward to the next year, up to a maximum of 7 days.",
        normal_style
    )
    elements.append(annual_leave)
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("1.2 Sick Leave", styles['Heading3']))
    sick_leave = Paragraph(
        "Employees are entitled to 10 days of sick leave per year. "
        "A medical certificate is required for sick leave exceeding 2 consecutive days. "
        "Sick leave cannot be carried forward to the next year.",
        normal_style
    )
    elements.append(sick_leave)
    elements.append(Spacer(1, 0.2*inch))
    
    elements.append(Paragraph("1.3 Maternity Leave", styles['Heading3']))
    maternity_leave = Paragraph(
        "Female employees are entitled to 12 weeks of maternity leave. "
        "Maternity leave should be notified to HR at least 4 weeks before the expected delivery date. "
        "The leave can be split as 2 weeks before delivery and 10 weeks after delivery.",
        normal_style
    )
    elements.append(maternity_leave)
    elements.append(Spacer(1, 0.3*inch))
    
    # Work From Home Policy
    elements.append(Paragraph("2. WORK FROM HOME POLICY", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    wfh_policy = Paragraph(
        "Employees may work from home up to 2 days per week with prior manager approval. "
        "Work from home requests must be submitted through the HR portal at least 24 hours in advance. "
        "Employees must be available during core working hours (10 AM - 4 PM) and maintain regular communication with their team.",
        normal_style
    )
    elements.append(wfh_policy)
    elements.append(Spacer(1, 0.3*inch))
    
    # Notice Period
    elements.append(Paragraph("3. RESIGNATION AND NOTICE PERIOD", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    notice_period = Paragraph(
        "Employees wishing to resign must provide written notice to their manager and HR department. "
        "The notice period is as follows:<br/>"
        "• Probationary employees: 2 weeks<br/>"
        "• Permanent employees (0-2 years): 1 month<br/>"
        "• Permanent employees (2+ years): 2 months<br/>"
        "The company reserves the right to waive the notice period or accept payment in lieu of notice.",
        normal_style
    )
    elements.append(notice_period)
    elements.append(Spacer(1, 0.3*inch))
    
    # Medical Benefits
    elements.append(Paragraph("4. MEDICAL BENEFITS", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    medical_benefits = Paragraph(
        "All permanent employees are covered under the company's group medical insurance plan. "
        "The coverage includes:<br/>"
        "• Hospitalization: Up to $50,000 per year<br/>"
        "• Outpatient: Up to $2,000 per year<br/>"
        "• Dental: Up to $500 per year<br/>"
        "• Optical: Up to $300 per year<br/>"
        "Employees can add dependents (spouse and children) at a subsidized rate of 50% of the premium cost.",
        normal_style
    )
    elements.append(medical_benefits)
    elements.append(Spacer(1, 0.3*inch))
    
    # Travel Reimbursement
    elements.append(Paragraph("5. TRAVEL AND EXPENSE REIMBURSEMENT", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    travel_policy = Paragraph(
        "Employees traveling for business purposes are entitled to reimbursement of approved expenses. "
        "All expenses must be submitted within 30 days of incurring them, with valid receipts. "
        "Reimbursement rates:<br/>"
        "• Domestic travel: Economy class flights, up to $150 per night for accommodation<br/>"
        "• International travel: Economy class flights (Business class for flights over 6 hours), up to $200 per night for accommodation<br/>"
        "• Meals: Up to $50 per day for domestic travel, $75 per day for international travel<br/>"
        "• Local transportation: Actual costs with receipts",
        normal_style
    )
    elements.append(travel_policy)
    elements.append(Spacer(1, 0.3*inch))
    
    # Probation Period
    elements.append(Paragraph("6. PROBATION PERIOD", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    probation = Paragraph(
        "All new employees are subject to a probation period of 3 months from their date of joining. "
        "During this period, performance will be evaluated, and employment may be terminated with 1 week notice from either party. "
        "Upon successful completion of probation, employees will receive a confirmation letter and become eligible for all company benefits.",
        normal_style
    )
    elements.append(probation)
    elements.append(Spacer(1, 0.3*inch))
    
    # Working Hours
    elements.append(Paragraph("7. WORKING HOURS", heading_style))
    elements.append(Spacer(1, 0.2*inch))
    
    working_hours = Paragraph(
        "Standard working hours are 9:00 AM to 6:00 PM, Monday to Friday, with a 1-hour lunch break. "
        "Employees are expected to work 40 hours per week. "
        "Flexible working hours may be arranged with manager approval, provided core hours (10 AM - 4 PM) are maintained.",
        normal_style
    )
    elements.append(working_hours)
    
    # Build PDF
    doc.build(elements)
    print(f"✅ Sample HR policy PDF created: {pdf_path}")
    return pdf_path

if __name__ == "__main__":
    create_sample_hr_policy()
