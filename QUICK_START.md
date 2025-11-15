# Quick Start Guide

## ⚡ 5-Minute Start

### Option 1: Just the Insights
```bash
Double-click: 1_GENERATE_REPORT.bat
```
- Generates `INSIGHTS_REPORT_LATEST.txt` (5 seconds)
- Opens automatically
- Contains all analysis: themes, frequencies, quick wins, executive summary

### Option 2: Visual Exploration
```bash
Double-click: 2_LAUNCH_DASHBOARD.bat
```
- Opens web app at http://localhost:8501
- 5 views: Overview, Deep Dive, Sentiment, Quick Wins, Cross-Question
- Export charts for presentations

---

## 📊 Timeline Options

### If You Have 2 Hours
1. Generate report → Read executive summary section (15 min)
2. Launch dashboard → Export 3 key charts (20 min)
3. Build 5-slide presentation (85 min)

### If You Have 1 Day
1. Generate report → Review thoroughly (1 hour)
2. Launch dashboard → Explore all views (1 hour)
3. Export 10 charts (30 min)
4. Build 10-slide presentation (2.5 hours)

### If You Have 1 Week (Recommended)
- **Day 1:** Report + dashboard exploration (2 hours)
- **Day 2-3:** Deep analysis + sentiment (4 hours)
- **Day 4-5:** Build presentation (3 hours)
- **Day 6-7:** Finalize + launch quick win (2 hours)

---

## 🎯 Best Charts for Presentations

**Must-Have (5):**
1. Team Culture word cloud
2. Future Mission word cloud
3. Stop Doing bar chart
4. Start Doing bar chart
5. AI Tools frequency

**Export:** Right-click chart → "Download plot as PNG"

---

## 💡 Pro Tips

### Quick Wins Fast
1. Open `INSIGHTS_REPORT_LATEST.txt`
2. Search for "[QUICK WINS ANALYSIS]"
3. Items with >5% mention rate = high priority

### Finding Key Insights
Search the report for:
- `Q1:` through `Q12:` - Question analysis
- `[QUICK WINS]` - Stop/start priorities
- `[AI ADOPTION GAP]` - Capability gaps
- `EXECUTIVE SUMMARY` - Key takeaways

### Export Strategy
- Word clouds for executives (visual impact)
- Bar charts for data clarity
- Sentiment pie charts for quick understanding

---

## 🚨 Common Issues

**Web app error?**
```bash
venv\Scripts\python.exe -m pip install -r requirements.txt
```

**No data?**
- Check `raw-data.csv` exists
- Verify "Question,Responses" header

**Charts won't export?**
- Use right-click, not screenshots
- Look for camera icon on hover

---

## ✅ Success Checklist

After running the tools, you should have:
- [ ] Insights report with top themes
- [ ] 10-15 exported charts
- [ ] 3-5 priority quick wins identified
- [ ] Cross-question insights documented
- [ ] Representative quotes extracted

---

**Next:** See `README.md` for full documentation
