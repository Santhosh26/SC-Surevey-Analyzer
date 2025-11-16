# Deployment Guide

This guide explains how to package and distribute the SC Survey Analyzer application for standalone deployment.

---

## 📦 Deployment Options

### Option 1: Script-Based Deployment (Recommended for Most Users)

**Best for:** Users with Python installed, faster download, easier updates

**Package Contents:**
```
SC-Survey-Analyzer/
├── setup.bat / setup.sh              # First-time setup
├── 1_GENERATE_REPORT.bat / .sh       # Report generator
├── 2_LAUNCH_DASHBOARD.bat / .sh      # Dashboard launcher
├── generate_insights.py              # Core app
├── app.py                            # Core app
├── raw-data.csv                      # Data file
├── requirements.txt                  # Dependencies
├── .streamlit/config.toml            # Theme config
├── README.md                         # Documentation
└── QUICK_START.md                    # Quick start guide
```

**Distribution Steps:**
1. Delete these folders if they exist:
   - `venv/`
   - `__pycache__/`
   - `build/`
   - `dist/`
   - `.claude/`

2. Delete generated files:
   - `INSIGHTS_REPORT_*.txt`
   - `future_*.html`

3. Zip the entire folder

4. Share with users

**User Requirements:**
- Python 3.8 or higher installed
- Internet connection (for initial setup only)
- ~500 MB disk space (for dependencies)

**User Instructions:**
```
1. Extract the zip file
2. Run setup.bat (Windows) or ./setup.sh (Mac/Linux)
3. Use launcher scripts to run the app
```

**Package Size:** ~160 KB (compressed zip)

---

### Option 2: Executable Deployment (Standalone)

**Best for:** Users without Python, corporate environments with restrictions

**How to Build:**

**Windows:**
```bash
# 1. Setup environment
setup.bat

# 2. Activate venv
venv\Scripts\activate

# 3. Build executable
build_executable.bat
```

**Mac/Linux:**
```bash
# 1. Setup environment
./setup.sh

# 2. Activate venv
source venv/bin/activate

# 3. Build executable
./build_executable.sh
```

**Output Location:** `dist/SC_Survey_Analyzer/`

**Distribution Steps:**
1. Navigate to `dist/SC_Survey_Analyzer/`
2. Copy `raw-data.csv` to this folder (if not included)
3. Copy `.streamlit/config.toml` to this folder (if not included)
4. Zip the entire `SC_Survey_Analyzer` folder
5. Share with users

**User Requirements:**
- NO Python installation needed
- ~100-150 MB disk space
- Extract and run

**User Instructions:**
```
Windows:
1. Extract the zip file
2. Double-click SC_Survey_Analyzer.exe

Mac/Linux:
1. Extract the zip file
2. Run ./SC_Survey_Analyzer
```

**Package Size:** ~80-120 MB (compressed)

**Platform Notes:**
- Windows executable only runs on Windows
- Mac executable only runs on Mac (same OS version or newer)
- Linux executable may require same distribution family
- Build on target platform for best compatibility

---

## 🔧 Pre-Distribution Checklist

### Clean Repository

Run these commands before packaging:

**Windows:**
```bash
# Delete virtual environment
rmdir /s /q venv

# Delete Python cache
rmdir /s /q __pycache__

# Delete build artifacts
rmdir /s /q build dist

# Delete generated files
del INSIGHTS_REPORT_*.txt
del future_*.html

# Delete IDE files
rmdir /s /q .claude
```

**Mac/Linux:**
```bash
# Delete virtual environment
rm -rf venv

# Delete Python cache
rm -rf __pycache__

# Delete build artifacts
rm -rf build dist

# Delete generated files
rm -f INSIGHTS_REPORT_*.txt
rm -f future_*.html

# Delete IDE files
rm -rf .claude
```

### Verify Essential Files

Ensure these files are present:
- [ ] `app.py`
- [ ] `generate_insights.py`
- [ ] `raw-data.csv`
- [ ] `requirements.txt`
- [ ] `.streamlit/config.toml`
- [ ] `README.md`
- [ ] `QUICK_START.md`
- [ ] `setup.bat` and `setup.sh`
- [ ] `1_GENERATE_REPORT.bat` and `1_generate_report.sh`
- [ ] `2_LAUNCH_DASHBOARD.bat` and `2_launch_dashboard.sh`

### Test Setup Process

Before distributing, test the setup on a clean environment:

**Windows:**
```bash
setup.bat
1_GENERATE_REPORT.bat
2_LAUNCH_DASHBOARD.bat
```

**Mac/Linux:**
```bash
./setup.sh
./1_generate_report.sh
./2_launch_dashboard.sh
```

---

## 📋 Distribution Package Comparison

| Feature | Script-Based | Executable |
|---------|--------------|------------|
| **Package Size** | ~160 KB | ~80-120 MB |
| **Python Required** | Yes (3.8+) | No |
| **Internet Required** | Yes (setup only) | No |
| **Setup Time** | ~5 minutes | Instant |
| **Platform** | Cross-platform | Platform-specific |
| **Updates** | Easy (git pull) | Rebuild required |
| **Corporate Friendly** | Maybe | Yes |
| **Best For** | Developers, tech users | End users, non-technical |

---

## 🚀 Quick Distribution Commands

### Script-Based Package

**Windows:**
```bash
# Clean
rmdir /s /q venv __pycache__ build dist .claude
del INSIGHTS_REPORT_*.txt future_*.html

# Create archive (requires 7-Zip or similar)
7z a SC-Survey-Analyzer.zip * -xr!venv -xr!__pycache__ -xr!.git -xr!build -xr!dist -xr!.claude -x!INSIGHTS_REPORT_*.txt -x!future_*.html
```

