"""
Cross-Question Insights Section
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from fpdf import FPDF

from .base import BaseSection


class CrossQuestionSection(BaseSection):
    """
    Generates Cross-Question Insights slide from LLM summaries.

    Requires: llm_summaries.json (overall_summary.cross_question_insights)
    """

    def get_slide_count(self) -> int:
        return 1

    def _get_insights(self) -> dict:
        """Extract cross-question insights from LLM data."""
        llm_data = self.data.get('llm_summaries', {})
        overall = llm_data.get('overall_summary', {})
        insights = overall.get('cross_question_insights', {})

        if not insights:
            return {
                'alignments': ['Data not available'],
                'contradictions': ['Data not available'],
                'emerging_patterns': ['Data not available'],
            }

        return insights

    def generate_pptx_slides(self, prs: Presentation) -> Presentation:
        insights = self._get_insights()

        slide = self.add_content_slide(prs, "Cross-Question Insights")

        categories = [
            ('Alignments', insights.get('alignments', []), 'positive'),
            ('Tensions', insights.get('contradictions', []), 'negative'),
            ('Emerging Patterns', insights.get('emerging_patterns', []), 'accent'),
        ]

        col_width = 4.0
        x_positions = [0.5, 4.7, 8.9]

        for i, (title, items, color) in enumerate(categories):
            x = x_positions[i]

            # Category header
            self.add_text_box(
                slide, x, 1.3, col_width, 0.5,
                title, font_size=16, bold=True, color=color
            )

            # Items
            y_pos = 1.9
            for item in items[:4]:  # Max 4 items per category
                self.add_text_box(
                    slide, x, y_pos, col_width, 1.2,
                    f"  {item}", font_size=10, color='text'
                )
                y_pos += 1.3

        return prs

    def generate_pdf_content(self, pdf: FPDF) -> FPDF:
        insights = self._get_insights()

        self.pdf_add_content_page(pdf, "Cross-Question Insights")

        categories = [
            ('Alignments', insights.get('alignments', []), self.pdf_colors['positive']),
            ('Tensions', insights.get('contradictions', []), self.pdf_colors['negative']),
            ('Emerging Patterns', insights.get('emerging_patterns', []), self.pdf_colors['accent']),
        ]

        for title, items, color in categories:
            pdf.set_font('Helvetica', 'B', 12)
            pdf.set_text_color(*color)
            pdf.cell(0, 8, title, new_x='LMARGIN', new_y='NEXT')

            pdf.set_font('Helvetica', '', 10)
            pdf.set_text_color(*self.pdf_colors['text'])
            for item in items[:4]:
                pdf.cell(5, 6, chr(149))
                pdf.multi_cell(0, 6, item)

            pdf.ln(4)

        return pdf
