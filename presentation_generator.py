"""
Presentation Generator - Core Orchestrator

Generates PowerPoint or PDF presentations from survey analysis data.
Allows users to select which sections to include.
"""

import os
import json
from io import BytesIO
from datetime import datetime
from typing import List, Dict, Optional, Any

import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from fpdf import FPDF

# Import section generators
from presentation_sections import (
    TitleSlideSection,
    ExecutiveSummarySection,
    SurveyOverviewSection,
    SentimentAnalysisSection,
    PrioritiesSection,
    RisksSection,
    CrossQuestionSection,
    ActionPlanSection,
    QuickWinsSection,
    MultipleChoiceSection,
    AIInsightsSection,
    AppendixSection,
)


# Color scheme matching the dashboard
COLOR_SCHEME = {
    'primary': RGBColor(0x1E, 0x3A, 0x5F),      # Dark blue
    'secondary': RGBColor(0x3D, 0x5A, 0x80),    # Medium blue
    'accent': RGBColor(0xE0, 0x7A, 0x5F),       # Coral
    'positive': RGBColor(0x2E, 0x7D, 0x32),     # Green
    'negative': RGBColor(0xC6, 0x28, 0x28),     # Red
    'neutral': RGBColor(0x75, 0x75, 0x75),      # Gray
    'background': RGBColor(0xF5, 0xF5, 0xF5),   # Light gray
    'text': RGBColor(0x21, 0x21, 0x21),         # Dark gray
    'white': RGBColor(0xFF, 0xFF, 0xFF),        # White
}

# Section registry - maps section names to classes
SECTION_REGISTRY = {
    'Title Slide': TitleSlideSection,
    'Executive Summary': ExecutiveSummarySection,
    'Survey Overview': SurveyOverviewSection,
    'Sentiment Analysis': SentimentAnalysisSection,
    'Top 5 Priorities': PrioritiesSection,
    'Critical Risks': RisksSection,
    'Cross-Question Insights': CrossQuestionSection,
    'Action Plan': ActionPlanSection,
    'Quick Wins': QuickWinsSection,
    'Multiple Choice Results': MultipleChoiceSection,
    'AI Insights (Full)': AIInsightsSection,
    'Appendix': AppendixSection,
}

# Sections that require LLM summaries
LLM_REQUIRED_SECTIONS = {
    'Executive Summary',
    'Top 5 Priorities',
    'Critical Risks',
    'Cross-Question Insights',
    'Action Plan',
    'AI Insights (Full)',
}


