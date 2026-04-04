# Pyqual Pipeline Report

**Generated:** 2026-04-04 15:57:30
**Pipeline run:** 2026-04-04T13:57:28.968924+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["push<br/>2.1s"]
    style S0 fill:#90EE90
    S1["setup<br/>2.8s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["publish<br/>0.5s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["markdown_report<br/>2.8s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["calibrate<br/>60.0s"]
    style S4 fill:#FFB6C1
    S3 --> S4
    S5["lint<br/>0.0s"]
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
│  ✓ push                         2.1s 🟢        │
│  ✓ setup                        2.8s 🟢        │
│  ✓ publish                      0.5s 🟢        │
│  ✓ markdown_report              2.8s 🟢        │
│  ✗ calibrate                   60.0s 🔴        │
│  ✓ lint                         0.0s 🟢        │
├─────────────────────────────────────────────────────────────────┤
│  ❌ SOME GATES FAILED                                            │
│  ⏱️  Total time: 68.2s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| coverage | 34.4% | >= 55.0% | ❌ FAIL |

### 🔧 Stage Execution Details

#### ✅ push
- **Status:** passed
- **Duration:** 2.1s
- **Return code:** 0

#### ✅ setup
- **Status:** passed
- **Duration:** 2.8s
- **Return code:** 0

#### ✅ publish
- **Status:** passed
- **Duration:** 0.5s
- **Return code:** 0

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 2.8s
- **Return code:** 0

#### ❌ calibrate
- **Status:** failed
- **Duration:** 60.0s
- **Return code:** 124

#### ✅ lint
- **Status:** passed
- **Duration:** 0.0s
- **Return code:** 0


---

## 📝 Summary

❌ **Some quality gates failed.** Review the stage details above.
