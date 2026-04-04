# Pyqual Pipeline Report

**Generated:** 2026-04-04 15:59:16
**Pipeline run:** 2026-04-04T13:59:16.836728+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["push<br/>2.1s"]
    style S0 fill:#90EE90
    S1["setup<br/>5.3s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["publish<br/>1.2s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["markdown_report<br/>7.0s"]
    style S3 fill:#90EE90
    S2 --> S3
    S4["calibrate<br/>60.1s"]
    style S4 fill:#FFB6C1
    S3 --> S4
    S5["lint<br/>0.1s"]
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
│  ✓ push                         2.1s 🟢        │
│  ✓ setup                        5.3s 🟢        │
│  ✓ publish                      1.2s 🟢        │
│  ✓ markdown_report              7.0s 🟢        │
│  ✗ calibrate                   60.1s 🔴        │
│  ✓ lint                         0.1s 🟢        │
├─────────────────────────────────────────────────────────────────┤
│  🎉 ALL GATES PASSED ✓                                           │
│  ⏱️  Total time: 75.7s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|

### 🔧 Stage Execution Details

#### ✅ push
- **Status:** passed
- **Duration:** 2.1s
- **Return code:** 0

#### ✅ setup
- **Status:** passed
- **Duration:** 5.3s
- **Return code:** 0

#### ✅ publish
- **Status:** passed
- **Duration:** 1.2s
- **Return code:** 0

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 7.0s
- **Return code:** 0

#### ❌ calibrate
- **Status:** failed
- **Duration:** 60.1s
- **Return code:** 124

#### ✅ lint
- **Status:** passed
- **Duration:** 0.1s
- **Return code:** 0


---

## 📝 Summary

✅ **All quality gates passed!** Pipeline completed successfully in 75.7s.
