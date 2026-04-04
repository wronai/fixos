# Pyqual Pipeline Report

**Generated:** 2026-04-04 15:55:13
**Pipeline run:** 2026-04-04T13:55:10.388449+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["markdown_report<br/>3.8s"]
    style S0 fill:#90EE90
    S1["setup<br/>3.1s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["calibrate<br/>2.9s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["lint<br/>0.0s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["push<br/>2.0s"]
    style S4 fill:#90EE90
    S3 --> S4
    S5["publish<br/>0.7s"]
    style S5 fill:#90EE90
    S4 --> S5
    G["✗ Gates Failed"]
    style G fill:#FFB6C1,stroke:#DC143C,stroke-width:3px
    S5 --> G
```

## 📈 ASCII Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                    PYQUAL PIPELINE FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│  ✓ markdown_report              3.8s 🟢        │
│  ✓ setup                        3.1s 🟢        │
│  ✓ calibrate                    2.9s 🟢        │
│  ✓ lint                         0.0s 🟢        │
│  ✓ push                         2.0s 🟢        │
│  ✓ publish                      0.7s 🟢        │
├─────────────────────────────────────────────────────────────────┤
│  ❌ SOME GATES FAILED                                            │
│  ⏱️  Total time: 12.5s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| coverage | 32.9% | >= 55.0% | ❌ FAIL |

### 🔧 Stage Execution Details

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 3.8s
- **Return code:** 0

#### ✅ setup
- **Status:** passed
- **Duration:** 3.1s
- **Return code:** 0

#### ✅ calibrate
- **Status:** passed
- **Duration:** 2.9s
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
