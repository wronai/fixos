# Pyqual Pipeline Report

**Generated:** 2026-04-04 16:30:16
**Pipeline run:** 2026-04-04T14:30:12.490211+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["verify<br/>0.8s"]
    style S0 fill:#FFB6C1
    S1["markdown_report<br/>2.7s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["setup<br/>8.6s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["lint<br/>0.0s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["push<br/>3.6s"]
    style S4 fill:#90EE90
    S3 --> S4
    S5["publish<br/>8.3s"]
    style S5 fill:#FFB6C1
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
│  ✗ verify                       0.8s 🔴        │
│  ✓ markdown_report              2.7s 🟢        │
│  ✓ setup                        8.6s 🟢        │
│  ✓ lint                         0.0s 🟢        │
│  ✓ push                         3.6s 🟢        │
│  ✗ publish                      8.3s 🔴        │
├─────────────────────────────────────────────────────────────────┤
│  ❌ SOME GATES FAILED                                            │
│  ⏱️  Total time: 23.9s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| coverage | 33.8% | >= 55.0% | ❌ FAIL |

### 🔧 Stage Execution Details

#### ❌ verify
- **Status:** failed
- **Duration:** 0.8s
- **Return code:** 2

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 2.7s
- **Return code:** 0

#### ✅ setup
- **Status:** passed
- **Duration:** 8.6s
- **Return code:** 0

#### ✅ lint
- **Status:** passed
- **Duration:** 0.0s
- **Return code:** 0

#### ✅ push
- **Status:** passed
- **Duration:** 3.6s
- **Return code:** 0

#### ❌ publish
- **Status:** failed
- **Duration:** 8.3s
- **Return code:** 2


---

## 📝 Summary

❌ **Some quality gates failed.** Review the stage details above.
