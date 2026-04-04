# Pyqual Pipeline Report

**Generated:** 2026-04-04 15:58:35
**Pipeline run:** 2026-04-04T13:58:34.936213+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["markdown_report<br/>4.0s"]
    style S0 fill:#90EE90
    S1["push<br/>2.2s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["publish<br/>0.6s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["setup<br/>3.8s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["calibrate<br/>60.1s"]
    style S4 fill:#FFB6C1
    S3 --> S4
    S5["lint<br/>0.1s"]
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
│  ✓ markdown_report              4.0s 🟢        │
│  ✓ push                         2.2s 🟢        │
│  ✓ publish                      0.6s 🟢        │
│  ✓ setup                        3.8s 🟢        │
│  ✗ calibrate                   60.1s 🔴        │
│  ✓ lint                         0.1s 🟢        │
├─────────────────────────────────────────────────────────────────┤
│  ❌ SOME GATES FAILED                                            │
│  ⏱️  Total time: 70.8s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| coverage | 32.9% | >= 55.0% | ❌ FAIL |

### 🔧 Stage Execution Details

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 4.0s
- **Return code:** 0

#### ✅ push
- **Status:** passed
- **Duration:** 2.2s
- **Return code:** 0

#### ✅ publish
- **Status:** passed
- **Duration:** 0.6s
- **Return code:** 0

#### ✅ setup
- **Status:** passed
- **Duration:** 3.8s
- **Return code:** 0

#### ❌ calibrate
- **Status:** failed
- **Duration:** 60.1s
- **Return code:** 124

#### ✅ lint
- **Status:** passed
- **Duration:** 0.1s
- **Return code:** 0


---

## 📝 Summary

❌ **Some quality gates failed.** Review the stage details above.
