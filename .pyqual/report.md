# Pyqual Pipeline Report

**Generated:** 2026-04-04 15:41:12
**Pipeline run:** 2026-04-04T13:41:09.735720+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["setup<br/>2.5s"]
    style S0 fill:#90EE90
    S1["prefact<br/>63.3s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["markdown_report<br/>2.8s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["lint<br/>0.0s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["verify<br/>0.0s"]
    style S4 fill:#D3D3D3
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
│  ✓ setup                        2.5s 🟢        │
│  ✓ prefact                     63.3s 🟢        │
│  ✓ markdown_report              2.8s 🟢        │
│  ✓ lint                         0.0s 🟢        │
│  ○ verify                       0.0s ⚪        │
├─────────────────────────────────────────────────────────────────┤
│  ❌ SOME GATES FAILED                                            │
│  ⏱️  Total time: 68.6s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| coverage | 32.9% | >= 55.0% | ❌ FAIL |

### 🔧 Stage Execution Details

#### ✅ setup
- **Status:** passed
- **Duration:** 2.5s
- **Return code:** 0

#### ✅ prefact
- **Status:** passed
- **Duration:** 63.3s
- **Return code:** 0

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 2.8s
- **Return code:** 0

#### ✅ lint
- **Status:** passed
- **Duration:** 0.0s
- **Return code:** 0

#### ⏭️ verify
- **Status:** skipped
- **Duration:** 0.0s
- **Return code:** 0


---

## 📝 Summary

❌ **Some quality gates failed.** Review the stage details above.
