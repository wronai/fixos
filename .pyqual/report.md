# Pyqual Pipeline Report

**Generated:** 2026-04-04 15:46:45
**Pipeline run:** 2026-04-04T13:46:42.810647+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["setup<br/>3.8s"]
    style S0 fill:#90EE90
    S1["lint<br/>0.0s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["markdown_report<br/>2.9s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["push<br/>2.1s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["publish<br/>0.0s"]
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
│  ✓ setup                        3.8s 🟢        │
│  ✓ lint                         0.0s 🟢        │
│  ✓ markdown_report              2.9s 🟢        │
│  ✓ push                         2.1s 🟢        │
│  ✓ publish                      0.0s 🟢        │
├─────────────────────────────────────────────────────────────────┤
│  ❌ SOME GATES FAILED                                            │
│  ⏱️  Total time: 8.8s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| coverage | 32.9% | >= 55.0% | ❌ FAIL |

### 🔧 Stage Execution Details

#### ✅ setup
- **Status:** passed
- **Duration:** 3.8s
- **Return code:** 0

#### ✅ lint
- **Status:** passed
- **Duration:** 0.0s
- **Return code:** 0

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 2.9s
- **Return code:** 0

#### ✅ push
- **Status:** passed
- **Duration:** 2.1s
- **Return code:** 0

#### ✅ publish
- **Status:** passed
- **Duration:** 0.0s
- **Return code:** 0


---

## 📝 Summary

❌ **Some quality gates failed.** Review the stage details above.
