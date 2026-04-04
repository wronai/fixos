# Pyqual Pipeline Report

**Generated:** 2026-04-04 15:45:38
**Pipeline run:** 2026-04-04T13:45:35.508118+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["verify<br/>0.0s"]
    style S0 fill:#D3D3D3
    S1["setup<br/>3.1s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["lint<br/>0.0s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["markdown_report<br/>2.7s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["push<br/>1.9s"]
    style S4 fill:#90EE90
    S3 --> S4
    S5["publish<br/>0.0s"]
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
│  ○ verify                       0.0s ⚪        │
│  ✓ setup                        3.1s 🟢        │
│  ✓ lint                         0.0s 🟢        │
│  ✓ markdown_report              2.7s 🟢        │
│  ✓ push                         1.9s 🟢        │
│  ✓ publish                      0.0s 🟢        │
├─────────────────────────────────────────────────────────────────┤
│  ❌ SOME GATES FAILED                                            │
│  ⏱️  Total time: 7.7s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| coverage | 32.9% | >= 55.0% | ❌ FAIL |

### 🔧 Stage Execution Details

#### ⏭️ verify
- **Status:** skipped
- **Duration:** 0.0s
- **Return code:** 0

#### ✅ setup
- **Status:** passed
- **Duration:** 3.1s
- **Return code:** 0

#### ✅ lint
- **Status:** passed
- **Duration:** 0.0s
- **Return code:** 0

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 2.7s
- **Return code:** 0

#### ✅ push
- **Status:** passed
- **Duration:** 1.9s
- **Return code:** 0

#### ✅ publish
- **Status:** passed
- **Duration:** 0.0s
- **Return code:** 0


---

## 📝 Summary

❌ **Some quality gates failed.** Review the stage details above.
