# Pyqual Pipeline Report

**Generated:** 2026-04-04 18:03:11
**Pipeline run:** 2026-04-04T16:03:08.714300+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["prefact<br/>60.4s"]
    style S0 fill:#90EE90
    S1["verify<br/>1.3s"]
    style S1 fill:#FFB6C1
    S0 --> S1
    S2["markdown_report<br/>2.9s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["setup<br/>3.8s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["lint<br/>0.0s"]
    style S4 fill:#90EE90
    S3 --> S4
    S5["push<br/>2.2s"]
    style S5 fill:#90EE90
    S4 --> S5
    S6["publish<br/>9.5s"]
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
│  ✓ prefact                     60.4s 🟢        │
│  ✗ verify                       1.3s 🔴        │
│  ✓ markdown_report              2.9s 🟢        │
│  ✓ setup                        3.8s 🟢        │
│  ✓ lint                         0.0s 🟢        │
│  ✓ push                         2.2s 🟢        │
│  ✗ publish                      9.5s 🔴        │
├─────────────────────────────────────────────────────────────────┤
│  ❌ SOME GATES FAILED                                            │
│  ⏱️  Total time: 80.2s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| coverage | 27.5% | >= 55.0% | ❌ FAIL |

### 🔧 Stage Execution Details

#### ✅ prefact
- **Status:** passed
- **Duration:** 60.4s
- **Return code:** 0

#### ❌ verify
- **Status:** failed
- **Duration:** 1.3s
- **Return code:** 2

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 2.9s
- **Return code:** 0

#### ✅ setup
- **Status:** passed
- **Duration:** 3.8s
- **Return code:** 0

#### ✅ lint
- **Status:** passed
- **Duration:** 0.0s
- **Return code:** 0

#### ✅ push
- **Status:** passed
- **Duration:** 2.2s
- **Return code:** 0

#### ❌ publish
- **Status:** failed
- **Duration:** 9.5s
- **Return code:** 2


---

## 📝 Summary

❌ **Some quality gates failed.** Review the stage details above.
