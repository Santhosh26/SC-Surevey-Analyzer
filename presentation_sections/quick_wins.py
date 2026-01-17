"""
Quick Wins Section - Enhanced with Charts
"""

from collections import Counter
from pptx import Presentation
from pptx.util import Inches, Pt
from fpdf import FPDF

from .base import BaseSection
from .charts import ChartGenerator


class QuickWinsSection(BaseSection):
    """
    Generates Quick Wins slides from Stop Doing / Start Doing questions.

    Enhanced with:
    - Side-by-side bar charts comparing Stop vs Start
    - Visual frequency ranking

    Requires: raw-data.csv (questions containing "STOP" or "START")
    """

    def get_slide_count(self) -> int:
        return 1  # Combined into single slide with dual chart

    def _get_quick_wins(self) -> dict:
        """Extract stop/start doing responses."""
        raw_data = self.data.get('raw_data')
        if raw_data is None:
            return {'stop': [], 'start': []}

        # Find STOP and START questions
        stop_responses = []
        start_responses = []

        for _, row in raw_data.iterrows():
            q = str(row['Question']).lower()
            r = str(row['Response']).strip()
            if r and r.lower() != 'nan':
                if 'stop' in q:
                    stop_responses.append(r)
                elif 'start' in q:
                    start_responses.append(r)

        # Get top responses by frequency
        def get_top_themes(responses, n=8):
            if not responses:
                return []
            counter = Counter(responses)
            return [{'text': text, 'count': count}
                    for text, count in counter.most_common(n)]

        return {
            'stop': get_top_themes(stop_responses),
            'start': get_top_themes(start_responses),
            'stop_total': len(stop_responses),
            'start_total': len(start_responses),
        }

    def generate_pptx_slides(self, prs: Presentation) -> Presentation:
        data = self._get_quick_wins()
        charts = ChartGenerator()

        slide = self.add_content_slide(prs, "Quick Wins: Stop vs Start")

        # Convert data for chart
        stop_data = [(item['text'], item['count']) for item in data['stop']]
        start_data = [(item['text'], item['count']) for item in data['start']]

        # Generate dual bar chart
        if stop_data or start_data:
            chart_path = charts.dual_bar_chart(
                stop_data,
                start_data,
                left_title="STOP DOING",
                right_title="START DOING",
                left_color='negative',
                right_color='positive',
                max_items=6,
                figsize=(12, 5)
            )
            self.add_chart_image(slide, chart_path, 0.3, 1.3, 12.5, 5)

        # Summary metrics at bottom
        self.add_text_box(
            slide, 1.0, 6.5, 5.0, 0.4,
            f"Total STOP responses: {data['stop_total']}",
            font_size=10, color='negative'
        )
        self.add_text_box(
            slide, 7.0, 6.5, 5.0, 0.4,
            f"Total START responses: {data['start_total']}",
            font_size=10, color='positive'
        )

        # Key insight
        if data['stop'] and data['start']:
            top_stop = data['stop'][0]['text'][:40]
            top_start = data['start'][0]['text'][:40]
            self.add_text_box(
                slide, 0.5, 6.9, 12.0, 0.4,
                f"Priority: Stop '{top_stop}...' and Start '{top_start}...'",
                font_size=10, bold=True, color='secondary', align='center'
            )

        charts.cleanup()
        return prs

    def generate_pdf_content(self, pdf: FPDF) -> FPDF:
        data = self._get_quick_wins()

        self.pdf_add_content_page(pdf, "Quick Wins: Stop vs Start")

        # Two-column layout simulation
        pdf.set_font('Helvetica', 'B', 14)

        # STOP section
        pdf.set_text_color(*self.pdf_colors['negative'])
        pdf.cell(0, 10, "STOP DOING", new_x='LMARGIN', new_y='NEXT')

        if data['stop']:
            max_count = max(item['count'] for item in data['stop'])
            for item in data['stop'][:6]:
                pdf.set_font('Helvetica', '', 10)
                pdf.set_text_color(*self.pdf_colors['text'])
                label = item['text'][:45] + '...' if len(item['text']) > 45 else item['text']
                pdf.cell(120, 6, f"  {label}")

                # Bar
                bar_width = (item['count'] / max_count) * 50
                pdf.set_fill_color(*self.pdf_colors['negative'])
                pdf.cell(bar_width, 6, '', fill=True)

                pdf.set_font('Helvetica', 'B', 9)
                pdf.cell(0, 6, f" {item['count']}", new_x='LMARGIN', new_y='NEXT')
        else:
            pdf.set_font('Helvetica', 'I', 10)
            pdf.cell(0, 8, "  No data available", new_x='LMARGIN', new_y='NEXT')

        pdf.ln(8)

        # START section
        pdf.set_font('Helvetica', 'B', 14)
        pdf.set_text_color(*self.pdf_colors['positive'])
        pdf.cell(0, 10, "START DOING", new_x='LMARGIN', new_y='NEXT')

        if data['start']:
            max_count = max(item['count'] for item in data['start'])
            for item in data['start'][:6]:
                pdf.set_font('Helvetica', '', 10)
                pdf.set_text_color(*self.pdf_colors['text'])
                label = item['text'][:45] + '...' if len(item['text']) > 45 else item['text']
                pdf.cell(120, 6, f"  {label}")

                # Bar
                bar_width = (item['count'] / max_count) * 50
                pdf.set_fill_color(*self.pdf_colors['positive'])
                pdf.cell(bar_width, 6, '', fill=True)

                pdf.set_font('Helvetica', 'B', 9)
                pdf.cell(0, 6, f" {item['count']}", new_x='LMARGIN', new_y='NEXT')
        else:
            pdf.set_font('Helvetica', 'I', 10)
            pdf.cell(0, 8, "  No data available", new_x='LMARGIN', new_y='NEXT')

        pdf.set_text_color(*self.pdf_colors['text'])
        return pdf
