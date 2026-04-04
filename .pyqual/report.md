# Pyqual Pipeline Report

**Generated:** 2026-04-04 15:47:42
**Pipeline run:** 2026-04-04T13:47:40.107277+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["markdown_report<br/>2.6s"]
    style S0 fill:#90EE90
    S1["setup<br/>2.7s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["lint<br/>0.0s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["push<br/>2.0s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["publish<br/>0.7s"]
    style S4 fill:#90EE90
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
│  ✓ markdown_report              2.6s 🟢        │
│  ✓ setup                        2.7s 🟢        │
│  ✓ lint                         0.0s 🟢        │
│  ✓ push                         2.0s 🟢        │
│  ✓ publish                      0.7s 🟢        │
├─────────────────────────────────────────────────────────────────┤
│  ❌ SOME GATES FAILED                                            │
│  ⏱️  Total time: 8.0s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| coverage | 32.9% | >= 55.0% | ❌ FAIL |

### 🔧 Stage Execution Details

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 2.6s
- **Return code:** 0

#### ✅ setup
- **Status:** passed
- **Duration:** 2.7s
- **Return code:** 0

#### ✅ lint
- **Status:** passed
- **Duration:** 0.0s
- **Return code:** 0

#### ✅ push
- **Status:** passed
- **Duration:** 2.0s
- **Return code:** 0

#### ✅ publish
- **Status:** passed
- **Duration:** 0.7s
- **Return code:** 0


---

## 📝 Summary

❌ **Some quality gates failed.** Review the stage details above.
