# Pyqual Pipeline Report

**Generated:** 2026-04-04 17:59:17
**Pipeline run:** 2026-04-04T15:59:14.470096+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["markdown_report<br/>2.9s"]
    style S0 fill:#90EE90
    S1["lint<br/>0.0s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["prefact<br/>60.4s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["verify<br/>1.3s"]
    style S3 fill:#FFB6C1
    S2 --> S3
    G["✗ Gates Failed"]
    style G fill:#FFB6C1,stroke:#DC143C,stroke-width:3px
    S3 --> G
```

## 📈 ASCII Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                    PYQUAL PIPELINE FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│  ✓ markdown_report              2.9s 🟢        │
│  ✓ lint                         0.0s 🟢        │
│  ✓ prefact                     60.4s 🟢        │
│  ✗ verify                       1.3s 🔴        │
├─────────────────────────────────────────────────────────────────┤
│  ❌ SOME GATES FAILED                                            │
│  ⏱️  Total time: 64.6s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| coverage | 27.5% | >= 55.0% | ❌ FAIL |

### 🔧 Stage Execution Details

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 2.9s
- **Return code:** 0

#### ✅ lint
- **Status:** passed
- **Duration:** 0.0s
- **Return code:** 0

#### ✅ prefact
- **Status:** passed
- **Duration:** 60.4s
- **Return code:** 0

#### ❌ verify
- **Status:** failed
- **Duration:** 1.3s
- **Return code:** 2


---

## 📝 Summary

❌ **Some quality gates failed.** Review the stage details above.
