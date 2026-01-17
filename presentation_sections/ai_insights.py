"""
AI Insights (Full) Section
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from fpdf import FPDF

from .base import BaseSection


class AIInsightsSection(BaseSection):
    """
    Generates comprehensive AI Insights slides from LLM summaries.

    Requires: llm_summaries.json (question_summaries)

    Shows per-question analysis with:
    - Executive summary
    - Key themes
    - Representative quotes
    - Actionable insights
    """

    def get_slide_count(self) -> int:
        # One slide per question (up to 5 for brevity)
        summaries = self.data.get('llm_summaries', {}).get('question_summaries', [])
        return min(len(summaries), 5) + 1  # +1 for overview slide

    def _get_summaries(self) -> list:
        """Get question summaries from LLM data."""
        return self.data.get('llm_summaries', {}).get('question_summaries', [])

    def generate_pptx_slides(self, prs: Presentation) -> Presentation:
        summaries = self._get_summaries()

        if not summaries:
            slide = self.add_content_slide(prs, "AI Insights")
            self.add_text_box(
                slide, 0.5, 2.0, 12.0, 2.0,
                "AI insights not available.\n\nRun llm_batch_summarizer.py to generate AI-powered analysis.",
                font_size=16, color='neutral'
            )
            return prs

        # Overview slide
        overview = self.add_content_slide(prs, "AI Insights: Question Analysis")
        self.add_text_box(
            overview, 0.5, 1.3, 12.0, 1.0,
            f"Claude Opus 4.5 analyzed {len(summaries)} open-ended questions.\n"
            "The following slides show key insights per question.",
            font_size=14, color='text'
        )

        # List questions analyzed
        y_pos = 2.5
        for i, s in enumerate(summaries[:8]):
            q_short = s.get('question', '')[:60]
            if len(s.get('question', '')) > 60:
                q_short += '...'
            self.add_text_box(
                overview, 0.5, y_pos, 12.0, 0.4,
                f"  {i+1}. {q_short}",
                font_size=11, color='text'
            )
            y_pos += 0.5

        # Per-question slides (top 5)
        for summary in summaries[:5]:
            self._add_question_slide(prs, summary)

        return prs

    def _add_question_slide(self, prs: Presentation, summary: dict):
        """Add a detailed slide for one question."""
        question = summary.get('question', 'Unknown Question')
        q_short = question[:50] + '...' if len(question) > 50 else question

        slide = self.add_content_slide(prs, f"AI Analysis: {q_short}")

        # Executive summary
        exec_summary = summary.get('executive_summary', 'N/A')
        self.add_text_box(
            slide, 0.5, 1.3, 7.5, 2.0,
            exec_summary[:300] + ('...' if len(exec_summary) > 300 else ''),
            font_size=11, color='text'
        )

        # Key themes (right column)
        themes = summary.get('themes', [])
        self.add_text_box(
            slide, 8.2, 1.3, 4.5, 0.4,
            "Key Themes:", font_size=12, bold=True, color='primary'
        )

        y_pos = 1.8
        for theme in themes[:4]:
            theme_name = theme.get('theme', 'Theme')
            freq = theme.get('frequency', '')
            self.add_text_box(
                slide, 8.2, y_pos, 4.5, 0.6,
                f"  {theme_name} ({freq})",
                font_size=10, color='secondary'
            )
            y_pos += 0.5

        # Representative quotes (bottom)
        quotes = summary.get('representative_quotes', [])
        if quotes:
            self.add_text_box(
                slide, 0.5, 4.0, 12.0, 0.4,
                "Representative Quotes:", font_size=12, bold=True, color='primary'
            )

            y_pos = 4.5
            for quote in quotes[:2]:
                self.add_text_box(
                    slide, 0.5, y_pos, 12.0, 0.8,
                    f'"{quote[:100]}{"..." if len(quote) > 100 else ""}"',
                    font_size=10, color='neutral'
                )
                y_pos += 0.9

        # Sentiment indicator
        sentiment = summary.get('sentiment_analysis', {}).get('overall', 'Neutral')
        sentiment_color = 'positive' if sentiment == 'Positive' else 'negative' if sentiment == 'Negative' else 'neutral'
        self.add_text_box(
            slide, 0.5, 6.5, 4.0, 0.4,
            f"Sentiment: {sentiment}",
            font_size=11, bold=True, color=sentiment_color
        )

    def generate_pdf_content(self, pdf: FPDF) -> FPDF:
        summaries = self._get_summaries()

        if not summaries:
            self.pdf_add_content_page(pdf, "AI Insights")
            pdf.set_font('Helvetica', 'I', 14)
            pdf.multi_cell(0, 8, "AI insights not available.\n\nRun llm_batch_summarizer.py to generate.")
            return pdf

        # Overview page
        self.pdf_add_content_page(pdf, "AI Insights: Question Analysis")
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(0, 6, f"Claude Opus 4.5 analyzed {len(summaries)} open-ended questions.")
        pdf.ln(5)

        for i, s in enumerate(summaries[:8]):
            q_short = s.get('question', '')[:70]
            pdf.cell(0, 6, f"{i+1}. {q_short}{'...' if len(s.get('question', '')) > 70 else ''}", new_x='LMARGIN', new_y='NEXT')

        # Per-question pages (top 5)
        for summary in summaries[:5]:
            self._add_pdf_question(pdf, summary)

        return pdf

    def _add_pdf_question(self, pdf: FPDF, summary: dict):
        """Add a question analysis page to PDF."""
        question = summary.get('question', 'Unknown')
        q_short = question[:60] + '...' if len(question) > 60 else question

        self.pdf_add_content_page(pdf, f"AI: {q_short}")

        # Executive summary
        exec_summary = summary.get('executive_summary', 'N/A')
        pdf.set_font('Helvetica', '', 10)
        pdf.multi_cell(0, 5, exec_summary[:400])
        pdf.ln(5)

        # Themes
        themes = summary.get('themes', [])
        if themes:
            pdf.set_font('Helvetica', 'B', 11)
            pdf.set_text_color(*self.pdf_colors['primary'])
            pdf.cell(0, 7, "Key Themes:", new_x='LMARGIN', new_y='NEXT')

            pdf.set_font('Helvetica', '', 10)
            pdf.set_text_color(*self.pdf_colors['text'])
            for theme in themes[:4]:
                pdf.cell(5, 6, chr(149))
                pdf.cell(0, 6, f"{theme.get('theme', '')} ({theme.get('frequency', '')})", new_x='LMARGIN', new_y='NEXT')

        # Quotes
        quotes = summary.get('representative_quotes', [])
        if quotes:
            pdf.ln(3)
            pdf.set_font('Helvetica', 'B', 11)
            pdf.set_text_color(*self.pdf_colors['primary'])
            pdf.cell(0, 7, "Representative Quotes:", new_x='LMARGIN', new_y='NEXT')

            pdf.set_font('Helvetica', 'I', 9)
            pdf.set_text_color(*self.pdf_colors['neutral'])
            for quote in quotes[:2]:
                pdf.multi_cell(0, 5, f'"{quote[:120]}{"..." if len(quote) > 120 else ""}"')

        pdf.set_text_color(*self.pdf_colors['text'])
