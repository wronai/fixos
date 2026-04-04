# Pyqual Pipeline Report

**Generated:** 2026-04-04 16:11:02
**Pipeline run:** 2026-04-04T14:11:00.224094+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["prefact<br/>86.2s"]
    style S0 fill:#90EE90
    S1["verify<br/>0.8s"]
    style S1 fill:#FFB6C1
    S0 --> S1
    S2["markdown_report<br/>2.8s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["setup<br/>2.7s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["lint<br/>0.0s"]
    style S4 fill:#90EE90
    S3 --> S4
    S5["push<br/>2.4s"]
    style S5 fill:#90EE90
    S4 --> S5
    S6["publish<br/>0.5s"]
    style S6 fill:#FFB6C1
    S5 --> S6
    G["✗ Gates Failed"]
    style G fill:#FFB6C1,stroke:#DC143C,stroke-width:3px
    S6 --> G
```

## 📈 ASCII Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                    PYQUAL PIPELINE FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│  ✓ prefact                     86.2s 🟢        │
│  ✗ verify                       0.8s 🔴        │
│  ✓ markdown_report              2.8s 🟢        │
│  ✓ setup                        2.7s 🟢        │
│  ✓ lint                         0.0s 🟢        │
│  ✓ push                         2.4s 🟢        │
│  ✗ publish                      0.5s 🔴        │
├─────────────────────────────────────────────────────────────────┤
│  ❌ SOME GATES FAILED                                            │
│  ⏱️  Total time: 95.3s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| coverage | 33.4% | >= 55.0% | ❌ FAIL |

### 🔧 Stage Execution Details

#### ✅ prefact
- **Status:** passed
- **Duration:** 86.2s
- **Return code:** 0

#### ❌ verify
- **Status:** failed
- **Duration:** 0.8s
- **Return code:** 2

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 2.8s
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
- **Duration:** 2.4s
- **Return code:** 0

#### ❌ publish
- **Status:** failed
- **Duration:** 0.5s
- **Return code:** 2


---

## 📝 Summary

❌ **Some quality gates failed.** Review the stage details above.
