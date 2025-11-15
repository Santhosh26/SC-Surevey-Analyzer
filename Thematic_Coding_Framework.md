# THEMATIC CODING FRAMEWORK FOR PRESALES SURVEY ANALYSIS

## Purpose
This framework guides systematic analysis of 100+ open-ended survey responses to extract actionable insights while maintaining analytical rigor.

---

## PHASE 1: PREPARATION (15-30 minutes)

### Step 1: Familiarize Yourself with the Data
- Read through 20-30 responses across different questions
- Note recurring words, phrases, and concepts
- Identify obvious patterns (e.g., multiple people mentioning "AI", "time management", "silos")
- Don't code yet - just observe

### Step 2: Create Initial Theme Hypotheses
Based on your initial reading, hypothesize 3-5 potential themes per question category:

**Example for Q1 (Culture):**
- Collaborative vs. Siloed
- Innovative vs. Conservative  
- Proactive vs. Reactive
- Supportive vs. Competitive

---

## PHASE 2: DEVELOP CODING SCHEME (1-2 hours)

### Step 3: Define 5-7 Themes Per Question

**Critical Rules:**
- Themes must be **mutually exclusive** (minimal overlap)
- Themes must be **exhaustive** (cover 90%+ of responses)
- Each theme needs clear **inclusion criteria**
- Use **parallel structure** (all positive, or positive/negative pairs)

### Theme Definition Template

```
THEME CODE: [4-6 letter abbreviation]
THEME NAME: [Clear, descriptive label]
DEFINITION: [What qualifies for this theme - be specific]
INCLUSION CRITERIA:
  - Mentions [specific keywords]
  - Describes [specific concepts/situations]
  - Implies [specific attitudes/beliefs]
EXCLUSION CRITERIA:
  - Does NOT mean [clarify boundaries]
EXAMPLE QUOTES:
  - "[Actual quote from data]"
  - "[Another actual quote]"
```

### Sample Coding Schemes by Question

#### Q1: TEAM CULTURE

**COLLAB** - Collaborative
- Definition: Emphasizes teamwork, knowledge sharing, cross-functional cooperation
- Keywords: "together", "team", "sharing", "collaborate", "support"
- Example: "We work well together across regions"

**SILOS** - Siloed/Fragmented
- Definition: Describes disconnection, isolation, lack of coordination
- Keywords: "disconnected", "isolated", "fragmented", "separate", "don't communicate"
- Example: "Each region operates independently with little coordination"

**INNOV** - Innovative
- Definition: Highlights experimentation, creativity, forward-thinking
- Keywords: "innovative", "creative", "experiment", "cutting-edge", "try new"
- Example: "Culture of experimentation and trying new approaches"

**REACT** - Reactive/Firefighting
- Definition: Describes urgency-driven, last-minute, crisis management mode
- Keywords: "reactive", "firefighting", "urgent", "rushed", "last minute"
- Example: "Always in firefighting mode with urgent requests"

**SUPPORT** - Supportive Leadership
- Definition: Mentions leadership support, psychological safety, investment in people
- Keywords: "supportive", "leadership", "trust", "safety", "development"
- Example: "Leadership is supportive and invests in our growth"

**OTHER** - Other/Uncategorizable
- Use sparingly (<5% of responses)

---

#### Q2: FUTURE MISSION

**TRUST** - Trusted Advisor/Strategic Partner
- Definition: Evolving from seller to strategic business advisor
- Keywords: "advisor", "consultant", "partner", "strategic", "trust"

**COMPLEX** - Navigate Complexity
- Definition: Help customers through increasingly complex technical/business landscapes
- Keywords: "complex", "integration", "architecture", "navigate"

**VALUE** - Demonstrate Business Value
- Definition: Focus on ROI, outcomes, measurable business impact
- Keywords: "ROI", "value", "outcomes", "business case", "impact"

**EDUCATE** - Educate/Enable Market
- Definition: Thought leadership, market education, category creation
- Keywords: "educate", "enable", "teach", "evangelize", "awareness"

**ACCEL** - Accelerate Customer Success
- Definition: Speed up adoption, implementation, time-to-value
- Keywords: "accelerate", "fast", "quick", "adoption", "time-to-value"

---

#### Q6: AI USAGE

**RESEARCH** - Research & Discovery
- Definition: Using AI to find information, competitor analysis, market research
- Keywords: "research", "find", "discover", "search", "analyze data"

**CONTENT** - Content Generation
- Definition: Creating demos, documentation, presentations, proposals
- Keywords: "create", "generate", "draft", "write", "automate docs"

