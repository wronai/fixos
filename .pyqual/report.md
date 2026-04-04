# Pyqual Pipeline Report

**Generated:** 2026-04-04 15:59:08
**Pipeline run:** 2026-04-04T13:59:08.612341+00:00

---

## 🔄 Pipeline Flow Diagram

```mermaid
flowchart LR
    S0["setup<br/>3.8s"]
    style S0 fill:#90EE90
    S1["publish<br/>0.8s"]
    style S1 fill:#90EE90
    S0 --> S1
    S2["markdown_report<br/>4.1s"]
    style S2 fill:#90EE90
    S1 --> S2
    S3["push<br/>2.0s"]
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
│  ✓ setup                        3.8s 🟢        │
│  ✓ publish                      0.8s 🟢        │
│  ✓ markdown_report              4.1s 🟢        │
│  ✓ push                         2.0s 🟢        │
│  ✗ calibrate                   60.1s 🔴        │
│  ✓ lint                         0.1s 🟢        │
├─────────────────────────────────────────────────────────────────┤
│  🎉 ALL GATES PASSED ✓                                           │
│  ⏱️  Total time: 70.7s                                          │
└─────────────────────────────────────────────────────────────────┘
```

### 📊 Quality Gates

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|

### 🔧 Stage Execution Details

#### ✅ setup
- **Status:** passed
- **Duration:** 3.8s
- **Return code:** 0

#### ✅ publish
- **Status:** passed
- **Duration:** 0.8s
- **Return code:** 0

#### ✅ markdown_report
- **Status:** passed
- **Duration:** 4.1s
- **Return code:** 0

#### ✅ push
- **Status:** passed
- **Duration:** 2.0s
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

✅ **All quality gates passed!** Pipeline completed successfully in 70.7s.
