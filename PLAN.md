# Presentation Generator Enhancement Plan

## Problem Statement

Current presentations are **too text-heavy** for senior management. Need to transform from ~60% text to ~80% visual with:
- Charts and graphs instead of bullet lists
- Executive-friendly layouts with key metrics highlighted
- Visual data storytelling rather than paragraph dumps

## Current State Analysis

| Section | Current State | Visual Coverage |
|---------|--------------|-----------------|
| Survey Overview | Text list of questions | 0% |
| Executive Summary | 3 paragraphs of text | 0% |
| Sentiment Analysis | Three colored boxes | 60% |
| Quick Wins | Text list with counts | 10% |
| Action Plan | Three-column text | 20% |
| Priorities | Numbered text items | 30% |
| Risks | Three-column text | 10% |
| Cross-Question | Text columns | 0% |
| AI Insights | Text-heavy analysis | 0% |
| Multiple Choice | Horizontal bars | 70% ✓ |

## Enhancement Strategy

### Approach: Matplotlib Chart Generation

Add a `ChartGenerator` utility class that:
1. Creates professional charts using matplotlib
2. Saves charts as temporary PNG images
3. Sections embed these images into slides
4. Clean, consistent styling across all charts

**Why matplotlib?** Already installed (in requirements.txt), proven library, works with both PowerPoint and PDF.

---

## Implementation Plan

### Phase 1: Chart Infrastructure

**1.1 Create `presentation_sections/charts.py`**

```python
class ChartGenerator:
    """Generate matplotlib charts for presentation slides."""

    def horizontal_bar_chart(data, title, colors) -> str:
        """Returns path to PNG image"""

    def donut_chart(values, labels, colors) -> str:
        """Sentiment/distribution pie chart"""

    def metric_card(value, label, trend) -> str:
        """Executive KPI card with large number"""

    def heatmap(matrix, x_labels, y_labels) -> str:
        """Risk matrix, correlation grid"""

    def timeline(items, timeframes) -> str:
        """Action plan timeline visualization"""
```

**1.2 Update `base.py`**

Add helper method:
```python
def add_chart_image(self, slide, image_path, left, top, width, height):
    """Insert chart image into PowerPoint slide"""
```

---

### Phase 2: High-Impact Section Enhancements

#### 2.1 Survey Overview → Response Distribution Chart

**Before:** Text list of questions with response counts
**After:** Horizontal bar chart showing all questions ranked by response volume

```
┌─────────────────────────────────────────────────────────────┐
│  SURVEY OVERVIEW                                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────────────────────────────┐                  │
│   │  [HORIZONTAL BAR CHART]              │    Key Metrics   │
│   │  Q1: Team Culture ████████████ 127   │    ┌──────────┐  │
│   │  Q2: Future Mission ██████████ 115   │    │   1,434  │  │
│   │  Q6: AI Tools ████████ 98            │    │ Responses│  │
│   │  Q12: Challenges ███████ 89          │    └──────────┘  │
│   │  ...                                 │    ┌──────────┐  │
│   └──────────────────────────────────────┘    │    14    │  │
│                                               │ Questions│  │
│                                               └──────────┘  │
└─────────────────────────────────────────────────────────────┘
```

#### 2.2 Sentiment Analysis → Donut Chart + Metrics

**Before:** Three colored boxes with percentages
**After:** Donut chart with sentiment breakdown + per-question heatmap

```
┌─────────────────────────────────────────────────────────────┐
│  SENTIMENT ANALYSIS                                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────────┐      ┌─────────────────────────────┐  │
│   │   [DONUT CHART] │      │  Per-Question Sentiment     │  │
│   │                 │      │  Q1: ████████░░ Positive    │  │
│   │    ████████     │      │  Q2: ██████░░░░ Neutral     │  │
│   │   ██      ██    │      │  Q6: ████░░░░░░ Mixed       │  │
│   │   ██  45% ██    │      │  Q12: ██░░░░░░░ Negative    │  │
│   │   ██      ██    │      │  ...                        │  │
│   │    ████████     │      └─────────────────────────────┘  │
│   │   Positive      │                                       │
│   └─────────────────┘      30% Neutral | 25% Negative       │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 2.3 Quick Wins → Frequency Bar Charts (Stop/Start)

**Before:** Text list with mention counts
**After:** Side-by-side bar charts for Stop vs Start

```
┌─────────────────────────────────────────────────────────────┐
│  QUICK WINS: STOP vs START                                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   🛑 STOP DOING                    🚀 START DOING            │
│   ┌────────────────────┐          ┌────────────────────┐    │
│   │ POC overload ████ 23│          │ Collaboration ████ 28│  │
│   │ Manual work ███ 18  │          │ AI tools ███ 21     │  │
│   │ Silos ██ 12         │          │ Training ██ 15      │  │
│   │ ...                 │          │ ...                 │  │
│   └────────────────────┘          └────────────────────┘    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 2.4 Priorities → Visual Priority Matrix

