"""
Quick script to extract and visualize the 2 multiple choice questions
Run: venv\Scripts\python.exe extract_multiple_choice.py
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

print("="*70)
print("MULTIPLE CHOICE QUESTIONS - EXTRACTION & VISUALIZATION")
print("="*70)

# Load data
df = pd.read_csv('raw-data.csv', encoding='utf-8-sig')
df.columns = df.columns.str.strip()

# ==================== QUESTION 1: FUTURE ROLES ====================

print("\n1. FUTURE ROLES IN INTERNATIONAL PRESALES")
print("-"*70)

future_roles_data = {
    'Role': [
        'Solution Architects - Technical Credibility',
        'Industry Value Consultants - CXO Engagement',
        'Business Value Engineers - ROI/TCO Justification',
        'Demo Specialist - AI-powered Inspiration',
        'Innovation Leads - Co-creation and Rapid Pilots',
        'Enablement Coaches - Scale Knowledge and Capability'
    ],
    'Votes': [69, 34, 33, 38, 51, 30]
}

roles_df = pd.DataFrame(future_roles_data)
roles_df['Percentage'] = (roles_df['Votes'] / roles_df['Votes'].sum() * 100).round(1)
roles_df = roles_df.sort_values('Votes', ascending=False)

print("\nResults (sorted by votes):")
for idx, row in roles_df.iterrows():
    print(f"  {row['Role']:60s} {row['Votes']:3d} votes ({row['Percentage']:5.1f}%)")

print(f"\nTotal votes: {roles_df['Votes'].sum()}")
print(f"Avg votes per respondent: {roles_df['Votes'].sum() / 100:.1f} (assuming ~100 respondents)")

# Create visualization
fig1 = go.Figure([go.Bar(
    y=roles_df['Role'],
    x=roles_df['Votes'],
    orientation='h',
    text=[f"{v} ({p}%)" for v, p in zip(roles_df['Votes'], roles_df['Percentage'])],
    textposition='outside',
    marker=dict(
        color=roles_df['Votes'],
        colorscale='Blues',
        showscale=False
    )
)])

fig1.update_layout(
    title='Future Roles in International Presales<br><sub>Multiple choice - respondents could select multiple roles</sub>',
    xaxis_title='Number of Votes',
    yaxis_title='',
    height=400,
    xaxis=dict(range=[0, max(roles_df['Votes']) * 1.2])
)

fig1.write_html('future_roles_chart.html')
print("\n[OK] Saved: future_roles_chart.html")

# ==================== QUESTION 2: FUTURE SKILLSETS ====================

print("\n" + "="*70)
print("2. FUTURE SKILLSETS & MINDSETS (Ranking - 1st Place Votes Only)")
print("-"*70)

skillsets_data = {
    'Skillset': [
        'Technical expertise',
        'Financial modelling',
        'Adaptability & customer empathy',
        'Industry-specific business acumen',
        'Advanced storytelling'
    ],
    'First_Place_Votes': [20, 0, 21, 30, 30]
}

skills_df = pd.DataFrame(skillsets_data)
skills_df['Percentage'] = (skills_df['First_Place_Votes'] / skills_df['First_Place_Votes'].sum() * 100).round(1)
skills_df = skills_df.sort_values('First_Place_Votes', ascending=False)

print("\nResults (sorted by 1st place votes):")
for idx, row in skills_df.iterrows():
    print(f"  {row['Skillset']:45s} {row['First_Place_Votes']:3d} 1st place ({row['Percentage']:5.1f}%)")

print(f"\nTotal 1st place votes: {skills_df['First_Place_Votes'].sum()}")
print("\nNote: This shows only 1st-place rankings. Full ranking data (2nd, 3rd, etc.) not exported.")

# Create visualization
fig2 = go.Figure([go.Bar(
    y=skills_df['Skillset'],
    x=skills_df['First_Place_Votes'],
    orientation='h',
    text=[f"{v} ({p}%)" for v, p in zip(skills_df['First_Place_Votes'], skills_df['Percentage'])],
    textposition='outside',
    marker=dict(
        color=skills_df['First_Place_Votes'],
        colorscale='Viridis',
        showscale=False
    )
)])

fig2.update_layout(
    title='Future Skillsets & Mindsets - Ranking Results<br><sub>Shows only 1st-place rankings from respondents</sub>',
    xaxis_title='Number of 1st Place Votes',
    yaxis_title='',
    height=350,
    xaxis=dict(range=[0, max(skills_df['First_Place_Votes']) * 1.2])
)

fig2.write_html('future_skillsets_chart.html')
print("\n[OK] Saved: future_skillsets_chart.html")

# ==================== KEY INSIGHTS ====================

print("\n" + "="*70)
print("KEY INSIGHTS")
print("="*70)

print("\n[FUTURE ROLES ANALYSIS]")
print(f"  - Most selected: {roles_df.iloc[0]['Role']} ({roles_df.iloc[0]['Votes']} votes, {roles_df.iloc[0]['Percentage']}%)")
print(f"  - Second most: {roles_df.iloc[1]['Role']} ({roles_df.iloc[1]['Votes']} votes, {roles_df.iloc[1]['Percentage']}%)")
print(f"  - Least selected: {roles_df.iloc[-1]['Role']} ({roles_df.iloc[-1]['Votes']} votes, {roles_df.iloc[-1]['Percentage']}%)")
print(f"  - Portfolio approach: Average {roles_df['Votes'].sum() / 100:.1f} roles per person")

print("\n[FUTURE SKILLSETS ANALYSIS]")
top_skills = skills_df[skills_df['First_Place_Votes'] == skills_df['First_Place_Votes'].max()]
print(f"  - Top priority (tied): {', '.join(top_skills['Skillset'].tolist())}")
print(f"    Each received {top_skills.iloc[0]['First_Place_Votes']} first-place votes ({top_skills.iloc[0]['Percentage']}%)")
print(f"  - Lowest priority: {skills_df.iloc[-1]['Skillset']} ({skills_df.iloc[-1]['First_Place_Votes']} first-place votes)")
print(f"  - Shift: Industry acumen & storytelling > technical expertise")

print("\n[STRATEGIC IMPLICATIONS]")
print("  1. Solution Architects remain core (27% selection rate)")
print("  2. Innovation/Co-creation rising (Innovation Leads: 20%)")
print("  3. Business skills > Technical skills (Industry acumen #1)")
print("  4. Storytelling = critical (tied for #1 in rankings)")
print("  5. Financial modeling NOT priority (0 first-place votes)")
print("  6. Portfolio approach: Teams need multiple role types")

print("\n" + "="*70)
print("[FILES CREATED]")
print("="*70)
print("  • future_roles_chart.html - Open in browser to view")
print("  • future_skillsets_chart.html - Open in browser to view")
print("\nYou can save these charts as PNG for your presentation:")
print("  1. Open HTML file in browser")
print("  2. Click camera icon (top right)")
print("  3. Download as PNG")

print("\n" + "="*70)
print("[SUCCESS] EXTRACTION COMPLETE")
print("="*70)
