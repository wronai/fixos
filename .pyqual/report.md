# Pyqual Pipeline Report

**Generated:** 2026-04-04 15:44:58
**Pipeline run:** 2026-04-04T13:44:55.840161+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["prefact<br/>60.8s"]
    style S0 fill:#90EE90
    S1["verify<br/>0.0s"]
    style S1 fill:#D3D3D3
    S0 --> S1
    S2["markdown_report<br/>2.6s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["setup<br/>2.6s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["lint<br/>0.0s"]
    style S4 fill:#90EE90
    S3 --> S4
    S5["push<br/>2.0s"]
    style S5 fill:#90EE90
    S4 --> S5
    S6["publish<br/>0.0s"]
    style S6 fill:#90EE90
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
│  ✓ prefact                     60.8s 🟢        │
│  ○ verify                       0.0s ⚪        │
│  ✓ markdown_report              2.6s 🟢        │
│  ✓ setup                        2.6s 🟢        │
│  ✓ lint                         0.0s 🟢        │
│  ✓ push                         2.0s 🟢        │
│  ✓ publish                      0.0s 🟢        │
├─────────────────────────────────────────────────────────────────┤
│  ❌ SOME GATES FAILED                                            │
│  ⏱️  Total time: 68.1s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| coverage | 32.9% | >= 55.0% | ❌ FAIL |

### 🔧 Stage Execution Details

#### ✅ prefact
- **Status:** passed
- **Duration:** 60.8s
- **Return code:** 0

#### ⏭️ verify
- **Status:** skipped
- **Duration:** 0.0s
- **Return code:** 0

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 2.6s
- **Return code:** 0

#### ✅ setup
- **Status:** passed
- **Duration:** 2.6s
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
- **Duration:** 0.0s
- **Return code:** 0


---

## 📝 Summary

❌ **Some quality gates failed.** Review the stage details above.
