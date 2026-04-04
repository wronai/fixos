# Pyqual Pipeline Report

**Generated:** 2026-04-04 16:05:06
**Pipeline run:** 2026-04-04T14:05:06.687506+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["prefact<br/>114.6s"]
    style S0 fill:#90EE90
    S1["verify<br/>1.1s"]
    style S1 fill:#FFB6C1
    S0 --> S1
    S2["setup<br/>3.7s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["lint<br/>0.0s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["markdown_report<br/>3.0s"]
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
│  ✓ prefact                    114.6s 🟢        │
│  ✗ verify                       1.1s 🔴        │
│  ✓ setup                        3.7s 🟢        │
│  ✓ lint                         0.0s 🟢        │
│  ✓ markdown_report              3.0s 🟢        │
├─────────────────────────────────────────────────────────────────┤
│  ❌ SOME GATES FAILED                                            │
│  ⏱️  Total time: 122.5s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| coverage | 33.4% | >= 55.0% | ❌ FAIL |

### 🔧 Stage Execution Details

#### ✅ prefact
- **Status:** passed
- **Duration:** 114.6s
- **Return code:** 0

#### ❌ verify
- **Status:** failed
- **Duration:** 1.1s
- **Return code:** 2

#### ✅ setup
- **Status:** passed
- **Duration:** 3.7s
- **Return code:** 0

#### ✅ lint
- **Status:** passed
- **Duration:** 0.0s
- **Return code:** 0

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 3.0s
- **Return code:** 0


---

## 📝 Summary

❌ **Some quality gates failed.** Review the stage details above.
