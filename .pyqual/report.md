# Pyqual Pipeline Report

**Generated:** 2026-04-04 15:58:59
**Pipeline run:** 2026-04-04T13:58:58.813325+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["push<br/>2.0s"]
    style S0 fill:#90EE90
    S1["markdown_report<br/>3.6s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["publish<br/>0.7s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["calibrate<br/>60.1s"]
    style S3 fill:#FFB6C1
    S2 --> S3
    S4["lint<br/>0.0s"]
    style S4 fill:#90EE90
    S3 --> S4
    S5["setup<br/>3.5s"]
    style S5 fill:#90EE90
    S4 --> S5
    G["✓ All Gates Passed"]
    style G fill:#90EE90,stroke:#228B22,stroke-width:3px
    S5 --> G
```

## 📈 ASCII Visualization

```
┌─────────────────────────────────────────────────────────────────┐
│                    PYQUAL PIPELINE FLOW                         │
├─────────────────────────────────────────────────────────────────┤
│  ✓ push                         2.0s 🟢        │
│  ✓ markdown_report              3.6s 🟢        │
│  ✓ publish                      0.7s 🟢        │
│  ✗ calibrate                   60.1s 🔴        │
│  ✓ lint                         0.0s 🟢        │
│  ✓ setup                        3.5s 🟢        │
├─────────────────────────────────────────────────────────────────┤
│  🎉 ALL GATES PASSED ✓                                           │
│  ⏱️  Total time: 69.9s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|

### 🔧 Stage Execution Details

#### ✅ push
- **Status:** passed
- **Duration:** 2.0s
- **Return code:** 0

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 3.6s
- **Return code:** 0

#### ✅ publish
- **Status:** passed
- **Duration:** 0.7s
- **Return code:** 0

#### ❌ calibrate
- **Status:** failed
- **Duration:** 60.1s
- **Return code:** 124

#### ✅ lint
- **Status:** passed
- **Duration:** 0.0s
- **Return code:** 0

#### ✅ setup
- **Status:** passed
- **Duration:** 3.5s
- **Return code:** 0


---

## 📝 Summary

✅ **All quality gates passed!** Pipeline completed successfully in 69.9s.