**PREP** - Meeting/Demo Preparation
- Definition: Preparing for customer interactions, briefings, demos
- Keywords: "prepare", "brief", "plan", "demo prep"

**ANALYSIS** - Analysis & Insights
- Definition: Analyzing customer data, usage patterns, technical requirements
- Keywords: "analyze", "insights", "patterns", "understand", "interpret"

**CODE** - Code/Technical Work
- Definition: Writing scripts, configurations, integrations, troubleshooting
- Keywords: "code", "script", "debug", "configure", "technical"

---

#### Q11: HUMAN VALUE

**EMPATHY** - Emotional Intelligence/Empathy
- Definition: Understanding customer emotions, building relationships, trust
- Keywords: "empathy", "relationship", "trust", "understand", "listen"

**CREATIVITY** - Creative Problem Solving
- Definition: Novel solutions, adaptability to unique situations, thinking outside box
- Keywords: "creative", "unique", "adapt", "innovative", "custom"

**JUDGMENT** - Strategic Judgment
- Definition: Contextual decision-making, prioritization, knowing what matters
- Keywords: "judgment", "prioritize", "context", "strategic", "decide"

**STORYTELL** - Storytelling/Communication
- Definition: Crafting compelling narratives, making complex simple, persuasion
- Keywords: "story", "narrative", "explain", "communicate", "persuade"

---

#### Q12: CHALLENGES

**TIME** - Time/Capacity Constraints
- Definition: Too much work, not enough time, overloaded
- Keywords: "time", "busy", "overwhelmed", "capacity", "bandwidth"

**TOOLS** - Tool/System Limitations
- Definition: Inadequate tools, broken systems, technical debt
- Keywords: "tools", "systems", "broken", "outdated", "inadequate"

**COORD** - Coordination/Alignment Issues
- Definition: Difficulty coordinating across teams, misalignment
- Keywords: "coordination", "alignment", "communication", "silos", "disconnect"

**INFO** - Information Access
- Definition: Can't find information, knowledge scattered, poor documentation
- Keywords: "information", "documentation", "knowledge", "can't find"

**PROCESS** - Process Inefficiencies
- Definition: Bureaucracy, redundant processes, manual work
- Keywords: "process", "bureaucracy", "manual", "redundant", "inefficient"

---

## PHASE 3: CODING EXECUTION (3-5 hours)

### Step 4: Code All Responses

**Best Practices:**
- Code in batches of 20-30 responses at a time
- Take breaks to maintain consistency
- Each response can have 1-3 theme codes
- If a response is genuinely complex, assign 2-3 codes
- Use "OTHER" sparingly (<5% of responses)
- If you use OTHER >10%, your coding scheme needs refinement

**Coding Process:**
1. Open the appropriate question sheet (e.g., Q1_Culture)
2. Read response
3. Ask: "What is the PRIMARY theme here?"
4. Assign code to Column C
5. Ask: "Is there a strong SECONDARY theme?"
6. If yes, assign to Column D
7. If response is highly complex, assign tertiary code to Column E
8. Move to next response

**Consistency Checks:**
- Every 25 responses, re-read your theme definitions
- If uncertain, mark the response and return later
- Keep a "borderline cases" log for discussion

---

## PHASE 4: QUANTITATIVE ANALYSIS (1-2 hours)

### Step 5: Calculate Theme Frequencies

For each question sheet:

1. **Count themes** using COUNTIF formulas:
   - In Theme Frequency section (Column G-I)
   - List each theme code
   - Count occurrences: `=COUNTIF(C:C,"COLLAB")+COUNTIF(D:D,"COLLAB")+COUNTIF(E:E,"COLLAB")`
   - Calculate percentage: `=H6/SUM($H$6:$H$12)`

2. **Rank themes** by frequency
   - Sort theme table by Count (descending)
   - Identify top 3-5 themes (these are your "major themes")

3. **Check for "OTHER"**
   - If OTHER >10%, examine those responses
   - Can you create a new theme that captures them?
   - Or are they genuinely scattered edge cases?

---

## PHASE 5: QUALITATIVE SYNTHESIS (2-3 hours)

### Step 6: Extract Representative Quotes

For each MAJOR theme (top 3-5):

1. **Find best examples:**
   - Scan all responses tagged with that theme
   - Look for quotes that:
     - Clearly articulate the theme
     - Are quotable (concise, powerful)
     - Represent different perspectives within the theme
   - Select 2-3 per theme

2. **Document quotes:**
   - Copy Response ID
   - Copy exact quote (or relevant excerpt)
   - Tag with theme code