class PresentationGenerator:
    """
    Main orchestrator for generating presentations from survey analysis.

    Usage:
        generator = PresentationGenerator(output_format='pptx')
        generator.load_data_sources()
        generator.add_section('Title Slide', config={'title': 'Survey Analysis'})
        generator.add_section('Executive Summary')
        generator.add_section('Top 5 Priorities')
        presentation_bytes = generator.generate()
    """

    def __init__(self, output_format: str = 'pptx'):
        """
        Initialize the presentation generator.

        Args:
            output_format: 'pptx' for PowerPoint, 'pdf' for PDF
        """
        self.output_format = output_format.lower()
        self.sections: List[Dict[str, Any]] = []
        self.data_sources: Dict[str, Any] = {}
        self._data_loaded = False

    def load_data_sources(self,
                          csv_path: str = 'raw-data.csv',
                          llm_summaries_path: str = 'llm_summaries.json') -> Dict[str, bool]:
        """
        Load all available data sources.

        Returns:
            Dict indicating which sources were loaded successfully
        """
        results = {
            'csv': False,
            'llm_summaries': False,
        }

        # Load raw survey data
        if os.path.exists(csv_path):
            try:
                df = pd.read_csv(csv_path)
                # Normalize column names
                df.columns = [col.strip() for col in df.columns]
                if 'Responses' in df.columns:
                    df = df.rename(columns={'Responses': 'Response'})

                # Clean data
                df = df.dropna(subset=['Response'])
                df = df[df['Response'].astype(str).str.strip() != '']
                df = df[df['Response'].astype(str).str.lower() != 'nan']

                self.data_sources['raw_data'] = df
                self.data_sources['questions'] = df['Question'].unique().tolist()
                results['csv'] = True
            except Exception as e:
                print(f"Error loading CSV: {e}")

        # Load LLM summaries if available
        if os.path.exists(llm_summaries_path):
            try:
                with open(llm_summaries_path, 'r', encoding='utf-8') as f:
                    self.data_sources['llm_summaries'] = json.load(f)
                results['llm_summaries'] = True
            except Exception as e:
                print(f"Error loading LLM summaries: {e}")

        self._data_loaded = True
        return results

    def get_available_sections(self) -> List[Dict[str, Any]]:
        """
        Get list of available sections with their requirements.

        Returns:
            List of dicts with section info and availability
        """
        if not self._data_loaded:
            self.load_data_sources()

        has_llm = 'llm_summaries' in self.data_sources
        has_csv = 'raw_data' in self.data_sources

        sections = []
        for name in SECTION_REGISTRY.keys():
            requires_llm = name in LLM_REQUIRED_SECTIONS
            available = True
            reason = None

            if requires_llm and not has_llm:
                available = False
                reason = "Requires LLM summaries (run llm_batch_summarizer.py first)"
            elif not has_csv and name not in LLM_REQUIRED_SECTIONS:
                if name not in ['Title Slide']:
                    available = False
                    reason = "Requires raw survey data (raw-data.csv)"

            sections.append({
                'name': name,
                'available': available,
                'requires_llm': requires_llm,
                'reason': reason,
            })

        return sections

    def add_section(self, section_name: str, config: Optional[Dict] = None) -> bool:
        """
        Add a section to the presentation.

        Args:
            section_name: Name of the section (must be in SECTION_REGISTRY)
            config: Optional configuration for the section

        Returns:
            True if section was added, False if not available
        """
        if section_name not in SECTION_REGISTRY:
            print(f"Unknown section: {section_name}")
            return False

        # Check if section can be generated
        available_sections = self.get_available_sections()
        section_info = next((s for s in available_sections if s['name'] == section_name), None)

        if section_info and not section_info['available']:
            print(f"Section '{section_name}' not available: {section_info['reason']}")
            return False

        self.sections.append({
            'name': section_name,
            'config': config or {},
        })
        return True

    def clear_sections(self):
        """Remove all sections from the presentation."""
        self.sections = []

    def get_estimated_slides(self) -> int:
        """Estimate the number of slides that will be generated."""
        # Rough estimates per section
        estimates = {
            'Title Slide': 1,
            'Executive Summary': 1,
            'Survey Overview': 1,
            'Sentiment Analysis': 2,
            'Top 5 Priorities': 2,
            'Critical Risks': 1,
            'Cross-Question Insights': 1,
            'Action Plan': 1,
            'Quick Wins': 2,
            'Multiple Choice Results': 2,
            'AI Insights (Full)': 3,
            'Appendix': 1,
        }
        return sum(estimates.get(s['name'], 1) for s in self.sections)

    def generate(self) -> bytes:
        """
        Generate the presentation.

        Returns:
            Presentation as bytes (for download)
        """
        if not self._data_loaded:
            self.load_data_sources()

        if self.output_format == 'pptx':
            return self._generate_pptx()
        elif self.output_format == 'pdf':
            return self._generate_pdf()
        else:
            raise ValueError(f"Unsupported format: {self.output_format}")

    def _generate_pptx(self) -> bytes:
        """Generate PowerPoint presentation."""
        prs = Presentation()

        # Set slide dimensions (16:9 widescreen)
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)

        # Generate each section
        for section_info in self.sections:
            section_class = SECTION_REGISTRY[section_info['name']]
            section = section_class(self.data_sources, section_info['config'])
            prs = section.generate_pptx_slides(prs)

        # Save to bytes
        buffer = BytesIO()
        prs.save(buffer)
        buffer.seek(0)
        return buffer.getvalue()

    def _generate_pdf(self) -> bytes:
        """Generate PDF presentation."""
        pdf = FPDF(orientation='L', unit='mm', format='A4')
        pdf.set_auto_page_break(auto=True, margin=15)

        # Generate each section
        for section_info in self.sections:
            section_class = SECTION_REGISTRY[section_info['name']]
            section = section_class(self.data_sources, section_info['config'])
            pdf = section.generate_pdf_content(pdf)

        # Return as bytes
        return bytes(pdf.output())

    def export_to_file(self, filepath: str):
        """
        Save presentation to a file.

        Args:
            filepath: Output file path
        """
        content = self.generate()
        with open(filepath, 'wb') as f:
            f.write(content)
        print(f"Presentation saved to: {filepath}")


def get_default_filename(format: str = 'pptx') -> str:
    """Generate a default filename with timestamp."""
    timestamp = datetime.now().strftime('%Y-%m-%d_%H%M')
    return f"survey_presentation_{timestamp}.{format}"


# Quick test
if __name__ == '__main__':
    print("Presentation Generator - Test Mode")

    generator = PresentationGenerator(output_format='pptx')
    results = generator.load_data_sources()
    print(f"Data sources loaded: {results}")

    print("\nAvailable sections:")
    for section in generator.get_available_sections():
        status = "Available" if section['available'] else f"Unavailable ({section['reason']})"
        print(f"  - {section['name']}: {status}")

    print(f"\nTo generate a presentation, add sections and call generate()")