**Mac/Linux:**
```bash
# Clean
rm -rf venv __pycache__ build dist .claude
rm -f INSIGHTS_REPORT_*.txt future_*.html

# Create archive
zip -r SC-Survey-Analyzer.zip . -x "venv/*" "__pycache__/*" ".git/*" "build/*" "dist/*" ".claude/*" "INSIGHTS_REPORT_*.txt" "future_*.html"
```

### Executable Package

After building with `build_executable.bat` or `build_executable.sh`:

**Windows:**
```bash
cd dist
7z a SC-Survey-Analyzer-Standalone.zip SC_Survey_Analyzer
```

**Mac/Linux:**
```bash
cd dist
zip -r SC-Survey-Analyzer-Standalone.zip SC_Survey_Analyzer
```

---

## 📧 Distribution Email Template

### For Script-Based Deployment

**Subject:** SC Survey Analyzer - Installation Package

**Body:**
```
Hi [Name],

Attached is the SC Survey Analyzer toolkit for analyzing presales survey responses.

QUICK START:

1. Extract the zip file to your preferred location

2. Run the setup script (one-time only):
   - Windows: Double-click setup.bat
   - Mac/Linux: Run ./setup.sh in terminal

3. Generate insights report:
   - Windows: Double-click 1_GENERATE_REPORT.bat
   - Mac/Linux: Run ./1_generate_report.sh

4. (Optional) Launch interactive dashboard:
   - Windows: Double-click 2_LAUNCH_DASHBOARD.bat
   - Mac/Linux: Run ./2_launch_dashboard.sh

REQUIREMENTS:
- Python 3.8 or higher (check: python --version)
- Internet connection (for initial setup only)
- ~500 MB disk space

DOCUMENTATION:
- See README.md for full documentation
- See QUICK_START.md for quick reference

Questions? Reply to this email.

Best regards,
[Your Name]
```

### For Executable Deployment

**Subject:** SC Survey Analyzer - Standalone Application

**Body:**
```
Hi [Name],

Attached is the standalone SC Survey Analyzer application. No Python installation required!

QUICK START:

1. Extract the zip file to your preferred location

2. Run the application:
   - Windows: Double-click SC_Survey_Analyzer.exe
   - Mac/Linux: Run ./SC_Survey_Analyzer

3. The dashboard opens in your browser at http://localhost:8501

REQUIREMENTS:
- No Python needed
- ~150 MB disk space
- Any modern web browser

NOTE: First launch may take 10-15 seconds to initialize.

Questions? Reply to this email.

Best regards,
[Your Name]
```

---

## 🐛 Common Deployment Issues

### PyInstaller Build Fails

**Issue:** `ModuleNotFoundError` during build

**Solution:**
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Clean previous builds
rm -rf build dist

# Rebuild
pyinstaller app.spec --clean
```

### Executable Won't Run on Target Machine

**Issue:** "Missing DLL" or "Library not found"

**Solution:**
- Ensure target machine has Visual C++ Redistributable (Windows)
- Build on same OS version as target (Mac/Linux)
- Use `--onefile` mode in PyInstaller (larger but more portable)

### Streamlit Not Loading

**Issue:** Executable runs but Streamlit doesn't start

**Solution:**
- Check `app.spec` includes all Streamlit data files
- Verify `.streamlit/config.toml` is in the package
- Test with `streamlit run app.py` before building

### Data File Not Found

**Issue:** "raw-data.csv not found"

**Solution:**
- Ensure `raw-data.csv` is in the same directory as the executable
- Update `app.spec` to include data files:
```python
added_files = [
    ('raw-data.csv', '.'),
]
```

---

## 📊 Deployment Recommendations

### For Internal Team (Same Organization)

**Recommended:** Script-Based
- Easy to update (git pull)
- Smaller package size
- Developers likely have Python
- Can customize easily

### For External Clients

**Recommended:** Executable
- No technical setup required
- Professional appearance
- No Python dependency issues
- Works out-of-the-box

### For Cloud Deployment

**Recommended:** Docker + Streamlit Cloud
- See README_WEB_APP.md for cloud deployment
- Best for sharing with many users
- No local installation needed
- Always up-to-date

---

## 📝 Version Control Best Practices

### .gitignore Recommendations

The included `.gitignore` excludes:
```
venv/
__pycache__/
*.pyc
build/
dist/
*.spec
INSIGHTS_REPORT_*.txt
future_*.html
.claude/
```

These files should NEVER be committed to version control.

### Release Process

1. Test thoroughly on clean environment
2. Update version number in README.md
3. Tag release in git: `git tag v1.0.0`
4. Build deployment packages
5. Upload to distribution platform (email, SharePoint, etc.)
6. Send distribution email with instructions

---

## ✅ Final Checklist

Before distributing:

- [ ] All unwanted files removed (venv, __pycache__, etc.)
- [ ] Requirements.txt is up-to-date
- [ ] Setup scripts tested on clean environment
- [ ] README.md and QUICK_START.md are accurate
- [ ] Data file (raw-data.csv) is included
- [ ] .streamlit/config.toml is included
- [ ] All launcher scripts (.bat and .sh) work correctly
- [ ] (If executable) Build tested on target platform
- [ ] Package size is reasonable (<200 KB script-based, <150 MB executable)
- [ ] Distribution email drafted
- [ ] Documentation reviewed

---

**Next Steps:** Choose your deployment method above and follow the corresponding instructions.
