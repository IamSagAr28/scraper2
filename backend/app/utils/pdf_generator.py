from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from typing import List
import os
from datetime import datetime
from app.models.schemas import CauseListData, CauseListEntry

class PDFGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            spaceAfter=30,
            alignment=1,  # Center alignment
            textColor=colors.darkblue
        )
        self.header_style = ParagraphStyle(
            'CustomHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            spaceAfter=12,
            textColor=colors.black
        )
    
    def generate_cause_list_pdf(self, cause_list_data: CauseListData, output_path: str) -> str:
        """Generate PDF for a single cause list"""
        try:
            doc = SimpleDocTemplate(output_path, pagesize=A4)
            story = []
            
            # Title
            title = Paragraph(f"CAUSE LIST", self.title_style)
            story.append(title)
            story.append(Spacer(1, 12))
            
            # Court and Judge Information
            court_info = f"<b>Court:</b> {cause_list_data.court_name}<br/>"
            court_info += f"<b>Judge:</b> {cause_list_data.judge_name}<br/>"
            court_info += f"<b>Date:</b> {cause_list_data.date}<br/>"
            court_info += f"<b>Case Type:</b> {cause_list_data.case_type.upper()}"
            
            court_para = Paragraph(court_info, self.header_style)
            story.append(court_para)
            story.append(Spacer(1, 20))
            
            if cause_list_data.entries:
                # Create table data
                table_data = [
                    ['Sr. No.', 'Case Number', 'Case Title', 'Petitioner', 'Respondent', 'Advocate', 'Purpose']
                ]
                
                for entry in cause_list_data.entries:
                    row = [
                        entry.sr_no or '',
                        entry.case_number or '',
                        entry.case_title or '',
                        entry.petitioner or '',
                        entry.respondent or '',
                        entry.advocate or '',
                        entry.purpose or ''
                    ]
                    table_data.append(row)
                
                # Create table
                table = Table(table_data, colWidths=[0.8*inch, 1.5*inch, 2*inch, 1.5*inch, 1.5*inch, 1.2*inch, 1*inch])
                
                # Table style
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('FONTSIZE', (0, 1), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                
                story.append(table)
            else:
                no_cases = Paragraph("No cases listed for this date.", self.styles['Normal'])
                story.append(no_cases)
            
            # Footer
            story.append(Spacer(1, 30))
            footer = Paragraph(
                f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>"
                "Note: This cause list is generated from publicly available data and may differ from the actual court cause list.",
                self.styles['Normal']
            )
            story.append(footer)
            
            # Build PDF
            doc.build(story)
            return output_path
            
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            raise e
    
    def generate_multiple_cause_lists_pdf(self, cause_lists: List[CauseListData], output_dir: str) -> List[str]:
        """Generate multiple PDFs for different cause lists"""
        pdf_files = []
        
        for i, cause_list in enumerate(cause_lists):
            # Create filename
            safe_judge_name = "".join(c for c in cause_list.judge_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_judge_name = safe_judge_name.replace(' ', '_')
            filename = f"causelist_{safe_judge_name}_{cause_list.date}_{cause_list.case_type}.pdf"
            output_path = os.path.join(output_dir, filename)
            
            try:
                pdf_path = self.generate_cause_list_pdf(cause_list, output_path)
                pdf_files.append(pdf_path)
            except Exception as e:
                print(f"Error generating PDF for {cause_list.judge_name}: {str(e)}")
                continue
        
        return pdf_files
    
    def create_output_directory(self, base_dir: str = "output") -> str:
        """Create output directory for PDFs"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = os.path.join(base_dir, f"cause_lists_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
