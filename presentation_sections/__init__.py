"""
Presentation Sections Module

Each section generates content for PowerPoint and PDF presentations.
"""

from .base import BaseSection, COLORS, PDF_COLORS
from .title_slide import TitleSlideSection
from .executive_summary import ExecutiveSummarySection
from .survey_overview import SurveyOverviewSection
from .sentiment_analysis import SentimentAnalysisSection
from .priorities import PrioritiesSection
from .risks import RisksSection
from .cross_question import CrossQuestionSection
from .action_plan import ActionPlanSection
from .quick_wins import QuickWinsSection
from .multiple_choice import MultipleChoiceSection
from .ai_insights import AIInsightsSection
from .appendix import AppendixSection

__all__ = [
    'BaseSection',
    'COLORS',
    'PDF_COLORS',
    'TitleSlideSection',
    'ExecutiveSummarySection',
    'SurveyOverviewSection',
    'SentimentAnalysisSection',
    'PrioritiesSection',
    'RisksSection',
    'CrossQuestionSection',
    'ActionPlanSection',
    'QuickWinsSection',
    'MultipleChoiceSection',
    'AIInsightsSection',
    'AppendixSection',
]