**Example:**
| Theme | Response ID | Quote |
|-------|-------------|-------|
| COLLAB | R023 | "Best thing about our team is how we share knowledge across regions" |
| COLLAB | R047 | "Strong collaborative culture, everyone willing to help" |

---

### Step 7: Identify Sub-themes and Nuances

Within each major theme, are there variations?

**Example - Within "TRUST" (Future Mission):**
- Sub-theme A: Focus on C-level engagement
- Sub-theme B: Focus on technical advisor role
- Sub-theme C: Focus on business outcomes advisor

**Document this structure:**
```
THEME: Trusted Advisor (47% of responses)
  Sub-theme: C-level Strategic Partner (18%)
    - "Need to engage at C-level, not just IT"
  Sub-theme: Deep Technical Advisor (21%)
    - "Technical expert they can rely on for architecture"
  Sub-theme: Business Outcomes Focus (8%)
    - "Help them achieve business goals, not just tech"
```

---

## PHASE 6: CROSS-QUESTION ANALYSIS (2-3 hours)

### Step 8: Look for Patterns Across Questions

**Key Cross-References:**

1. **Vision vs. Reality Check:**
   - Q2 (Future Mission) vs. Q12 (Current Challenges)
   - Are current challenges blocking the future vision?
   - Example: Mission = "Trusted Advisor" but Challenge = "No time for strategic work"

2. **Aspiration vs. Capability:**
   - Q11 (Human Value) vs. Q6/Q7 (AI Usage/Tools)
   - Can AI free up time for the "uniquely human" value?
   - What's the gap between desired AI use vs. current use?

3. **Skills Demand vs. Supply:**
   - Q4 (Future Skills) vs. Q5 (Additional Skills Needed)
   - Which ranked skills are mentioned as gaps?
   - Where do we need investment?

4. **Relationship Evolution:**
   - Q10 (Cross-functional) vs. Q12 (Challenges)
   - Are coordination issues driven by relationship problems?
   - What needs to change?

**Create a Cross-Reference Matrix:**

| Theme Cluster | Related Questions | Key Insight | Recommendation |
|--------------|-------------------|-------------|----------------|
| AI Readiness | Q6, Q7, Q12 | Want AI for content (45%) but only 20% use it regularly. Bottleneck = training | Launch AI training program |
| Strategic Value | Q2, Q11, Q12 | Vision = trusted advisor, unique value = empathy, but challenge = no time for relationships | Automate admin tasks to free capacity |

---

## PHASE 7: VALIDATION & REFINEMENT (1-2 hours)

### Step 9: Validate Your Analysis

**Consistency Checks:**
1. Have a colleague blind-code 10% of responses
2. Calculate inter-rater reliability (aim for >80% agreement)
3. Discuss disagreements and refine definitions

**Reality Checks:**
1. Do the themes make intuitive sense to someone familiar with presales?
2. Are there any surprising themes? (good - those are insights!)
3. Are themes too granular or too broad?

**Refinement Options:**
- Merge themes if <5% frequency each and conceptually similar
- Split themes if >30% frequency and contains distinct sub-themes
- Rename themes for clarity

---

## PHASE 8: INSIGHT GENERATION (2-3 hours)

### Step 10: Move from Data to Insights

**Framework: So What? → Now What?**

For each major theme:
1. **What did we learn?** (the finding)
2. **So what?** (why it matters)
3. **Now what?** (what to do about it)

**Example:**

**Finding:** 47% describe future mission as "Trusted Advisor/Strategic Partner"

**So What?**
- Strong consensus on strategic evolution
- Implies shift from transactional to consultative selling
- Requires different skills, metrics, and operating model

**Now What?**
- Immediate: Redefine success metrics (add customer satisfaction, strategic influence)
- Medium-term: Launch advisory skills training program
- Long-term: Restructure team into specialist vs. generalist tracks

---

### Step 11: Identify Key Tensions

Look for **contradictions or competing priorities:**

**Examples:**
- "Need deep technical expertise" (32%) vs. "Need broad business acumen" (28%)
  → **Tension:** Specialist vs. Generalist model
  
- "Want more time with customers" (41%) vs. "Too many internal meetings" (35%)
  → **Tension:** External focus vs. Internal coordination
  
- "AI will automate tasks" (52%) vs. "Need human judgment" (48%)
  → **Tension:** Automation anxiety vs. Augmentation opportunity

**Document tensions in a 2x2 matrix:**

```
        High Tech Depth
              |
Generalist ---|--- Specialist
              |
        High Business Breadth
```

These tensions reveal strategic choices leadership must make.

---

## DELIVERABLE CHECKLIST

