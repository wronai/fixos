# Pyqual Pipeline Report

**Generated:** 2026-04-04 16:05:41
**Pipeline run:** 2026-04-04T14:05:39.028055+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["push<br/>2.2s"]
    style S0 fill:#90EE90
    S1["publish<br/>0.8s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["prefact<br/>86.2s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["markdown_report<br/>2.7s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["verify<br/>0.8s"]
    style S4 fill:#FFB6C1
    S3 --> S4
    G["✗ Gates Failed"]
    style G fill:#FFB6C1,stroke:#DC143C,stroke-width:3px
    S4 --> G
```

## 📈 ASCII Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                    PYQUAL PIPELINE FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│  ✓ push                         2.2s 🟢        │
│  ✓ publish                      0.8s 🟢        │
│  ✓ prefact                     86.2s 🟢        │
│  ✓ markdown_report              2.7s 🟢        │
│  ✗ verify                       0.8s 🔴        │
├─────────────────────────────────────────────────────────────────┤
│  ❌ SOME GATES FAILED                                            │
│  ⏱️  Total time: 92.6s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| coverage | 33.4% | >= 55.0% | ❌ FAIL |

### 🔧 Stage Execution Details

#### ✅ push
- **Status:** passed
- **Duration:** 2.2s
- **Return code:** 0

#### ✅ publish
- **Status:** passed
- **Duration:** 0.8s
- **Return code:** 0

#### ✅ prefact
- **Status:** passed
- **Duration:** 86.2s
- **Return code:** 0

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 2.7s
- **Return code:** 0

#### ❌ verify
- **Status:** failed
- **Duration:** 0.8s
- **Return code:** 2


---

## 📝 Summary

❌ **Some quality gates failed.** Review the stage details above.
