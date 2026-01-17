"""
Chart Generator - Creates matplotlib charts for presentations.

Generates professional charts as PNG images that can be embedded
into PowerPoint or PDF presentations.
"""

import os
import tempfile
from typing import List, Tuple, Dict, Optional
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server use
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np


# Color scheme matching the presentation theme
CHART_COLORS = {
    'primary': '#1E3A5F',      # Dark blue
    'secondary': '#3D5A80',    # Medium blue
    'accent': '#E07A5F',       # Coral
    'positive': '#2E7D32',     # Green
    'negative': '#C62828',     # Red
    'neutral': '#757575',      # Gray
    'background': '#F5F5F5',   # Light gray
    'text': '#212121',         # Dark gray
    'white': '#FFFFFF',        # White
    'light_blue': '#90CAF9',   # Light blue for gradients
    'light_green': '#A5D6A7',  # Light green
    'light_red': '#EF9A9A',    # Light red
}

# Gradient color palettes for bar charts
BAR_GRADIENTS = {
    'blue': ['#1E3A5F', '#3D5A80', '#5C7A99', '#7B9AB3', '#9ABACC', '#B9DAE6'],
    'sentiment': ['#2E7D32', '#757575', '#C62828'],  # Green, Gray, Red
}


class ChartGenerator:
    """
    Generate matplotlib charts for presentation slides.

    Usage:
        charts = ChartGenerator()
        path = charts.horizontal_bar_chart(data, "Title")
        # Use path to embed image in slide
        charts.cleanup()  # Remove temp files when done
    """

    def __init__(self):
        """Initialize the chart generator."""
        self.temp_dir = tempfile.mkdtemp(prefix='pres_charts_')
        self.temp_files: List[str] = []
        self.colors = CHART_COLORS

        # Set matplotlib defaults for consistent styling
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
            'font.size': 10,
            'axes.titlesize': 14,
            'axes.labelsize': 11,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'figure.facecolor': 'white',
            'axes.facecolor': 'white',
            'axes.edgecolor': '#CCCCCC',
            'axes.grid': False,
        })

    def _save_chart(self, fig, name: str = 'chart') -> str:
        """Save matplotlib figure to temp PNG and return path."""
        filepath = os.path.join(self.temp_dir, f'{name}_{len(self.temp_files)}.png')
        fig.savefig(filepath, dpi=150, bbox_inches='tight',
                    facecolor='white', edgecolor='none')
        plt.close(fig)
        self.temp_files.append(filepath)
        return filepath

    def cleanup(self):
        """Remove all temporary chart files."""
        for filepath in self.temp_files:
            try:
                os.remove(filepath)
            except OSError:
                pass
        try:
            os.rmdir(self.temp_dir)
        except OSError:
            pass
        self.temp_files = []

    # =====================================================
    # HORIZONTAL BAR CHART
    # =====================================================

    def horizontal_bar_chart(
        self,
        data: List[Tuple[str, int]],
        title: str = '',
        color: str = 'primary',
        show_values: bool = True,
        max_items: int = 10,
        figsize: Tuple[float, float] = (8, 5)
    ) -> str:
        """
        Create a horizontal bar chart.

        Args:
            data: List of (label, value) tuples
            title: Chart title
            color: Color key from CHART_COLORS or hex color
            show_values: Show value labels at end of bars
            max_items: Maximum number of bars to show
            figsize: Figure size in inches

        Returns:
            Path to PNG image file
        """
        # Limit data and sort by value
        data = sorted(data, key=lambda x: x[1], reverse=True)[:max_items]
        labels = [d[0] for d in data]
        values = [d[1] for d in data]

        # Truncate long labels
        labels = [l[:35] + '...' if len(l) > 35 else l for l in labels]

        # Reverse for horizontal bar (top to bottom)
        labels = labels[::-1]
        values = values[::-1]

        # Get bar color
        bar_color = self.colors.get(color, color)

        # Create figure
        fig, ax = plt.subplots(figsize=figsize)

        # Create gradient colors for bars
        n_bars = len(values)
        if n_bars > 1:
            gradient = plt.cm.Blues(np.linspace(0.4, 0.9, n_bars))
        else:
            gradient = [bar_color]

        # Draw bars
        y_pos = np.arange(len(labels))
        bars = ax.barh(y_pos, values, color=gradient, edgecolor='none', height=0.7)

        # Add value labels
        if show_values:
            max_val = max(values) if values else 1
            for i, (bar, val) in enumerate(zip(bars, values)):
                ax.text(val + max_val * 0.02, bar.get_y() + bar.get_height() / 2,
                        str(val), va='center', ha='left',
                        fontsize=10, fontweight='bold', color=self.colors['text'])

        # Styling
        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels)
        ax.set_xlabel('')
        ax.set_xlim(0, max(values) * 1.15 if values else 1)

        # Remove spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.tick_params(bottom=False, left=False)

        if title:
            ax.set_title(title, fontsize=14, fontweight='bold',
                        color=self.colors['primary'], pad=15)

        plt.tight_layout()
        return self._save_chart(fig, 'hbar')

    # =====================================================
    # DONUT CHART
    # =====================================================

    def donut_chart(
        self,
        values: List[int],
        labels: List[str],
        colors: Optional[List[str]] = None,
        center_text: str = '',
        title: str = '',
        figsize: Tuple[float, float] = (5, 5)
    ) -> str:
        """
        Create a donut (ring) chart.

        Args:
            values: List of numeric values
            labels: List of labels for each slice
            colors: List of colors (defaults to sentiment colors)
            center_text: Text to show in center of donut
            title: Chart title
            figsize: Figure size

        Returns:
            Path to PNG image file
        """
        if colors is None:
            colors = [self.colors['positive'], self.colors['neutral'], self.colors['negative']]

        fig, ax = plt.subplots(figsize=figsize)

        # Create donut
        wedges, texts, autotexts = ax.pie(
            values,
            labels=None,
            colors=colors[:len(values)],
            autopct='%1.0f%%',
            startangle=90,
            pctdistance=0.75,
            wedgeprops={'width': 0.5, 'edgecolor': 'white', 'linewidth': 2}
        )

        # Style percentage labels
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(11)
            autotext.set_fontweight('bold')

        # Center text
        if center_text:
            ax.text(0, 0, center_text, ha='center', va='center',
                    fontsize=16, fontweight='bold', color=self.colors['primary'])

        # Legend
        ax.legend(wedges, labels, loc='center left', bbox_to_anchor=(1, 0.5),
                  frameon=False, fontsize=10)

        if title:
            ax.set_title(title, fontsize=14, fontweight='bold',
                        color=self.colors['primary'], pad=15)

        ax.axis('equal')
        plt.tight_layout()
        return self._save_chart(fig, 'donut')

    # =====================================================
    # METRIC CARDS
    # =====================================================

    def metric_cards(
        self,
        metrics: List[Tuple[str, str, str]],
        figsize: Tuple[float, float] = (10, 2)
    ) -> str:
        """
        Create a row of KPI metric cards.

        Args:
            metrics: List of (value, label, color_key) tuples
                     color_key can be 'primary', 'positive', 'negative', etc.
            figsize: Figure size

        Returns:
            Path to PNG image file
        """
        n_cards = len(metrics)
        fig, axes = plt.subplots(1, n_cards, figsize=figsize)

        if n_cards == 1:
            axes = [axes]

        for ax, (value, label, color_key) in zip(axes, metrics):
            color = self.colors.get(color_key, self.colors['primary'])

            # Remove axes
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')

            # Draw card background
            card = FancyBboxPatch(
                (0.05, 0.05), 0.9, 0.9,
                boxstyle="round,pad=0.05,rounding_size=0.1",
                facecolor=color,
                edgecolor='none',
                alpha=0.9
            )
            ax.add_patch(card)

            # Value (large)
            ax.text(0.5, 0.55, str(value), ha='center', va='center',
                    fontsize=28, fontweight='bold', color='white')

            # Label (smaller)
            ax.text(0.5, 0.25, label, ha='center', va='center',
                    fontsize=10, color='white', alpha=0.9)

        plt.tight_layout()
        return self._save_chart(fig, 'metrics')

    # =====================================================
    # DUAL BAR CHART (Stop vs Start)
    # =====================================================

    def dual_bar_chart(
        self,
        left_data: List[Tuple[str, int]],
        right_data: List[Tuple[str, int]],
        left_title: str = 'Left',
        right_title: str = 'Right',
        left_color: str = 'negative',
        right_color: str = 'positive',
        max_items: int = 6,
        figsize: Tuple[float, float] = (12, 5)
    ) -> str:
        """
        Create side-by-side horizontal bar charts (e.g., Stop vs Start).

        Args:
            left_data: Data for left chart
            right_data: Data for right chart
            left_title: Title for left chart
            right_title: Title for right chart
            left_color: Color for left bars
            right_color: Color for right bars
            max_items: Max items per side
            figsize: Figure size

        Returns:
            Path to PNG image file
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)

        # Process data
        left_data = sorted(left_data, key=lambda x: x[1], reverse=True)[:max_items]
        right_data = sorted(right_data, key=lambda x: x[1], reverse=True)[:max_items]

        for ax, data, title, color in [
            (ax1, left_data, left_title, left_color),
            (ax2, right_data, right_title, right_color)
        ]:
            if not data:
                ax.text(0.5, 0.5, 'No data', ha='center', va='center')
                ax.axis('off')
                continue

            labels = [d[0][:25] + '...' if len(d[0]) > 25 else d[0] for d in data]
            values = [d[1] for d in data]

            labels = labels[::-1]
            values = values[::-1]

            y_pos = np.arange(len(labels))
            bar_color = self.colors.get(color, color)

            bars = ax.barh(y_pos, values, color=bar_color, height=0.6, alpha=0.85)

            # Value labels
            max_val = max(values) if values else 1
            for bar, val in zip(bars, values):
                ax.text(val + max_val * 0.03, bar.get_y() + bar.get_height() / 2,
                        str(val), va='center', fontsize=9, fontweight='bold')

            ax.set_yticks(y_pos)
            ax.set_yticklabels(labels, fontsize=9)
            ax.set_xlim(0, max_val * 1.2)
            ax.set_title(title, fontsize=12, fontweight='bold', color=bar_color)

            # Clean up spines
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.tick_params(bottom=False, left=False)

        plt.tight_layout()
        return self._save_chart(fig, 'dual_bar')

    # =====================================================
    # TIMELINE
    # =====================================================

    def timeline(
        self,
        phases: Dict[str, List[str]],
        phase_colors: Optional[Dict[str, str]] = None,
        figsize: Tuple[float, float] = (12, 4)
    ) -> str:
        """
        Create a horizontal timeline visualization.

        Args:
            phases: Dict mapping phase names to list of action items
                    e.g., {'0-30 days': ['Action 1', 'Action 2'], ...}
            phase_colors: Optional dict mapping phase names to colors
            figsize: Figure size

        Returns:
            Path to PNG image file
        """
        if phase_colors is None:
            phase_colors = {
                '0-30 days': self.colors['positive'],
                '30-90 days': self.colors['accent'],
                '90+ days': self.colors['secondary'],
            }

        fig, ax = plt.subplots(figsize=figsize)
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 5)
        ax.axis('off')

        n_phases = len(phases)
        phase_width = 9 / n_phases

        for i, (phase_name, actions) in enumerate(phases.items()):
            x_start = 0.5 + i * phase_width
            color = phase_colors.get(phase_name, self.colors['secondary'])

            # Phase header
            header = FancyBboxPatch(
                (x_start, 4), phase_width - 0.3, 0.7,
                boxstyle="round,pad=0.02,rounding_size=0.1",
                facecolor=color,
                edgecolor='none'
            )
            ax.add_patch(header)
            ax.text(x_start + (phase_width - 0.3) / 2, 4.35, phase_name,
                    ha='center', va='center', fontsize=10, fontweight='bold', color='white')

            # Vertical line
            ax.plot([x_start + (phase_width - 0.3) / 2] * 2, [0.5, 3.8],
                    color=color, linewidth=2, alpha=0.5)

            # Action items
            for j, action in enumerate(actions[:3]):  # Max 3 per phase
                y_pos = 3.2 - j * 1.0
                action_box = FancyBboxPatch(
                    (x_start, y_pos), phase_width - 0.4, 0.8,
                    boxstyle="round,pad=0.02,rounding_size=0.05",
                    facecolor='white',
                    edgecolor=color,
                    linewidth=1.5
                )
                ax.add_patch(action_box)

                # Truncate long text
                action_text = action[:30] + '...' if len(action) > 30 else action
                ax.text(x_start + (phase_width - 0.4) / 2, y_pos + 0.4,
                        action_text, ha='center', va='center',
                        fontsize=8, color=self.colors['text'], wrap=True)

        # Arrow at bottom
        ax.annotate('', xy=(9.5, 0.3), xytext=(0.5, 0.3),
                    arrowprops=dict(arrowstyle='->', color=self.colors['neutral'], lw=2))
        ax.text(5, 0.05, 'Timeline', ha='center', fontsize=9, color=self.colors['neutral'])

        plt.tight_layout()
        return self._save_chart(fig, 'timeline')

    # =====================================================
    # SENTIMENT BAR (per question)
    # =====================================================

    def sentiment_bars(
        self,
        data: List[Tuple[str, str]],
        figsize: Tuple[float, float] = (6, 4)
    ) -> str:
        """
        Create stacked sentiment bars showing per-question sentiment.

        Args:
            data: List of (question_label, sentiment) tuples
                  sentiment should be 'Positive', 'Neutral', or 'Negative'
            figsize: Figure size

        Returns:
            Path to PNG image file
        """
        sentiment_colors = {
            'Positive': self.colors['positive'],
            'Neutral': self.colors['neutral'],
            'Negative': self.colors['negative'],
        }

        fig, ax = plt.subplots(figsize=figsize)

        y_pos = np.arange(len(data))
        labels = [d[0][:20] + '...' if len(d[0]) > 20 else d[0] for d in data]
        sentiments = [d[1] for d in data]

        colors = [sentiment_colors.get(s, self.colors['neutral']) for s in sentiments]

        # Full bars (background)
        ax.barh(y_pos, [1] * len(data), color=self.colors['background'], height=0.6)

        # Sentiment indicators
        for i, (label, sentiment) in enumerate(data):
            color = sentiment_colors.get(sentiment, self.colors['neutral'])
            # Draw indicator circle
            ax.scatter([0.95], [i], s=200, c=[color], marker='o', zorder=5)

        ax.set_yticks(y_pos)
        ax.set_yticklabels(labels)
        ax.set_xlim(0, 1.1)
        ax.set_xticks([])

        # Remove spines
        for spine in ax.spines.values():
            spine.set_visible(False)
        ax.tick_params(left=False)

        # Legend
        legend_elements = [
            mpatches.Patch(facecolor=self.colors['positive'], label='Positive'),
            mpatches.Patch(facecolor=self.colors['neutral'], label='Neutral'),
            mpatches.Patch(facecolor=self.colors['negative'], label='Negative'),
        ]
        ax.legend(handles=legend_elements, loc='lower right', frameon=False, fontsize=8)

        plt.tight_layout()
        return self._save_chart(fig, 'sentiment_bars')

    # =====================================================
    # PRIORITY RANKING
    # =====================================================

    def priority_ranking(
        self,
        priorities: List[Tuple[int, str, str]],
        figsize: Tuple[float, float] = (6, 5)
    ) -> str:
        """
        Create a visual priority ranking with importance bars.

        Args:
            priorities: List of (rank, priority_name, importance) tuples
                       importance can be 'HIGH', 'MEDIUM', 'LOW'
            figsize: Figure size

        Returns:
            Path to PNG image file
        """
        importance_widths = {'HIGH': 0.9, 'MEDIUM': 0.6, 'LOW': 0.3}
        importance_colors = {
            'HIGH': self.colors['accent'],
            'MEDIUM': self.colors['secondary'],
            'LOW': self.colors['neutral']
        }

        fig, ax = plt.subplots(figsize=figsize)

        for i, (rank, name, importance) in enumerate(priorities[:5]):
            y = 4 - i
            width = importance_widths.get(importance.upper(), 0.5)
            color = importance_colors.get(importance.upper(), self.colors['secondary'])

            # Rank number
            circle = plt.Circle((0.3, y), 0.25, color=self.colors['accent'], zorder=5)
            ax.add_patch(circle)
            ax.text(0.3, y, str(rank), ha='center', va='center',
                    fontsize=12, fontweight='bold', color='white', zorder=6)

            # Priority name
            name_short = name[:30] + '...' if len(name) > 30 else name
            ax.text(0.7, y + 0.15, name_short, ha='left', va='center',
                    fontsize=10, fontweight='bold', color=self.colors['text'])

            # Importance bar
            bar = FancyBboxPatch(
                (0.7, y - 0.25), width * 4, 0.3,
                boxstyle="round,pad=0.01,rounding_size=0.05",
                facecolor=color,
                alpha=0.8
            )
            ax.add_patch(bar)

            # Importance label
            ax.text(0.7 + width * 4 + 0.1, y - 0.1, importance.upper(),
                    ha='left', va='center', fontsize=8, color=color, fontweight='bold')

        ax.set_xlim(0, 6)
        ax.set_ylim(-0.5, 5)
        ax.axis('off')

        plt.tight_layout()
        return self._save_chart(fig, 'priority')


# Quick test
if __name__ == '__main__':
    print("Testing ChartGenerator...")

    charts = ChartGenerator()

    # Test horizontal bar chart
    data = [
        ("Team Culture", 127),
        ("Future Mission", 115),
        ("AI Tools", 98),
        ("Challenges", 89),
        ("Human Value", 76),
    ]
    path = charts.horizontal_bar_chart(data, "Response Distribution")
    print(f"Horizontal bar chart: {path}")

    # Test donut chart
    path = charts.donut_chart([45, 30, 25], ["Positive", "Neutral", "Negative"], center_text="Sentiment")
    print(f"Donut chart: {path}")

    # Test metric cards
    metrics = [
        ("1,434", "Responses", "primary"),
        ("45%", "Positive", "positive"),
        ("5", "Priorities", "accent"),
    ]
    path = charts.metric_cards(metrics)
    print(f"Metric cards: {path}")

    # Test dual bar chart
    stop_data = [("POC overload", 23), ("Manual work", 18), ("Silos", 12)]
    start_data = [("Collaboration", 28), ("AI tools", 21), ("Training", 15)]
    path = charts.dual_bar_chart(stop_data, start_data, "STOP DOING", "START DOING")
    print(f"Dual bar chart: {path}")

    # Test timeline
    phases = {
        '0-30 days': ['Quick Win 1', 'Quick Win 2'],
        '30-90 days': ['Process Reform', 'Training Program'],
        '90+ days': ['Platform Build', 'Scale Program'],
    }
    path = charts.timeline(phases)
    print(f"Timeline: {path}")

    print(f"\nGenerated {len(charts.temp_files)} chart images")
    print("Cleaning up...")
    charts.cleanup()
    print("Done!")