### 1. Analysis Workbook (Excel)
- [ ] All responses coded with 1-3 theme codes
- [ ] Theme frequency calculated for each question
- [ ] Representative quotes extracted for top themes
- [ ] Cross-question insights documented
- [ ] Zero formula errors

### 2. Theme Code Documentation
- [ ] All themes defined with inclusion/exclusion criteria
- [ ] Inter-rater reliability >80% (if validated)
- [ ] Sub-themes identified where relevant

### 3. Quick Wins List
- [ ] Top 5 "Stop Doing" items from Q13, prioritized by frequency + impact
- [ ] Top 5 "Start Doing" items from Q14, prioritized by impact/effort
- [ ] Owner and timeline assigned

### 4. Executive Summary
- [ ] 1-page overview with top 3 findings per category
- [ ] Key tensions and trade-offs identified
- [ ] 3-5 strategic recommendations
- [ ] Visual dashboard with key metrics

### 5. Detailed Report (Optional)
- [ ] Methodology section
- [ ] Findings by question with supporting data
- [ ] Cross-question analysis
- [ ] Appendix with full theme definitions and quote library

---

## ADVANCED TECHNIQUES

### Using AI to Accelerate Analysis

**Theme Discovery Prompt:**
```
I have 100 responses to this question: "[question text]"

Here are 30 sample responses:
[paste 30 responses]

Analyze these and suggest 5-7 major themes with:
1. Theme name
2. Definition
3. Estimated frequency (% of these 30)
4. 2 example quotes per theme
```

**Sentiment Analysis Prompt:**
```
Analyze the sentiment of these responses:
[paste responses]

For each response, tag with: OPTIMISTIC, ANXIOUS, FRUSTRATED, or NEUTRAL
Then give me a distribution breakdown.
```

**Gap Analysis Prompt:**
```
Compare these two sets of responses:
Q6 (What would you use AI for): [paste]
Q7 (What AI tools you currently use): [paste]

Identify the top 5 capability gaps between aspiration and current state.
```

### Statistical Analysis (if you have demographic data)

**Chi-Square Test for Independence:**
- Do senior vs. junior folks see the future differently?
- Do different regions have different pain points?
- Use Python scipy.stats.chi2_contingency

**Correlation Analysis:**
- Do people who mention "time constraints" also mention "process inefficiency"?
- Calculate theme co-occurrence matrix

---

## COMMON PITFALLS TO AVOID

### 1. Confirmation Bias
- **Risk:** You find only what you expect to find
- **Mitigation:** Code 20% of responses before forming hypotheses

### 2. Theme Proliferation
- **Risk:** Creating 15+ themes per question (too granular)
- **Mitigation:** Force yourself to 5-7 themes max; merge related themes

### 3. Quote Cherry-Picking
- **Risk:** Selecting quotes that support your preferred narrative
- **Mitigation:** Use systematic sampling (e.g., first 3 responses per theme)

### 4. Ignoring the "Boring Middle"
- **Risk:** Focusing only on extreme or interesting responses
- **Mitigation:** Ensure themes capture the majority (80%+) of responses

### 5. Analysis Paralysis
- **Risk:** Spending weeks coding and never getting to insights
- **Mitigation:** Time-box each phase; aim for "good enough" not "perfect"

---

## TIMELINE ESTIMATE

| Phase | Time | Cumulative |
|-------|------|------------|
| Preparation | 0.5 hr | 0.5 hr |
| Develop coding scheme | 2 hr | 2.5 hr |
| Code all responses | 4 hr | 6.5 hr |
| Quantitative analysis | 1.5 hr | 8 hr |
| Qualitative synthesis | 2.5 hr | 10.5 hr |
| Cross-question analysis | 2.5 hr | 13 hr |
| Validation | 1.5 hr | 14.5 hr |
| Insight generation | 2 hr | 16.5 hr |
| **Total** | **~17 hours** | |

**Faster approach with AI assistance:** ~8-10 hours

---

## FINAL THOUGHTS

This framework transforms raw survey responses into actionable intelligence. The goal is not just to count themes, but to:

1. **Understand the current state** (culture, challenges)
2. **Clarify the future vision** (mission, skills, value)
3. **Identify the gap** (what's blocking the transition)
4. **Provide a roadmap** (quick wins → strategic investments)

The analysis is successful if leadership can make data-driven decisions about:
- Where to invest (training, tools, headcount)
- What to change (processes, metrics, org structure)
- How to communicate (the narrative about presales evolution)

Done right, this survey analysis becomes the foundation for your presales transformation strategy for 2025-2027.