**Before:** Numbered list with descriptions
**After:** Impact/Effort quadrant matrix + ranked list

```
┌─────────────────────────────────────────────────────────────┐
│  TOP 5 STRATEGIC PRIORITIES                                  │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────────────────┐    ┌──────────────────────┐   │
│   │     PRIORITY MATRIX     │    │  1. AI Enablement    │   │
│   │                         │    │     ██████████ HIGH  │   │
│   │  HIGH  │  ①  │  ②      │    │                      │   │
│   │ IMPACT │     │          │    │  2. Process Reform   │   │
│   │        ├─────┼──────────│    │     ████████ HIGH    │   │
│   │  LOW   │  ④  │  ③ ⑤    │    │                      │   │
│   │        │     │          │    │  3. Skills Training  │   │
│   │        └─────┴──────────│    │     ██████ MEDIUM    │   │
│   │          LOW    HIGH    │    │                      │   │
│   │            EFFORT       │    │  ...                 │   │
│   └─────────────────────────┘    └──────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 2.5 Risks → Risk Heat Map

**Before:** Three-column text layout
**After:** Risk severity matrix with color intensity

```
┌─────────────────────────────────────────────────────────────┐
│  CRITICAL RISKS                                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │           RISK ASSESSMENT MATRIX                     │   │
│   │                                                      │   │
│   │              LOW        MEDIUM       HIGH            │   │
│   │           LIKELIHOOD                                 │   │
│   │  ┌────────┬──────────┬──────────┬──────────┐        │   │
│   │  │ HIGH   │    ▓▓    │   ████   │   ████   │ ← PEOPLE│   │
│   │  │ IMPACT │          │          │   ████   │        │   │
│   │  ├────────┼──────────┼──────────┼──────────┤        │   │
│   │  │ MEDIUM │    ░░    │    ▓▓    │   ████   │← REVENUE│   │
│   │  ├────────┼──────────┼──────────┼──────────┤        │   │
│   │  │ LOW    │    ░░    │    ░░    │    ▓▓    │← COMPET.│   │
│   │  └────────┴──────────┴──────────┴──────────┘        │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                              │
│   Key takeaway: People risk is CRITICAL (high impact/likely) │
└─────────────────────────────────────────────────────────────┘
```

#### 2.6 Action Plan → Timeline Visualization

**Before:** Three-column text layout
**After:** Horizontal timeline with action blocks

```
┌─────────────────────────────────────────────────────────────┐
│  RECOMMENDED ACTION PLAN                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   NOW (0-30 days)    NEXT (30-90 days)    LATER (90+ days)  │
│   ─────────────────────────────────────────────────────────  │
│   │                  │                    │                  │
│   │  ┌──────────┐    │  ┌──────────┐     │  ┌──────────┐   │
│   │  │ Quick    │    │  │ Process  │     │  │ Platform │   │
│   │  │ Win #1   │    │  │ Reform   │     │  │ Build    │   │
│   │  └──────────┘    │  └──────────┘     │  └──────────┘   │
│   │  ┌──────────┐    │  ┌──────────┐     │  ┌──────────┐   │
│   │  │ Quick    │    │  │ Training │     │  │ Scale    │   │
│   │  │ Win #2   │    │  │ Program  │     │  │ Program  │   │
│   │  └──────────┘    │  └──────────┘     │  └──────────┘   │
│   │                  │                    │                  │
│   ▼                  ▼                    ▼                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 2.7 Executive Summary → Key Metrics Dashboard

**Before:** Three paragraphs of text
**After:** Metric cards + condensed key findings

```
┌─────────────────────────────────────────────────────────────┐
│  EXECUTIVE SUMMARY                                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐       │
│   │  1,434  │  │   45%   │  │    5    │  │   HIGH  │       │
│   │Responses│  │Positive │  │Priorities│  │Confidence│      │
│   └─────────┘  └─────────┘  └─────────┘  └─────────┘       │
│                                                              │
│   KEY INSIGHT: Team aspires to "Trusted Advisor" role but   │
│   faces operational barriers. Top 3 themes: AI enablement,  │
│   process simplification, skills development.               │
│                                                              │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  "More collaboration" mentioned 47 times             │   │
│   │  "POC overload" mentioned 23 times                   │   │
│   │  "Training needed" mentioned 31 times                │   │
│   └─────────────────────────────────────────────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

### Phase 3: Cross-Question & AI Insights

#### 3.1 Cross-Question Insights → Relationship Diagram

**Before:** Three text columns
**After:** Visual showing question relationships

```
┌─────────────────────────────────────────────────────────────┐
│  CROSS-QUESTION INSIGHTS                                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ALIGNMENTS          TENSIONS           EMERGING PATTERNS   │
│   ┌──────────┐       ┌──────────┐       ┌──────────┐        │
│   │ Q1 ←→ Q2 │       │ Q2 ⚡ Q12│       │ Q6 → Q7  │        │
│   │ Culture  │       │ Vision vs│       │ AI Gap   │        │
│   │ = Mission│       │ Reality  │       │ Emerging │        │
│   └──────────┘       └──────────┘       └──────────┘        │
│                                                              │
│   ═══════════════════════════════════════════════════════   │
│                                                              │
│   3 alignments found | 3 tensions identified | 3 patterns   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

