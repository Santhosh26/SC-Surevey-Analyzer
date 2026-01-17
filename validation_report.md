# LLM Batch Summarizer Validation Report

**Generated**: 2026-01-09T11:38:47.468239
**Model**: us.anthropic.claude-opus-4-5-20251101-v1:0
**Dataset**: 1416 responses across 14 questions

---

## Overall Status: [FAIL] FAILED

The LLM batch summarizer has failed validation and **should NOT be used** for strategic decision-making until issues are resolved.

### Failures Detected:
-  Quote Hallucination Detection: 60/70 quotes found in raw data
-  Response Count Validation: 12/14 response counts within tolerance

---

## Test Results

### Tier 1: Critical Tests (Must Pass 100%)

| Test | Status | Pass Rate | Required |
|------|--------|-----------|----------|
| Quote Hallucination Detection | [FAIL] FAIL | 85.7% | 100.0% |
| Response Count Validation | [FAIL] FAIL | 85.7% | 100.0% |
| JSON Schema Validation | [PASS] PASS | 100.0% | 100.0% |

### Tier 2: Accuracy Tests (Must Pass 70-80%)

| Test | Status | Pass Rate | Required |
|------|--------|-----------|----------|
| Frequency Estimation Accuracy | [PASS] PASS | 80.0% | 80.0% |

---

## Detailed Findings

### Test 1: Quote Hallucination Detection

**Status**: FAIL (85.7%)

**Summary**: 60/70 quotes found in raw data

**Sample Results**:

- {'question': 'As routine tasks get automated, what becomes the most important, uniquely human value that Presales delivers?', 'quote': 'Active listening and understanding what client actually needs to solve their problems', 'status': 'PASS', 'match_type': 'exact'}
- {'question': 'As routine tasks get automated, what becomes the most important, uniquely human value that Presales delivers?', 'quote': 'Emotional Intelligence and Trust Building', 'status': 'PASS', 'match_type': 'exact'}
- {'question': 'As routine tasks get automated, what becomes the most important, uniquely human value that Presales delivers?', 'quote': "Translating customer's needs and pains into solutions", 'status': 'PASS', 'match_type': 'exact'}
- {'question': 'As routine tasks get automated, what becomes the most important, uniquely human value that Presales delivers?', 'quote': 'Trusted advisory, relationship, addressing customer challenges with better story telling', 'status': 'PASS', 'match_type': 'exact'}
- {'question': 'As routine tasks get automated, what becomes the most important, uniquely human value that Presales delivers?', 'quote': 'People buy from people!', 'status': 'PASS', 'match_type': 'fuzzy_90%'}

... and 65 more

### Test 2: Response Count Validation

**Status**: FAIL (85.7%)

**Summary**: 12/14 response counts within tolerance

**Sample Results**:

- {'question': 'As routine tasks get automated, what becomes the most import', 'reported': 105, 'actual': 105, 'diff': 0, 'status': 'PASS'}
- {'question': 'What do you believe are the future roles in International Pr', 'reported': 255, 'actual': 0, 'diff': 255, 'status': 'FAIL'}
- {'question': "How should our team's relationship with Product Management ,", 'reported': 106, 'actual': 106, 'diff': 0, 'status': 'PASS'}
- {'question': 'How would you describe  the team culture in International Pr', 'reported': 133, 'actual': 133, 'diff': 0, 'status': 'PASS'}
- {'question': 'How would you use AI to be more efficient in your role?', 'reported': 115, 'actual': 115, 'diff': 0, 'status': 'PASS'}

... and 9 more

### Test 3: JSON Schema Validation

**Status**: PASS (100.0%)

**Summary**: Schema valid

### Test 4: Frequency Estimation Accuracy

**Status**: PASS (80.0%)

**Summary**: 52/65 frequency claims within ±15% tolerance

**Sample Results**:

- {'question': 'As routine tasks get automated, what becomes the most import', 'theme': 'Trust & Credibility', 'claimed_freq': '38%', 'estimated_actual': '25%', 'diff': '13%', 'status': 'PASS'}
- {'question': 'As routine tasks get automated, what becomes the most import', 'theme': 'Relationship Building', 'claimed_freq': '28%', 'estimated_actual': '18%', 'diff': '10%', 'status': 'PASS'}
- {'question': 'As routine tasks get automated, what becomes the most import', 'theme': 'Empathy & Emotional Intelligence', 'claimed_freq': '15%', 'estimated_actual': '9%', 'diff': '6%', 'status': 'PASS'}
- {'question': 'As routine tasks get automated, what becomes the most import', 'theme': 'Human Connection & Personal Engagement', 'claimed_freq': '12%', 'estimated_actual': '18%', 'diff': '6%', 'status': 'PASS'}
- {'question': 'As routine tasks get automated, what becomes the most import', 'theme': 'Strategic Advisory & Problem-Solving', 'claimed_freq': '10%', 'estimated_actual': '3%', 'diff': '7%', 'status': 'PASS'}

... and 60 more

---

## Recommendations

### Blocking Issues:
-  Quote Hallucination Detection: Fix before using in production
-  Response Count Validation: Fix before using in production

### Accuracy Concerns:

### Risk Assessment:
- **Hallucination Risk**: [FAIL] HIGH (fabricated content detected)
- **Accuracy Risk**: [WARN] MEDIUM (review frequency outliers)
- **Quality Risk**: [WARN] MEDIUM (manual review recommended for insights)

---

## Next Steps

1.  **DO NOT DEPLOY** - Fix failing tests first
2. 🔍 **Investigate failures** - Review details in validation_report.json
3. 🛠️ **Fix and re-validate** - Re-run this script after fixes

---

**Validated by**: llm_eval_validator.py
**Report generated**: 2026-01-09T11:38:47.468239