#### 3.2 AI Insights → Theme Frequency Charts

**Before:** Text-heavy per-question analysis
**After:** Visual theme breakdown with frequency bars

```
┌─────────────────────────────────────────────────────────────┐
│  AI INSIGHTS: Q1 - Team Culture                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   SENTIMENT: ✅ Positive (82% confidence)                    │
│                                                              │
│   TOP THEMES                          REPRESENTATIVE QUOTE   │
│   ┌──────────────────────────┐       ┌─────────────────────┐│
│   │ Collaboration ████████ 38%│       │ "We have a strong  ││
│   │ Innovation ██████ 24%    │       │  culture of helping ││
│   │ Trust ████ 18%           │       │  each other..."     ││
│   │ Expertise ███ 12%        │       │                     ││
│   │ Growth ██ 8%             │       │ - Survey Respondent ││
│   └──────────────────────────┘       └─────────────────────┘│
│                                                              │
│   💡 ACTIONABLE: Leverage collaboration strength for AI      │
│      adoption initiatives.                                   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Technical Implementation Details

### New Files to Create

```
presentation_sections/
├── charts.py          # NEW: ChartGenerator class
└── (existing files)   # MODIFY: Add chart integration
```

### Dependencies

- `matplotlib` - Already in requirements.txt ✓
- `tempfile` - Built-in Python module for temp image storage

### ChartGenerator Class Design

```python
class ChartGenerator:
    def __init__(self):
        self.colors = {...}  # Match presentation color scheme
        self.temp_dir = tempfile.mkdtemp()

    def _save_chart(self, fig) -> str:
        """Save matplotlib figure to temp PNG, return path"""

    def horizontal_bar_chart(self, data: List[Tuple[str, int]],
                             title: str, color: str) -> str:
        """Create horizontal bar chart, return image path"""

    def donut_chart(self, values: List[int], labels: List[str],
                    colors: List[str], center_text: str) -> str:
        """Create donut/pie chart with center label"""

    def metric_cards(self, metrics: List[Tuple[str, str, str]]) -> str:
        """Create row of KPI metric cards"""

    def timeline(self, phases: Dict[str, List[str]]) -> str:
        """Create horizontal timeline visualization"""

    def heatmap(self, matrix: List[List[float]],
                x_labels: List[str], y_labels: List[str]) -> str:
        """Create heat map for risk/correlation matrix"""

    def cleanup(self):
        """Remove all temp images after presentation generation"""
```

### Section Modification Pattern

Each section that needs charts will:

```python
def generate_pptx_slides(self, prs):
    # 1. Initialize chart generator
    charts = ChartGenerator()

    # 2. Prepare data for chart
    data = [("Label1", 100), ("Label2", 80), ...]

    # 3. Generate chart image
    chart_path = charts.horizontal_bar_chart(data, "Title", "primary")

    # 4. Add chart to slide
    self.add_chart_image(slide, chart_path, left=0.5, top=1.5, width=6, height=4)

    # 5. Add supporting text/metrics
    self.add_text_box(slide, ...)

    # 6. Cleanup
    charts.cleanup()
```

---

## Implementation Phases

### Phase 1: Infrastructure (Foundation)
1. Create `charts.py` with ChartGenerator class
2. Add `add_chart_image()` helper to base.py
3. Test with simple bar chart

### Phase 2: High-Impact Sections
4. Enhance Survey Overview with response bar chart
5. Enhance Sentiment Analysis with donut chart
6. Enhance Quick Wins with frequency bars
7. Enhance Executive Summary with metric cards

### Phase 3: Medium-Impact Sections
8. Enhance Priorities with visual indicators
9. Enhance Risks with heat map
10. Enhance Action Plan with timeline

### Phase 4: Polish
11. Enhance Cross-Question with relationship visuals
12. Enhance AI Insights with theme charts
13. Final testing and cleanup

---

## Success Criteria

| Metric | Before | After |
|--------|--------|-------|
| Visual coverage | 60% text | 80% visual |
| Charts per presentation | 1 | 8-10 |
| Executive readability | Low | High |
| Key metrics visibility | Hidden in text | Prominent cards |
| Data storytelling | Paragraphs | Charts + callouts |

---

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Chart generation slow | Cache charts, optimize matplotlib settings |
| Image quality in PPTX | Use high DPI (150+), PNG format |
| PDF size bloat | Compress images, limit chart count |
| Color inconsistency | Use shared color scheme from base.py |

---

## Out of Scope

- Interactive charts (requires JavaScript/web)
- Animation in PowerPoint
- Real-time data refresh
- Custom fonts (stick to system fonts)
